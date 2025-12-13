class RomeError(Exception):
    """
    Base error for Rome API operations.
    """


class RomeAuthError(RomeError):
    """
    Authentication error when interacting with Rome API.
    """


class RomeNetworkError(RomeError):
    """
    Network error when interacting with Rome API.
    """
