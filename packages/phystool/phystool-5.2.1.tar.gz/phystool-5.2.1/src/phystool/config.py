import datetime
import locale
import re
import sys

from configparser import ConfigParser, SectionProxy
from enum import IntEnum, auto
from logging import critical
from logging.config import dictConfig
from pathlib import Path
from uuid import UUID, uuid4


try:
    locale.setlocale(locale.LC_ALL, "fr_CH.UTF-8")
    # readthedocs isn't happy with this call
except locale.Error:
    pass


def _ensure_exists(path: Path) -> Path:
    if not path.exists():
        path.mkdir()
    return path


class MyConfig:
    class Status(IntEnum):
        # TODO: write tests for all status
        READY = auto()
        MISSING_DB_CONF = auto()
        MISSING_DB = auto()
        MISSING_DB_DIR = auto()
        MISSING_KEY_IN_CONFIGURATION_FILE = auto()
        MISSING_PDB_TYPE = auto()
        MISSING_DOCUMENTCLASS_FILE = auto()

    def __init__(self) -> None:
        if (Path(__file__).parents[2] / "pyproject.toml").exists():
            # DEV MODE
            config_dir = Path(__file__).parents[1] / "dev"
            self.DEFAULT_LOGLEVEL = "DEBUG"
        else:
            config_dir = Path.home() / ".phystool"
            self.DEFAULT_LOGLEVEL = "INFO"

        self._config_file = config_dir / "phystool.conf"
        if not self._config_file.exists():
            conf = self._generate_default_config_file()
        else:
            conf = ConfigParser()
            conf.read(self._config_file)

        config_dir = self._config_file.parent
        self.DB_NAME = conf["general"]["db"]
        self.LOGFILE_PATH = config_dir / "phystool.log"
        self.AUX_DIR = _ensure_exists(config_dir / "texaux")
        self.EDITOR_CMD = conf["general"]["editor"].split(" ")
        _today = datetime.date.today()
        if _today.month > 7:
            self.CURRENT_SCOLAR_YEAR = _today.year
        else:
            self.CURRENT_SCOLAR_YEAR = _today.year - 1

        if ev_path := conf["general"].get("evaluation", None):
            self.EVALUATION_PATH = Path(ev_path)
        else:
            self.EVALUATION_PATH = config_dir / "evaluation.json"

        match theme := conf["general"].get("theme", "dark"):
            case "dark":
                self.DELTA_THEME = _DELTA_THEME_DARK + _DELTA_THEME_COMMON
            case "light":
                self.DELTA_THEME = _DELTA_THEME_LIGHT + _DELTA_THEME_COMMON
            case _:
                self.DELTA_THEME = theme

        self._dbs = {
            section_name[3:]: DBConf(section_name[3:], conf[section_name])
            for section_name in conf.sections()
            if section_name.startswith("db=")
        }
        self.db: DBConf

    def setup_db(self) -> Status:
        try:
            self.db = self._dbs[self.DB_NAME]
        except KeyError:
            return self.Status.MISSING_DB
        return self.db.configure()

    def get_db_list(self) -> list[str]:
        return list(self._dbs.keys())

    def new_pdb_filename(self) -> str:
        return str((self.db.DB_DIR / str(uuid4())).with_suffix(".tex"))

    def _generate_default_config_file(self) -> ConfigParser:
        conf = ConfigParser()
        conf["general"] = {
            "db": "tuto",
            "editor": "rxvt-unicode -e vim",
            "delta": "dark",
        }
        conf["db=tuto"] = {
            "path": "~/tuto_db",
            "repo": "git@bitbucket.org:jdufour/physdb_dev.git",
            "editable": "false",
        }
        with self._config_file.open("w") as config_file:
            conf.write(config_file)

        return conf


class DBConf:
    def __init__(self, name: str, section: SectionProxy):
        self.NAME = name
        self.DB_DIR = Path(section["path"]).expanduser()
        self.REMOTE_URL = section["repo"]
        self.EDITABLE = section.get("editable", False)
        self.SHARED = section.get("shared", False)
        self.PHYSTEX = self.DB_DIR / "phystex"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.DB_DIR})"

    def configure(self) -> MyConfig.Status:
        config_file = self.DB_DIR / "0_physdb.conf"
        if not config_file.exists():
            if not self.DB_DIR.exists():
                return MyConfig.Status.MISSING_DB_DIR
            return MyConfig.Status.MISSING_DB_CONF

        try:
            conf = ConfigParser()
            conf.read(config_file)
            self.PDB_TYPES = {
                section_name[9:]: (
                    re.compile(conf[section_name]["pattern"]),
                    conf[section_name].getboolean("standalone", False),
                )
                for section_name in sorted(conf.sections())
                if section_name.startswith("pdb-type=")
            }
            if not self.PDB_TYPES:
                return MyConfig.Status.MISSING_PDB_TYPE

            documentclass = conf["phystool"]["auto_latex"]
            if not (self.DB_DIR / "phystex" / f"{documentclass}.cls").exists():
                return MyConfig.Status.MISSING_DOCUMENTCLASS_FILE

            self._template = (
                f"\\documentclass{{{{{documentclass}}}}}\n"
                f"\\PdbSetDBPath{{{{{self.DB_DIR}/}}}}\n"
                "\\begin{{document}}\n"
                "    \\PdbInclude{{{uuid}}}\n"
                "\\end{{document}}"
            )
        except KeyError:
            return MyConfig.Status.MISSING_KEY_IN_CONFIGURATION_FILE
        return MyConfig.Status.READY

    def template(self, uuid: UUID) -> str:
        return self._template.format(uuid=uuid)


