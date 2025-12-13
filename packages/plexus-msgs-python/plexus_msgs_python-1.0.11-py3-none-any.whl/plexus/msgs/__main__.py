import argparse

from plexus.msgs.utils import generate_plexus_msg_tailor_cpp_code
from plexus.msgs.utils import generate_plexus_msg_tailor_java_code
from plexus.msgs.utils import generate_plexus_msg_tailor_python_code
from plexus.msgs.utils import import_plexus_msgs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang",
                        choices=["python", "cpp", "java"],
                        required=True,
                        help="Specify the language for which to generate the Plexus message tailor code.")
    parser.add_argument("--output",
                        type=str,
                        required=True,
                        help="Specify the output file path for the generated code.")
    parser.add_argument("--config",
                        type=str,
                        action="append",
                        help="Specify the configuration of the code generator.")

    args = parser.parse_args()

    kwargs = dict(config.split("=", 2) for config in (args.config or []))

    import_plexus_msgs()
    match args.lang:
        case "cpp":
            code = generate_plexus_msg_tailor_cpp_code(**kwargs)
        case "java":
            code = generate_plexus_msg_tailor_java_code(**kwargs)
        case "python":
            code = generate_plexus_msg_tailor_python_code(**kwargs)
        case _:
            raise ValueError(f"unsupported language '{args.lang}' specified")

    with open(args.output, "w") as fh:
        fh.write(code)
