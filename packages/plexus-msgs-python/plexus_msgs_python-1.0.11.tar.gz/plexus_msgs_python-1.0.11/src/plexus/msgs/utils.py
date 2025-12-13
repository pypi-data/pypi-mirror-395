import base64
import copy
import importlib
import importlib.resources
import pkgutil
import textwrap
from collections.abc import Callable
from types import ModuleType
from typing import Any

import jinja2
from google.protobuf import descriptor_pool, message_factory
from google.protobuf.descriptor_pb2 import (
    DescriptorProto as MessageDesc,
    FieldDescriptorProto as FieldDesc,
    FileDescriptorProto as FileDesc,
    FileDescriptorSet as FileDescSet,
)
from google.protobuf.message import Message
from iker.common.utils.funcutils import memorized, singleton

from plexus.msgs.plexus_common_message_pb2 import (
    Message as PlexusMessageProto,
    MessageHeader as PlexusMessageHeaderProto,
)

__all__ = [
    "import_plexus_msgs",
    "get_protobuf_class",
    "wrap_plexus_message",
    "unwrap_plexus_message",
    "import_submodules",
    "traverse_descriptor_file",
    "plexus_msgs_omitted_fields",
    "plexus_msgs_composite_fields",
    "generate_plexus_msg_tailor_python_code",
    "generate_plexus_msg_tailor_java_code",
    "generate_plexus_msg_tailor_cpp_code",
    "tailor_plexus_msg",
    "tailor_plexus_msg_2",
    "copy_plexus_message",
    "copy_plexus_message_2",
]


@singleton
def import_plexus_msgs():
    """Imports all modules in the ``plexus.msgs`` package"""
    import plexus.msgs
    return import_submodules(plexus.msgs)


@singleton
def plexus_msgs_descriptor_path() -> str:
    """Returns the path to the plexus messages descriptor file"""
    import plexus.msgs
    return str(importlib.resources.files(plexus.msgs).joinpath("descriptor.pb"))


@memorized
def get_protobuf_class[MessageT: Message](name: str) -> Callable[..., MessageT]:
    """Returns the protobuf class for a given name"""
    import_plexus_msgs()

    pool = descriptor_pool.Default()
    desc = pool.FindMessageTypeByName(name)
    return message_factory.GetMessageClass(desc)


def wrap_plexus_message[MessageT: Message](header: PlexusMessageHeaderProto, payload: MessageT) -> bytes:
    """Wraps a plexus message into a protobuf encoded string"""
    if header.payload_type != payload.DESCRIPTOR.full_name:
        raise ValueError(
            f"header payload type '{header.payload_type}' does not match payload type '{payload.DESCRIPTOR.full_name}'"
        )

    plexus_message_pb = PlexusMessageProto()
    plexus_message_pb.header.CopyFrom(header)
    plexus_message_pb.payload = base64.b64encode(payload.SerializeToString())

    return plexus_message_pb.SerializeToString()


def unwrap_plexus_message[MessageT: Message](data: bytes) -> tuple[PlexusMessageHeaderProto, MessageT]:
    """Unwraps a plexus message from a protobuf encoded string"""
    plexus_message_pb = PlexusMessageProto()
    plexus_message_pb.ParseFromString(data)

    payload_class = get_protobuf_class(plexus_message_pb.header.payload_type)
    payload_pb = payload_class()
    payload_pb.ParseFromString(base64.b64decode(plexus_message_pb.payload))

    return plexus_message_pb.header, payload_pb


def import_submodules(package: str | ModuleType) -> dict[str, ModuleType]:
    """Imports all submodules of a package, recursively"""
    if isinstance(package, str):
        return import_submodules(importlib.import_module(package))
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        results[name] = importlib.import_module(name)
    return results


def traverse_descriptor_file(
    descriptor_path: str,
    message_ops: Callable[[str, FileDesc, MessageDesc], ...],
    field_ops: Callable[[str, FileDesc, MessageDesc, FieldDesc], ...],
):
    """
    Traverses a protobuf descriptor file and applies operations on messages and fields.

    :param descriptor_path: Path to the protobuf descriptor file.
    :param message_ops: Callable that takes a qualified name, a file descriptor, and a message descriptor.
    :param field_ops: Callable that takes a qualified name, a file descriptor, a message descriptor, and a field
    descriptor.
    """

    def traverse(file_desc: FileDesc, message_desc: MessageDesc, parent_qualified_name: str):
        qualified_name = parent_qualified_name + "." + message_desc.name if parent_qualified_name else message_desc.name

        for field_desc in message_desc.field:
            field_ops(qualified_name, file_desc, message_desc, field_desc)
        message_ops(qualified_name, file_desc, message_desc)

        for nested_message_desc in message_desc.nested_type:
            traverse(file_desc, nested_message_desc, qualified_name)

    with open(descriptor_path, "rb") as fh:
        file_desc_set = FileDescSet()
        file_desc_set.ParseFromString(fh.read())

    for file_desc in file_desc_set.file:
        for message_desc in file_desc.message_type:
            traverse(file_desc, message_desc, "." + file_desc.package)


