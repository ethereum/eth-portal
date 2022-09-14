import binascii
from pathlib import Path

from eth_utils import ValidationError, to_bytes, to_tuple

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


def inject_content(portal_inserter, content_files):
    parsed_paths = parse_content_keys(content_files)

    print(f"Injecting {len(parsed_paths)} items of content...")
    for content_key, path in parsed_paths:
        content_value = path.read_bytes()
        portal_inserter.push_history(content_key, content_value)
