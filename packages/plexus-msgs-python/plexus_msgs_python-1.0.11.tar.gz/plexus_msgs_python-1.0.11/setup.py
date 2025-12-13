import argparse
import os

from iker.setup import setup, version_string
from plexus.protobuf.setup import compile_protos

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="setup script integrating dynamic version printer")
    parser.add_argument("--print-version-string", action="store_true", help="print version string and exit")

    args, _ = parser.parse_known_args()
    if args.print_version_string:
        print(version_string())
    else:
        compile_protos(os.path.join(os.path.dirname(__file__), "src"),
                       ["/usr/share/plexus_msgs/protos"],
                       ["/usr/share/plexus_msgs/protos"],
                       descriptor_path=os.path.join(
                           os.path.dirname(__file__), "src", "plexus", "msgs", "descriptor.pb"))
        setup()