def plexus_msgs_omitted_fields(
    descriptor_path: str = plexus_msgs_descriptor_path(),
) -> dict[str, tuple[FileDesc, MessageDesc, dict[str, FieldDesc]]]:
    class OptionCollector(object):
        def __init__(self, option_name: str, option_value_check: Callable[[Any], bool]):
            self.option_name = option_name
            self.option_value_check = option_value_check
            self.collected_fields: list[FieldDesc] = []
            self.collected_messages: list[tuple[str, FileDesc, MessageDesc, list[FieldDesc]]] = []

        def message_ops(self, qualified_name: str, file_desc: FileDesc, message_desc: MessageDesc):
            if self.collected_fields:
                self.collected_messages.append((qualified_name, file_desc, message_desc, self.collected_fields))
            self.collected_fields = []

        def field_ops(
            self,
            qualified_name: str,
            file_desc: FileDesc,
            message_desc: MessageDesc,
            field_desc: FieldDesc,
        ):
            for option, option_value in field_desc.options.ListFields():
                if getattr(option, "name", None) == self.option_name and self.option_value_check(option_value):
                    self.collected_fields.append(field_desc)
                    return

    collector = OptionCollector("omitted", lambda x: x is True)

    traverse_descriptor_file(descriptor_path, collector.message_ops, collector.field_ops)

    return {qualified_name: (file_desc, message_desc, {field_desc.name: field_desc for field_desc in field_desc_list})
            for qualified_name, file_desc, message_desc, field_desc_list in collector.collected_messages}


def plexus_msgs_composite_fields(
    descriptor_path: str = plexus_msgs_descriptor_path(),
) -> dict[str, tuple[FileDesc, MessageDesc, dict[str, FieldDesc]]]:
    class MessageTypeTreeCollector(object):
        def __init__(self):
            self.collected_fields: list[FieldDesc] = []
            self.collected_messages: list[tuple[str, FileDesc, MessageDesc, list[FieldDesc]]] = []

        def message_ops(self, qualified_name: str, file_desc: FileDesc, message_desc: MessageDesc):
            if self.collected_fields:
                self.collected_messages.append((qualified_name, file_desc, message_desc, self.collected_fields))
            self.collected_fields = []

        def field_ops(
            self,
            qualified_name: str,
            file_desc: FileDesc,
            message_desc: MessageDesc,
            field_desc: FieldDesc,
        ):
            if field_desc.type != FieldDesc.TYPE_MESSAGE:
                return
            self.collected_fields.append(field_desc)

    collector = MessageTypeTreeCollector()

    traverse_descriptor_file(descriptor_path, collector.message_ops, collector.field_ops)

    return {qualified_name: (file_desc, message_desc, {field_desc.name: field_desc for field_desc in field_desc_list})
            for qualified_name, file_desc, message_desc, field_desc_list in collector.collected_messages}


def collect_plexus_msg_tailor_specs(
    descriptor_path: str = plexus_msgs_descriptor_path(),
) -> list[tuple[str, FileDesc, MessageDesc, list[FieldDesc], list[FieldDesc]]]:
    omitted_fields = plexus_msgs_omitted_fields(descriptor_path)
    composite_fields = plexus_msgs_composite_fields(descriptor_path)

    def detect_omission(qualified_name: str, visited: set[str] = None) -> bool:
        visited = visited or set()
        if qualified_name in visited:
            return False
        if qualified_name in omitted_fields:
            return True

        if qualified_name in composite_fields:
            _, _, field_desc_map = composite_fields[qualified_name]
            return any(detect_omission(field_desc.type_name, visited | {qualified_name})
                       for field_desc in field_desc_map.values())
        return False

    specs = []
    for qualified_name, (file_desc, message_desc, field_desc_map) in composite_fields.items():
        if not detect_omission(qualified_name):
            continue
        _, _, omitted_field_desc_map = omitted_fields.get(qualified_name, (None, None, {}))
        composite_field_desc_list = []
        for field_desc in field_desc_map.values():
            if not detect_omission(field_desc.type_name) or field_desc.name in omitted_field_desc_map:
                continue
            composite_field_desc_list.append(field_desc)
        specs.append(
            (
                qualified_name,
                file_desc,
                message_desc,
                list(omitted_field_desc_map.values()),
                composite_field_desc_list,
            )
        )

    return specs


