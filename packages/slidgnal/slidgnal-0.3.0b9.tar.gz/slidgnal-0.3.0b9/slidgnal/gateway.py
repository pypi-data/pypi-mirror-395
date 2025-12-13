from logging import getLevelName, getLogger
from pathlib import Path
from typing import TYPE_CHECKING

from slidge import BaseGateway, global_config

from . import config
from .generated import signal

if TYPE_CHECKING:
    from .session import Session

REGISTRATION_INSTRUCTIONS = (
    "Continue and scan the resulting QR codes on your main device. More "
    "information at https://slidge.im/docs/slidgnal/main/user/registration.html"
)

WELCOME_MESSAGE = (
    "Thank you for registering! Please scan the following QR code on your main device "
    "to complete registration, or type 'help' to list other available commands."
)


class Gateway(BaseGateway):
    COMPONENT_NAME = "Signal (slidge)"
    COMPONENT_TYPE = "signal"
    COMPONENT_AVATAR = "https://signal.org/assets/images/favicon/apple-touch-icon.png"
    ROSTER_GROUP = "Signal"

    REGISTRATION_INSTRUCTIONS = REGISTRATION_INSTRUCTIONS
    WELCOME_MESSAGE = WELCOME_MESSAGE
    REGISTRATION_FIELDS = []

    GROUPS = True
    PROPER_RECEIPTS = True

    def __init__(self):
        super().__init__()
        self.signal = signal.NewGateway()
        self.signal.Name = "Slidge on " + str(global_config.JID)
        self.signal.LogLevel = getLevelName(getLogger().level)

        assert config.DB_PATH is not None
        Path(config.DB_PATH.parent).mkdir(exist_ok=True)
        self.signal.DBPath = str(config.DB_PATH) + config.DB_PARAMS

        self.signal.Init()

    async def validate(self, user_jid, registration_form):
        """
        Validate registration form. A no-op for Signal, as actual registration takes place
        after in-band registration commands complete; see :meth:`.Session.login` for more.
        """
        pass

    async def unregister(self, session: "Session"):  # type:ignore
        """
        Logout from the active Signal session. This will also force a remote log-out, and thus
        require pairing on next login. For simply disconnecting the active session, look at the
        :meth:`.Session.disconnect` function.
        """
        session.signal.Logout()
