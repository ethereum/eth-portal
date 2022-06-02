from eth_utils import encode_hex


class PortalInserter:
    """
    Track a group of Portal nodes, and simplify pushing content to them.

    Eventually, it will intelligently choose which nodes to broadcast content
    to. At documentation time, it naively pushes all content to all supplied nodes.
    """

    MAX_FIELD_DISPLAY_LENGTH = 2048

    def __init__(self, web3_links):
        """
        Create an instance, with web3 links to the launched Portal nodes.
        """
        self._web3_links = web3_links

    def push_history(self, content_key: bytes, content_value: bytes):
        """
        Push the given Portal History content out to the group of portal clients.
        """
        content_key_hex = encode_hex(content_key)
        content_value_hex = encode_hex(content_value)

        value_len = len(content_value_hex)
        if value_len > self.MAX_FIELD_DISPLAY_LENGTH:
            value_suffix = f"... ({value_len-self.MAX_FIELD_DISPLAY_LENGTH} more)"
        else:
            value_suffix = ""

        print(
            "Propagate new history content with key, value:",
            content_key_hex,
            ",",
            content_value_hex[: self.MAX_FIELD_DISPLAY_LENGTH] + value_suffix,
        )

        # For now, just push to all inserting clients. When running more, be a
        #   bit smarter about selecting inserters closer to the content key
        for w3 in self._web3_links:
            result = w3.provider.make_request(
                "portal_historyStore", [content_key_hex, content_value_hex]
            )
            print("History store response:", result)
