import os
from enum import Enum


class SessionEnvironment(str, Enum):
    """
    The environment of Session.

    :cvar ANTIOCH_CLOUD: The Antioch Cloud environment.
    :cvar LOCAL: The local environment.
    """

    ANTIOCH_CLOUD = "antioch_cloud"
    LOCAL = "local"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def check(cls) -> "SessionEnvironment":
        """
        Check the session environment by checking the KUBERNETES_SERVICE_HOST
        environment variable.

        :return: The session environment.
        """

        if os.environ.get("KUBERNETES_SERVICE_HOST") is not None:
            return cls.ANTIOCH_CLOUD
        else:
            return cls.LOCAL