def generate_plexus_msg_tailor_python_code(
    descriptor_path: str = plexus_msgs_descriptor_path(),
    *,
    tailor_function_name: str = "tailor_plexus_msg"
) -> str:
    tailors = [
        {
            "qualified_name": qualified_name,
            "tailor_function_name": "tailor" + "_".join(qualified_name.split(".")),
            "omitted_fields": [field_desc.name for field_desc in omitted_field_desc_list],
            "composite_fields": [
                {
                    "name": field_desc.name,
                    "repeated": field_desc.label == FieldDesc.LABEL_REPEATED,
                }
                for field_desc in composite_field_desc_list],
        }
        for qualified_name, _, _, omitted_field_desc_list, composite_field_desc_list
        in collect_plexus_msg_tailor_specs(descriptor_path)
    ]

    template_str = textwrap.dedent(
        """
        # AUTO-GENERATED FILE. DO NOT EDIT.
        import copy

        from google.protobuf.message import Message

        {% for tailor in tailors %}

        def {{ tailor.tailor_function_name }}(message: Message):
            {% for field_name in tailor.omitted_fields %}
            message.ClearField("{{ field_name }}")
            {% endfor %}
            {% for field in tailor.composite_fields %}
            {% if field.repeated %}
            for item in message.{{ field.name }}:
                {{ settings.tailor_function_name }}(item)
            {% else %}
            if message.HasField("{{ field.name }}"):
                {{ settings.tailor_function_name }}(message.{{ field.name }})
            {% endif %}
            {% endfor %}
            return message

        {% endfor %}

        PLEXUS_MSG_TAILORS_REGISTRY = {
        {% for tailor in tailors %}
            "{{ tailor.qualified_name }}": {{ tailor.tailor_function_name }},
        {% endfor %}
        }


        def {{ settings.tailor_function_name }}(message: Message):
            qualified_name = "." + message.DESCRIPTOR.full_name
            if qualified_name in PLEXUS_MSG_TAILORS_REGISTRY:
                return PLEXUS_MSG_TAILORS_REGISTRY[qualified_name](message)
            return message
        """
    )

    env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)

    template = env.from_string(template_str)
    rendered = template.render(tailors=tailors,
                               settings=dict(tailor_function_name=tailor_function_name))

    return rendered


def generate_plexus_msg_tailor_java_code(
    descriptor_path: str = plexus_msgs_descriptor_path(),
    *,
    tailor_package_name: str = "plexus.msgs",
    tailor_class_name: str = "PlexusMsgTailor",
    tailer_method_name: str = "tailor",
) -> str:
    def snake_case_to_camel_case(s: str) -> str:
        return "".join(word.capitalize() for word in s.split("_"))

    tailors = [
        {
            "qualified_name": qualified_name,
            "message_class_name": qualified_name[1:],
            "omitted_fields": [field_desc.name for field_desc in omitted_field_desc_list],
            "composite_fields": [
                {
                    "name": field_desc.name,
                    "repeated": field_desc.label == FieldDesc.LABEL_REPEATED,
                }
                for field_desc in composite_field_desc_list],
        }
        for qualified_name, file_desc, _, omitted_field_desc_list, composite_field_desc_list
        in collect_plexus_msg_tailor_specs(descriptor_path)
    ]

    template_str = textwrap.dedent(
        """
        // AUTO-GENERATED FILE. DO NOT EDIT.
        package {{ settings.tailor_package_name }};

        public class {{ settings.tailor_class_name }} {
            {% for tailor in tailors %}

            public static {{ tailor.message_class_name }} tailorMessage({{ tailor.message_class_name }} message) {
                var builder = message.toBuilder();
                {% for field_name in tailor.omitted_fields %}
                builder.clear{{ field_name|snake_case_to_camel_case }}();
                {% endfor %}
                {% for field in tailor.composite_fields %}
                {% if field.repeated %}
                for (int i = 0; i < builder.get{{ field.name|snake_case_to_camel_case }}Count(); i++) {
                    builder.set{{ field.name|snake_case_to_camel_case }}(
                            i, tailorMessage(builder.get{{ field.name|snake_case_to_camel_case }}(i)));
                }
                {% else %}
                if (builder.has{{ field.name|snake_case_to_camel_case }}()) {
                    builder.set{{ field.name|snake_case_to_camel_case }}(
                            tailorMessage(message.get{{ field.name|snake_case_to_camel_case }}()));
                }
                {% endif %}
                {% endfor %}
                return builder.build();
            }

            {% endfor %}

            public static <T extends com.google.protobuf.Message> T {{ settings.tailer_method_name}}(T message) {
                {% for tailor in tailors %}
                if (message instanceof {{ tailor.message_class_name }})
                    return (T) tailorMessage(({{ tailor.message_class_name }}) message);
                {% endfor %}
                return message;
            }
        }
        """
    )

    env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
    env.filters["snake_case_to_camel_case"] = snake_case_to_camel_case

    template = env.from_string(template_str)
    rendered = template.render(tailors=tailors,
                               settings=dict(tailor_package_name=tailor_package_name,
                                             tailor_class_name=tailor_class_name,
                                             tailer_method_name=tailer_method_name))

    return rendered


