import sys

from .run import launch_bridge

content_files = sys.argv[1:]
try:
    # if any content files are supplied, inject those instead of following the chain head
    launch_bridge(content_files)
except KeyboardInterrupt:
    if len(content_files):
        print("Warning: process exited before pushing out all content")
    else:
        print("Clean exit of bridge launcher")
