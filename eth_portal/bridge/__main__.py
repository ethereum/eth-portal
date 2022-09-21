from argparse import ArgumentParser

from .run import launch_backfill, launch_bridge, launch_injector

# Parse CLI arguments
parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-l",
    "--latest",
    action="store_true",
    help="Track the head of the chain, and publish the latest content into the Portal network.",
)
group.add_argument(
    "-f",
    "--content-files",
    nargs="+",
    help="Load the content from the files, and publish them into the Portal network.",
)
group.add_argument(
    "-b",
    "--block-range",
    nargs=2,
    type=int,
    help=(
        "Load the blocks from the start number to the end number given (inclusive),"
        " and publish them into the Portal network."
    ),
)
args = parser.parse_args()

try:
    if args.latest:
        launch_bridge()
    elif args.content_files:
        launch_injector(args.content_files)
    elif args.block_range:
        start, end = args.block_range
        if start > end:
            raise RuntimeError(
                "The end block must be the same or larger than the start block"
            )
        else:
            launch_backfill(start, end)
    else:
        raise RuntimeError("Must run bridge with an option. Run with -h to see them.")
except KeyboardInterrupt:
    if args.latest:
        print("Clean exit of bridge launcher")
    elif args.content_files or args.block_range:
        print("Warning: process exited before pushing out all content")
    else:
        raise RuntimeError("Program ended early, with unknown command line argument")
