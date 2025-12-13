"""
Config contains plugin-specific configuration for Signal, and is loaded automatically by the
core configuration framework.
"""

from pathlib import Path
from typing import Optional

from slidge import global_config

# Workaround because global_config.HOME_DIR is not defined unless
# called by slidge's main(), which is a problem for tests, docs and the
# dedicated slidgnal setuptools entrypoint
try:
    DB_PATH: Optional[Path] = global_config.HOME_DIR / "slidgnal" / "signal.db"
except AttributeError:
    DB_PATH: Optional[Path] = None  # type:ignore

DB_PATH__DOC = (
    "The path to the database used for the Signal plugin. Default to "
    "${SLIDGE_HOME_DIR}/slidgnal/signal.db"
)

DB_PARAMS = "?_txlock=immediate&_foreign_keys=true&_journal_mode=WAL"
DB_PARAMS__DOC = "Additional parameters to pass to database connection string."
