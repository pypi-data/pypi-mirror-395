import timeit

from iker.common.utils.randutils import randomizer

from plexus.msgs.plexus_common_pb2 import Timestamp
from plexus.msgs.testing.plexus_msgs_testing_dummy_pb2 import DummyMessage
from plexus.msgs.utils import copy_plexus_message, copy_plexus_message_2

make_int32 = lambda: randomizer().next_int(-2147483648, 2147483647)
make_int64 = lambda: randomizer().next_int(-9223372036854775808, 9223372036854775807)
make_double = lambda: randomizer().next_float()
make_bool = lambda: randomizer().next_bool()
make_string = lambda: randomizer().random_alphanumeric(randomizer().next_int(10, 20))
make_enum = lambda: randomizer().choose(DummyMessage.Enum.values())
make_timestamp = lambda: Timestamp(seconds=randomizer().next_int(0, 1000000),
                                   nanos=randomizer().next_int(0, 1000000000))

fill_repeated = lambda xs, gen: xs.extend(gen() for _ in range(randomizer().next_int(5, 10)))


def random_dummy_message(message_cls):
    message = message_cls()
    message.optional_int32 = make_int32()
    fill_repeated(message.repeated_int32, make_int32)
    message.optional_int64 = make_int64()
    fill_repeated(message.repeated_int64, make_int64)
    message.optional_double = make_double()
    fill_repeated(message.repeated_double, make_double)
    message.optional_bool = make_bool()
    fill_repeated(message.repeated_bool, make_bool)
    message.optional_string = make_string()
    fill_repeated(message.repeated_string, make_string)
    message.optional_enum = make_enum()
    fill_repeated(message.repeated_enum, make_enum)
    message.omitted_optional_int32 = make_int32()
    fill_repeated(message.omitted_repeated_int32, make_int32)
    message.omitted_optional_int64 = make_int64()
    fill_repeated(message.omitted_repeated_int64, make_int64)
    message.omitted_optional_double = make_double()
    fill_repeated(message.omitted_repeated_double, make_double)
    message.omitted_optional_bool = make_bool()
    fill_repeated(message.omitted_repeated_bool, make_bool)
    message.omitted_optional_string = make_string()
    fill_repeated(message.omitted_repeated_string, make_string)
    message.omitted_optional_enum = make_enum()
    fill_repeated(message.omitted_repeated_enum, make_enum)
    message.optional_timestamp.CopyFrom(make_timestamp())
    fill_repeated(message.repeated_timestamp, make_timestamp)

    return message


def compare_dummy_message(copy, origin, *, has_omitted_fields: bool = True):
    assert copy.optional_int32 == origin.optional_int32
    assert copy.repeated_int32 == origin.repeated_int32
    assert copy.optional_int64 == origin.optional_int64
    assert copy.repeated_int64 == origin.repeated_int64
    assert copy.optional_double == origin.optional_double
    assert copy.repeated_double == origin.repeated_double
    assert copy.optional_bool == origin.optional_bool
    assert copy.repeated_bool == origin.repeated_bool
    assert copy.optional_string == origin.optional_string
    assert copy.repeated_string == origin.repeated_string
    assert copy.optional_enum == origin.optional_enum
    assert copy.repeated_enum == origin.repeated_enum
    assert copy.optional_timestamp == origin.optional_timestamp
    assert copy.repeated_timestamp == origin.repeated_timestamp
    if has_omitted_fields:
        assert not copy.HasField("omitted_optional_int32")
        assert len(copy.omitted_repeated_int32) == 0
        assert not copy.HasField("omitted_optional_int64")
        assert len(copy.omitted_repeated_int64) == 0
        assert not copy.HasField("omitted_optional_double")
        assert len(copy.omitted_repeated_double) == 0
        assert not copy.HasField("omitted_optional_bool")
        assert len(copy.omitted_repeated_bool) == 0
        assert not copy.HasField("omitted_optional_string")
        assert len(copy.omitted_repeated_string) == 0
        assert not copy.HasField("omitted_optional_enum")
        assert len(copy.omitted_repeated_enum) == 0
        assert not copy.HasField("omitted_optional_timestamp")
        assert len(copy.omitted_repeated_timestamp) == 0


def test_copy_plexus_message():
    time_elapsed = 0
    for _ in range(1000):
        message_origin = random_dummy_message(DummyMessage)
        message_origin.optional_nested_message.CopyFrom(random_dummy_message(DummyMessage.NestedDummyMessage))
        message_origin.repeated_nested_message.extend(
            random_dummy_message(DummyMessage.NestedDummyMessage) for _ in range(randomizer().next_int(5, 10)))
        message_origin.omitted_optional_nested_message.CopyFrom(random_dummy_message(DummyMessage.NestedDummyMessage))
        message_origin.omitted_repeated_nested_message.extend(
            random_dummy_message(DummyMessage.NestedDummyMessage) for _ in range(randomizer().next_int(5, 10)))

        start_time = timeit.default_timer()
        message_copy = copy_plexus_message(message_origin, tailored=True)
        time_elapsed += timeit.default_timer() - start_time

        compare_dummy_message(message_copy, message_origin)
        compare_dummy_message(message_copy.optional_nested_message, message_origin.optional_nested_message)
        for copy, origin in zip(message_copy.repeated_nested_message, message_origin.repeated_nested_message):
            compare_dummy_message(copy, origin)
        assert not message_copy.HasField("omitted_optional_nested_message")
        assert len(message_copy.omitted_repeated_nested_message) == 0

    print(f"Average time elapsed for 'copy_plexus_message': {time_elapsed / 1000:.6f} seconds")


def test_copy_plexus_message_2():
    time_elapsed = 0
    for _ in range(1000):
        message_origin = random_dummy_message(DummyMessage)
        message_origin.optional_nested_message.CopyFrom(random_dummy_message(DummyMessage.NestedDummyMessage))
        message_origin.repeated_nested_message.extend(
            random_dummy_message(DummyMessage.NestedDummyMessage) for _ in range(randomizer().next_int(5, 10)))
        message_origin.omitted_optional_nested_message.CopyFrom(random_dummy_message(DummyMessage.NestedDummyMessage))
        message_origin.omitted_repeated_nested_message.extend(
            random_dummy_message(DummyMessage.NestedDummyMessage) for _ in range(randomizer().next_int(5, 10)))

        start_time = timeit.default_timer()
        message_copy = copy_plexus_message_2(message_origin, tailored=True)
        time_elapsed += timeit.default_timer() - start_time

        compare_dummy_message(message_copy, message_origin)
        compare_dummy_message(message_copy.optional_nested_message, message_origin.optional_nested_message)
        for copy, origin in zip(message_copy.repeated_nested_message, message_origin.repeated_nested_message):
            compare_dummy_message(copy, origin)
        assert not message_copy.HasField("omitted_optional_nested_message")
        assert len(message_copy.omitted_repeated_nested_message) == 0

    print(f"Average time elapsed for 'copy_plexus_message_2': {time_elapsed / 1000:.6f} seconds")
