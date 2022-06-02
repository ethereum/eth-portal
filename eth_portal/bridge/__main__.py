from .run import launch_bridge

try:
    launch_bridge()
except KeyboardInterrupt:
    print("Clean exit of bridge launcher")