_DELTA_THEME_COMMON = (
    " --file-decoration-style 'darkgoldenrod overline'"
    " --file-style 'darkgoldenrod bold'"
    " --file-added-label '[+]'"
    " --file-copied-label '[C]'"
    " --file-modified-label '[*]'"
    " --file-removed-label '[-]'"
    " --file-renamed-label '[→]'"
    " --line-numbers"
    " --line-numbers-left-format '{nm:>1}┊'"
    " --line-numbers-right-format '{np:>1}┊'"
    " --no-gitconfig"
    " --side-by-side"
    " --width 200"
    " --zero-style 'syntax'"
)
_DELTA_THEME_LIGHT = (
    " --hunk-header-decoration-style 'none'"
    " --hunk-header-file-style 'darkgoldenrod'"
    " --hunk-header-line-number-style 'orange'"
    " --hunk-header-style 'file line-number purple'"
    " --light"
    " --line-numbers-left-style 'darkgrey'"
    " --line-numbers-minus-style 'red'"
    " --line-numbers-plus-style 'green'"
    " --line-numbers-right-style 'orange'"
    " --line-numbers-zero-style 'darkgray'"
    " --minus-emph-style 'black tomato underline'"
    " --minus-empty-line-marker-style 'normal orangered'"
    " --minus-style 'syntax lightpink'"
    " --plus-emph-style 'black limegreen underline'"
    " --plus-empty-line-marker-style 'normal forestgreen'"
    " --plus-style 'syntax lightgreen'"
    " --syntax-theme 'Coldark-Cold'"
    " --whitespace-error-style 'black white'"
)
_DELTA_THEME_DARK = (
    " --dark"
    " --hunk-header-style 'syntax bold italic 237'"
    " --line-numbers-left-style 'red'"
    " --line-numbers-minus-style 'red bold'"
    " --line-numbers-plus-style 'green bold'"
    " --line-numbers-right-style 'green'"
    " --line-numbers-zero-style '\"#545474\" italic'"
    " --minus-emph-style 'normal \"#80002a\"'"
    " --minus-style 'normal \"#5e0000\"'"
    " --plus-emph-style 'syntax bold \"#007e5e\"'"
    " --plus-style 'syntax \"#003500\"'"
    " --syntax-theme 'OneHalfDark'"
    " --whitespace-error-style '\"#80002a\" reverse'"
)

config = MyConfig()


########################################################################
# LOGGER ###############################################################
def _handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = _handle_uncaught_exception

LOGGER_BOTH = {
    "handlers": ["default", "file_handler"],
    "level": config.DEFAULT_LOGLEVEL,
    "propagate": False,
}
LOGGER_FILE = {
    "handlers": ["file_handler"],
    "level": config.DEFAULT_LOGLEVEL,
    "propagate": False,
}
LOGGER_ALCHEMY = {
    "handlers": ["file_handler"],
    "level": "WARN",
    "propagate": False,
}
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s %(lineno)d: %(message)s"
        },
        "minimal": {"format": "%(levelname)-.3s| %(message)s"},
    },
    "handlers": {
        "default": {
            "level": config.DEFAULT_LOGLEVEL,
            "formatter": "minimal",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "file_handler": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": config.LOGFILE_PATH,
            "mode": "a",
            "maxBytes": 200000,
            "backupCount": 2,
        },
    },
    "loggers": {
        "__main__": LOGGER_BOTH,
        "helper": LOGGER_BOTH,
        "latex": LOGGER_BOTH,
        "pdbfile": LOGGER_BOTH,
        "physgit": LOGGER_BOTH,
        "physql": LOGGER_FILE,
        "phystool": LOGGER_BOTH,
        "qt": LOGGER_FILE,
        "sqlalchemy": LOGGER_ALCHEMY,
        "tags": LOGGER_BOTH,
    },
}

# TODO : fix sql log verbosity in production
dictConfig(LOGGING_CONFIG)
