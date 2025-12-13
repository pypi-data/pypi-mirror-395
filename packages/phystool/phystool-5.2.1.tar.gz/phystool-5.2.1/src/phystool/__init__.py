from logging import getLogger

from phystool.config import config

logger = getLogger(__name__)


def phystool() -> None:
    """Run the command line interface"""
    from phystool.cli import get_parser

    status = config.setup_db()
    if status != config.Status.READY:
        _recover(status, True)

    args = get_parser().parse_args()
    args.func(args)


def physnoob() -> None:
    """Run the graphical user interface"""
    from phystool.qt import PhysQt

    status = config.setup_db()
    if status != config.Status.READY:
        _recover(status, False)

    qt = PhysQt()
    qt.exec()


def _recover(status: int, in_terminal: bool) -> None:
    from phystool.helper import terminal_yes_no
    from phystool.physgit import is_valid_git_remote, clone_git_repository

    match status:
        case config.Status.MISSING_DB:
            logger.error(f"Database '{config.DB_NAME}' is not configured")
        case config.Status.MISSING_DB_DIR:
            logger.error(f"Database '{config.DB_NAME}' not found ({config.db.DB_DIR})")
            if in_terminal:
                if not is_valid_git_remote(config.db.REMOTE_URL):
                    logger.info(f"Invalid remote url {config.db.REMOTE_URL}")
                    return
                if terminal_yes_no(f"Clone from '{config.db.REMOTE_URL}'?"):
                    clone_git_repository(config.db.REMOTE_URL, config.db.DB_DIR)
        case config.Status.MISSING_KEY_IN_CONFIGURATION_FILE:
            logger.error("The configuration file is not valid")
        case config.Status.MISSING_PDB_TYPE:
            logger.error("The configuration file doesn't define valid PDBType")

    if config.setup_db() != config.Status.READY:
        raise RuntimeError("The initialisation and automatic recovery attempt failed")
