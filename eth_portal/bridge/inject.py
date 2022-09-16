import binascii
from pathlib import Path
import time

from eth_utils import ValidationError, to_bytes, to_tuple

MINIMUM_OTHER_PEERS_OFFERED = 3
SECONDS_TO_FIND_MORE_PEERS = 10
# TODO make issue to supply directories in addition to files


@to_tuple
def parse_content_keys(content_files):
    for str_path in content_files:
        path = Path(str_path)
        if not path.exists():
            raise ValidationError(f"Supplied file {path!r} does not exist")
        if not path.is_file():
            raise ValidationError(
                f"Supplied path {path!r} does not point to a file (is it a directory?)"
            )
        if path.suffix != ".portalcontent":
            raise ValidationError(
                f"Supplied files must end in .portalcontent, unlike: {path!r}"
            )
        try:
            content_key = to_bytes(hexstr=path.stem)
        except binascii.Error:
            raise ValidationError(
                f"File names must be in a hex-encoded format, unlike: {path!r}"
            )

        yield content_key, path


@to_tuple
def attempt_inject_all(portal_inserter, parsed_paths):
    """
    Inject all the content items, returning any that do not offer to enough peers.

    Note that trin is currently returning the number of peers offered (not
    accepted), and ignores whether that content was previously offered. So on
    multiple attempts to call this method, the result can be considered a
    cumulative count of how many peers were offered.

    This method returns if the *most connected* bridge client doesn't offer to
    enough peers. It ignores any lesser-connected bridge clients, which may be
    offering to duplicate peers of the most-connected client.

    :param content_paths: a list of (content_key, Path) content items to inject to network

    :return: a tuple of content_paths that too few peers were interested in
    """
    print(f"Injecting {len(parsed_paths)} items")
    for content_key, path in parsed_paths:
        content_value = path.read_bytes()
        peer_offers = portal_inserter.push_history(content_key, content_value)
        if max(peer_offers) < MINIMUM_OTHER_PEERS_OFFERED:
            yield content_key, path


def inject_content(portal_inserter, content_files):
    parsed_paths = parse_content_keys(content_files)

    failed_paths = attempt_inject_all(portal_inserter, parsed_paths)

    while len(failed_paths):
        print(f"Too few peers were interested in {len(failed_paths)} items")
        print(f"Retrying in {SECONDS_TO_FIND_MORE_PEERS} seconds...")
        time.sleep(SECONDS_TO_FIND_MORE_PEERS)
        failed_paths = attempt_inject_all(portal_inserter, failed_paths)

    print(f"Successfully injected all {len(parsed_paths)} content items")
