from argparse import ArgumentParser

from .run import launch_backfill, launch_bridge, launch_injector, launch_patch_recent

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
group.add_argument(
    "--patch-recent",
    nargs=1,
    type=int,
    help=(
        "Load the N most recent blocks from the current head,"
        " publish them into the Portal network, and shut down."
    ),
)
parser.add_argument(
    "-p",
    "--provider",
    choices=["infura", "cloudflare-auth"],
    default="infura",
    help="What kind of provider to use. Defaults to Infura.",
)
args = parser.parse_args()

try:
    if args.latest:
        launch_bridge(args.provider)
    elif args.content_files:
        launch_injector(args.content_files)
    elif args.block_range:
        start, end = args.block_range
        if start > end:
            raise RuntimeError(
                "The end block must be the same or larger than the start block"
            )
        else:
            launch_backfill(start, end, args.provider)
    elif args.patch_recent:
        launch_patch_recent(args.patch_recent[0], args.provider)
    else:
        raise RuntimeError("Must run bridge with an option. Run with -h to see them.")
except KeyboardInterrupt:
    if args.latest:
        print("Clean exit of bridge launcher")
    elif args.content_files or args.block_range:
        print("Warning: process exited before pushing out all content")
    else:
        raise RuntimeError("Program ended early, with unknown command line argument")