def generate_plexus_msg_tailor_cpp_code(
    descriptor_path: str = plexus_msgs_descriptor_path(),
    *,
    tailor_namespace: str = "plexus::msgs",
    tailor_class_name: str = "PlexusMsgTailor",
    tailor_method_name: str = "Tailor",
) -> str:
    def snake_case_to_pascal_case(s: str) -> str:
        return "".join(word.capitalize() for word in s.split("_"))

    tailors = [
        {
            "qualified_name": qualified_name,
            "message_class_name": qualified_name.replace(".", "::"),
            "omitted_fields": [field_desc.name for field_desc in omitted_field_desc_list],
            "composite_fields": [
                {
                    "name": field_desc.name,
                    "repeated": field_desc.label == FieldDesc.LABEL_REPEATED,
                }
                for field_desc in composite_field_desc_list],
        }
        for qualified_name, file_desc, _, omitted_field_desc_list, composite_field_desc_list
        in collect_plexus_msg_tailor_specs(descriptor_path)
    ]

    template_str = textwrap.dedent(
        """
        // AUTO-GENERATED FILE. DO NOT EDIT.
        #pragma once


        namespace {{ settings.tailor_namespace }} {


        class {{ settings.tailor_class_name }} {
        public:
            {% for tailor in tailors %}

            static void TailorMessage({{ tailor.message_class_name }} &message) {
                {% for field_name in tailor.omitted_fields %}
                message.clear_{{ field_name }}();
                {% endfor %}
                {% for field in tailor.composite_fields %}
                {% if field.repeated %}
                for (int i = 0; i < message.mutable_{{ field.name }}()->size(); ++i) {
                    {{ settings.tailor_class_name }}::TailorMessage(message.mutable_{{ field.name }}()->at(i));
                }
                {% else %}
                if (message.has_{{ field.name }}()) {
                    {{ settings.tailor_class_name }}::TailorMessage(*message.mutable_{{ field.name }}());
                }
                {% endif %}
                {% endfor %}
            }

            {% endfor %}

            template <typename T>
            static auto {{ settings.tailor_method_name }}(const T &message) {
                return message;
            }
        };

        {% for tailor in tailors %}

        template <>
        auto {{ settings.tailor_class_name }}::{{ settings.tailor_method_name }}(const {{ tailor.message_class_name }} &message) {
            auto copy = message;
            {{ settings.tailor_class_name }}::TailorMessage(copy);
            return copy;
        }

        {% endfor %}

        } // namespace {{ settings.tailor_namespace }}
        """
    )

    env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
    env.filters["snake_case_to_pascal_case"] = snake_case_to_pascal_case

    template = env.from_string(template_str)
    rendered = template.render(tailors=tailors,
                               settings=dict(tailor_namespace=tailor_namespace,
                                             tailor_class_name=tailor_class_name,
                                             tailor_method_name=tailor_method_name))

    return rendered


def make_tailor_plexus_msg():
    import_plexus_msgs()

    codegen_module = ModuleType("codegen")
    exec(generate_plexus_msg_tailor_python_code(), codegen_module.__dict__)

    return codegen_module.tailor_plexus_msg


tailor_plexus_msg = make_tailor_plexus_msg()


def tailor_plexus_msg_2[MessageT: Message](message: MessageT):
    qualified_name = "." + message.DESCRIPTOR.full_name
    _, _, omitted_field_desc_map = plexus_msgs_omitted_fields().get(qualified_name, (None, None, {}))
    if not omitted_field_desc_map:
        return message

    for field_desc in message.DESCRIPTOR.fields:
        if field_desc.name in omitted_field_desc_map:
            message.ClearField(field_desc.name)
        elif field_desc.type == FieldDesc.TYPE_MESSAGE:
            value = getattr(message, field_desc.name)
            if field_desc.label == FieldDesc.LABEL_REPEATED:
                for item in value:
                    tailor_plexus_msg(item)
            elif value is not None and value.ByteSize():
                tailor_plexus_msg(value)
    return message


def copy_plexus_message[MessageT: Message](message: MessageT, *, tailored: bool = False):
    message_copy = copy.deepcopy(message)
    return tailor_plexus_msg(message_copy) if tailored else message_copy


def copy_plexus_message_2[MessageT: Message](message: MessageT, *, tailored: bool = False) -> MessageT:
    message_copy = copy.deepcopy(message)
    return tailor_plexus_msg_2(message_copy) if tailored else message_copy
