from argparse import ArgumentParser

from .run import launch_bridge, launch_injector

# Parse CLI arguments
parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-l", "--latest")
group.add_argument("-c", "--content-files", nargs="+")
args = parser.parse_args()

try:
    if args.latest:
        launch_bridge()
    elif args.content_files:
        launch_injector(args.content_files)
    else:
        raise RuntimeError("Must run bridge with an option. Run with -h to see them.")
except KeyboardInterrupt:
    if args.latest:
        print("Clean exit of bridge launcher")
    elif args.content_files:
        print("Warning: process exited before pushing out all content")
    else:
        raise RuntimeError("Program ended early, with unknown command line argument")
