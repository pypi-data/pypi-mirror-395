"""Manages authentication with QCI Connect server and mini-orchestrator."""
from collections.abc import Mapping


class DummyTokenManager:
    """Dummy token manager for use with mini-orchestrator."""
    def __init__(self):
        """Init Dummy token manager for use with mini-orchestrator."""
        pass

    def add_auth_header(self, headers: Mapping) -> dict:
        """Returns unmodified headers dictionary."""
        return headers


class QciConnectTokenManager:
    """Dummy token manager for use with mini-orchestrator."""
    def __init__(self, token: str):
        """Init Dummy token manager for use with mini-orchestrator."""
        self._token_header = {'x-api-key': token}

    def add_auth_header(self, headers: Mapping) -> dict:
        """Returns unmodified headers dictionary."""
        headers.update(self._token_header)
        return headers
