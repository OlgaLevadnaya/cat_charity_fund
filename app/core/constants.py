from pathlib import Path


class UsersConstants:
    __slots__ = ()
    MIN_PASSWORD_LENGTH = 3


class LogConstants:
    __slots__ = ()
    BASE_DIR = Path(__file__).parent.parent.parent
    LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
    DT_FORMAT = '%d.%m.%Y %H:%M:%S'
    MAX_BYTES = 10 ** 6
    BACKUP_COUNT = 5


users_constants = UsersConstants()
log_constants = LogConstants()
