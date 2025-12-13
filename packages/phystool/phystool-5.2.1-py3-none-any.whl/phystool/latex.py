import re
import shutil
import subprocess

from abc import ABC
from logging import getLogger
from pathlib import Path
from typing import Match, Pattern, Iterator

from phystool.helper import ContextIterator

logger = getLogger(__name__)


class LogFileMessage(ABC):
    """Helper class that stores log file messages."""

    PATTERN: Pattern
    VERBOSE = False

    @classmethod
    def toggle_verbose_mode(cls) -> None:
        cls.VERBOSE = not cls.VERBOSE

    def __init__(self, match: Match[str], context: list[str], tex_file: Path):
        self._tex_file = tex_file
        self._match = match
        self._context = context
        self.ignore = False
        if self.VERBOSE:
            self.message = LogFileMessage._get_message(self)
        else:
            self.message = f"{self._get_message().strip()}\n    -> {self._tex_file}"

    def __str__(self) -> str:
        return self.message

    def __bool__(self) -> bool:
        return bool(self.message)

    def _get_message(self) -> str:
        """Returns the formatted log message"""
        return (
            "Context:\n"
            + "".join([f"{i:>2}: {context}" for i, context in enumerate(self._context)])
            + "\nRegex match groups:\n"
            + "\n".join([f"{i+1:>2}: {m}" for i, m in enumerate(self._match.groups())])
        )


class BadBoxMessage(LogFileMessage):
    PATTERN = re.compile(
        r"^(Over|Under)full "
        r"\\([hv])box "
        r"\((?:badness (\d+)|(\d+(?:\.\d+)?pt) too \w+)\) (?:"
        r"(?:(?:in paragraph|in alignment|detected) "
        r"(?:at lines (\d+)--(\d+)|at line (\d+)))"
        r"|(?:has occurred while [\\]output is active [\[](\d+)?[\]]))"
    )
    # 0 - Whole match (line)
    # 1 - Type (Over|Under)
    # 2 - Direction ([hv])
    # 3 - Underfull box badness (badness (\d+))
    # 4 - Overfull box over size (\d+(\.\d+)?pt too \w+)
    # 5 - Multi-line start line (at lines (\d+)--)
    # 6 - Multi-line end line (--(d+))
    # 7 - Single line (at line (\d+))

    def _get_message(self) -> str:
        l1, l2 = (
            (self._match.group(7), self._match.group(7))
            if self._match.group(7) is not None
            else (self._match.group(5), self._match.group(6))
        )
        return "[B]: {}-{} {} {}{}".format(
            l1 if l1 else "?",
            l2 if l2 else "?",
            self._match.group(2),
            "+" if self._match.group(1) == "Over" else "-",
            self._match.group(3) or self._match.group(4),
        )


class InfoMessage(LogFileMessage):
    PATTERN = re.compile(
        r"^((?:La|pdf)TeX3?|Package|Class)(?: (\S+))? [iI]nfo(?: \(([\\]?\w+)\))?: (.*)"
    )
    # 0 - Whole match (line)
    # 1 - Type ((?:La|pdf)TeX3?|Package|Class)
    # 2 - Package or Class name (\w*)
    # 3 - extra
    # 4 - message (.*)

    def _get_message(self) -> str:
        if self._match.group(3):
            return super()._get_message()

        out = "[I{}] {}"
        tmp = self._match.group(4).strip()
        if self._match.group(1) == "LaTeX":
            return out.format(f":{self._match.group(2) or 'LaTeX'}", tmp)

        if package := self._match.group(2):
            return out.format(f":{package=}", tmp)

        return super()._get_message()


class WarningMessage(LogFileMessage):
    PATTERN = re.compile(
        r"^((?:La|pdf)TeX3?|Package|Class)(?: (\S+))? [wW]arning(?: \(([\\]?\w+)\))?: (.*)"
    )
    # 0 - Whole match (line)
    # 1 - Type ((?:La|pdf)TeX3?|Package|Class)
    # 2 - Package or Class name (\w*)
    # 3 - extra
    # 4 - message (.*)

    should_recompile: bool

    class RecompilationRequired(Exception):
        ERRNO_MESSAGE = (20, "Recompilation required")

    def _get_message(self) -> str:
        out = "[W{}] {}"
        tmp = self._match.group(4)
        self.should_recompile = "rerun" in tmp.lower()
        if package := self._match.group(2):
            self.ignore = (
                package == "hyperref" and "Token not allowed in a PDF string" in tmp
            )
            out = out.format(f":{package=}", tmp) + "\n"
            loffset = len(package) + 15
            i = 7
            while line := self._context[i].lstrip():
                if tmp := line.replace(f"({package})", "").lstrip():
                    out += loffset * " " + tmp
                i += 1

            return out

        if self._match.group(1) == "pdfTeX":
            return out.format(":pdfTeX", tmp)

        if self._match.group(1) == "LaTeX":
            component = ":" + (self._match.group(2) or "LaTeX")
            if "float specifier changed" in tmp:
                for line in self._context[:6]:
                    if line.startswith("<use"):
                        out += f"\n    {line[1:-2]}\n"
                        break
                return out.format(component, tmp)

            tmp += " " + self._context[7].strip()
            return out.format(component, tmp)

        return super()._get_message()


class ErrorMessage(LogFileMessage):
    PATTERN = re.compile(
        r"^(?:! ?((?:La|pdf)TeX3?|Package|Class)(?: (\S+))? [eE]rror(?: \(([\\]?\w+)\))?: (.*)|! (.*))"
    )
    # 0 - Whole match (line)
    # 1 - Type ((?:La|pdf)TeX3?|Package|Class)
    # 2 - Package or Class (\w+)
    # 3 - extra (\(([\\]\w+)\))
    # 4 - Error message for typed error (.*)
    # 5 - TeX error message (.*)

    _EXTRA_CONTEXT_PACKAGE = {
        "geometry": False,
        "cmd": True,
        "amsmath": True,
        "keyval": True,
        "tikz": True,
        "phys": True,
        "siunitx": True,
        "pdftex": True,
        "pgf": True,  # also match pgfkeys
    }
    _EXTRA_CONTEXT_LATEX = {
        "PDF inclusion": False,
        "Control sequence": True,
        "There's no line here to end": True,
        "invalid in math mode": True,
        "Environment": True,
        r"ended by \end{": True,
        "Can be used only in preamble.": True,
        r"Something's wrong": True,
        "File": True,
        r"Missing \begin{document}": True,
        "only in math mode": True,
        "Unknown float option": True,
        "Illegal character in array arg.": True,
        "is unknown and is being ignored.": True,
        "Option clash": True,
        "Unicode character": True,
        "caption outside float.": True,
        "Not in outer par mode.": True,
        "Bad math environment delimiter.": True,
        r"Lonely \item": True,
    }
    _EXTRA_CONTEXT_NONE = {
        "File ended while scanning": False,
        "Undefined control sequence": True,
        "Misplaced ": True,
        r"Extra }, or forgotten ": True,
        "Paragraph ended ": True,
        "Argument of ": True,
        "Extra alignment tab has been changed": True,
        r"Too many }'s": True,
        "Please use": True,
        "Missing ": True,
        "There's no line here to end": True,
        "Double subscript.": True,
        "Display math should end with $$.": True,
        "Package PGF Math Error": True,
        "Illegal parameter number in definition": False,
        "Illegal unit of measure": True,
        r"You can't use `\eqno'": True,
        r"Use of \??? doesn't match its definition.": True,
    }

    def _get_full_error_line(self, out: str, replace: str) -> str:
        idx = 7
        while line := self._context[idx].strip():
            if tmp := line.replace(f"({replace})", "").strip():
                if tmp.startswith("==> Fatal"):
                    return out
                out += " " + tmp
            idx += 1
        return out

    def _get_message(self) -> str:
        out = "[E{}] {}"
        tmp = self._match.group(4)
        if package := self._match.group(2):
            out = out.format(f":{package=}", self._get_full_error_line(tmp, package))
            tmp = package
            extra_context = self._EXTRA_CONTEXT_PACKAGE
        elif error_type := self._match.group(1):
            out = out.format(
                f":{error_type}", self._get_full_error_line(tmp, error_type)
            )
            extra_context = self._EXTRA_CONTEXT_LATEX
        else:
            tmp = self._match.group(5)
            out = out.format("", tmp)
            extra_context = self._EXTRA_CONTEXT_NONE

        for txt, extra in extra_context.items():
            if txt in tmp:
                if extra:
                    i = 7
                    while not self._context[i].startswith("l."):
                        i += 1
                    out += "\n    " + "    ".join(self._context[i : i + 2])
                return out

        return super()._get_message()


class Latex3Message(LogFileMessage):
    PATTERN = re.compile(r"^> (.*)")

    def _get_message(self) -> str:
        line = self._match.group(1)
        i = 7
        n = len(self._context)
        if not line:  # to catch long lines
            line = self._context[i]
            i += 1
        while i < n and self._context[i][0] != "<":
            line += self._context[i]
            i += 1

        if i == n:
            # it sometimes happens that a '>' is the first character of a line
            # and that it's not related to a Latex3Message. This test is an
            # attempt to get rid of those cases.
            self.ignore = True

        return f"[S:LaTeX3] {line}"


class LogMessageList[T: LogFileMessage]:
    def __init__(self, klass: type[T]):
        self._klass = klass
        self._message_list: list[T] = []

    def __bool__(self) -> bool:
        return bool(self._message_list)

    def __getitem__(self, idx: int) -> T:
        return self._message_list[idx]

    def __iter__(self) -> Iterator[T]:
        for message in self._message_list:
            yield message

    def add(
        self, line: str, lines_iterable: ContextIterator[str], tex_file: Path
    ) -> bool:
        match = self._klass.PATTERN.match(line)
        if match is None:
            return False

        message = self._klass(match, lines_iterable.get(), tex_file)
        if not message.ignore:
            self._message_list.append(message)
        return True

    def as_log(self) -> None:
        for message in self._message_list:
            logger.info(message)

    def stats(self) -> str:
        if n := len(self._message_list):
            return f"{self._klass.__name__}: {n}"
        else:
            return ""


class LatexLogParser:
    """
    LatexLogParser parses a LaTeX log file to generate lists of errors,
    warnings, infos and bad boxes. Each message is stored as a LogFileMessage
    in the corresponding list.

    To properly parse the log file, 'texmf.cnf' must be configured so that filenames
    are written on single line ('max_print_line=1000')

    :param texfile: LaTeX file for which the log should be parsed
    :param message_types: selection of LogfileMessage to parse and display
    """

    # should match the last .tex file of a line
    TEX_FILE_PATTERN = re.compile(r".*\((\/.*\.(tex|cls|sty))[\s)$]")

    def __init__(
        self,
        texfile: Path,
        message_types: list = [
            BadBoxMessage,
            InfoMessage,
            WarningMessage,
            ErrorMessage,
            Latex3Message,
        ],
    ):
        self._logfile = texfile.with_suffix(".log")
        self._message_map = {mt: LogMessageList(mt) for mt in message_types}

    def _extract_texfile_name_from_line(self, line: str) -> Path | None:
        if tf := self.TEX_FILE_PATTERN.match(line):
            out = Path(tf.group(1)).resolve()
            if out.is_relative_to(Path.home()) or out.is_relative_to(Path("/tmp")):
                return out
        return None

    def process(self) -> None:
        """
        Main method that parses each line of the LaTeX logfile and checks for
        a matching pattern. When a pattern is matched, a new message is created
        and added to the correct LogMessageList according to its type.
        """
        tex_file = None
        with self._logfile.open(encoding="utf-8", errors="replace") as lf:
            lines_iterable = ContextIterator(lf, before=6, after=10)
            for line in lines_iterable:
                if not line:
                    continue

                if tmp_file := self._extract_texfile_name_from_line(line):
                    tex_file = tmp_file
                elif (
                    tex_file and "==> Fatal" not in line and "Emergency" not in line
                ):  # fully ignore these errors
                    for message_list in self._message_map.values():
                        if message_list.add(line, lines_iterable, tex_file):
                            break

    def should_recompile(self) -> bool:
        """True if any WarningMessage is flagged as 'should_recompile'"""
        for message in self.warning():
            if message.should_recompile:
                return True
        return False

    def as_log(self) -> None:
        """Logs all messages sorted by type and add a general summary"""
        out = []
        for message_list in self._message_map.values():
            message_list.as_log()
            if tmp := message_list.stats():
                out.append(tmp)

        if out:
            logger.info(", ".join(out))

    def as_text(self) -> str:
        """Returns a concatenated string of all messages sorted by type"""
        return "\n".join(
            [
                message.message
                for message_list in self._message_map.values()
                for message in message_list
            ]
        )

    def warning(self) -> LogMessageList[WarningMessage]:
        """Returns WarningMessage"""
        return self._message_map[WarningMessage]

    def error(self) -> LogMessageList:
        """Returns ErrorMessage"""
        return self._message_map[ErrorMessage]

    def latex3(self) -> LogMessageList:
        """Returns Latex3Message"""
        return self._message_map[Latex3Message]


class PdfLatex:
    class CompilationError(Exception):
        ERRNO_MESSAGE = (66, "Latex compilation error")

    class PdfCropError(Exception):
        ERRNO_MESSAGE = (64, "PDF crop error")

        def __init__(self, error):
            self.error = error

    class PdfToPngError(Exception):
        ERRNO_MESSAGE = (63, "PDF to PNG error")

    class MoveError(Exception):
        ERRNO_MESSAGE = (62, "Move error")

        def __init__(self, source: Path, dest: Path):
            super().__init__(f"Moving {source} to {dest} failed")

        @property
        def error(self) -> str:
            return self.args[0]

    @classmethod
    def output(cls, as_string: str) -> Path:
        fname = Path(as_string).resolve().with_suffix(".pdf")
        if fname.parent.exists():
            return fname
        raise ValueError

    def __init__(self, fullname: Path):
        self._fullname = fullname.with_suffix(".tex")

    def full_compile(self, dest: Path | None, can_recompile: bool) -> bool:
        try:
            self.compile()

            llp = LatexLogParser(self._fullname, [WarningMessage])
            llp.process()
            llp.as_log()
            if llp.should_recompile() and can_recompile:
                logger.info("Automatic recompilation triggered")
                self.compile()
                llp = LatexLogParser(self._fullname, [WarningMessage])
                llp.process()
                llp.as_log()
                logger.info("Automatic recompilation successful")

            self.move_pdf(dest)
            return True
        except self.CompilationError:
            llp = LatexLogParser(self._fullname, [Latex3Message, ErrorMessage])
            llp.process()
            llp.as_log()
        except self.MoveError:
            logger.error(f"Moving pdf to {dest} failed")
        return False

    def compile(self, env: dict[str, str] | None = None) -> None:
        try:
            subprocess.run(
                self.compilation_command(),
                capture_output=True,
                check=True,
                env=env,
            )
            logger.debug(f"{self._fullname.name}: pdflatex successful")
        except subprocess.CalledProcessError:
            logger.error(f"{self._fullname.name}: pdflatex failed")
            raise self.CompilationError

    def compilation_command(self) -> list[str]:
        return [
            "pdflatex",
            "-shell-escape",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-output-directory={self._fullname.parent}",
            str(self._fullname),
        ]

    def convert_pdf_to_png(
        self, dest_files: list[Path] = [], cropped: bool = False
    ) -> None:
        if cropped:
            try:
                subprocess.check_output(
                    [
                        "pdfcrop",
                        self._fullname.with_suffix(".pdf"),
                        self._fullname.with_suffix(".pdf"),
                    ],
                    stderr=subprocess.STDOUT,
                )
                logger.debug(f"{self._fullname.name} PDF crop successful")
            except subprocess.CalledProcessError as e:
                logger.error(f"{self._fullname.name}: PDF crop failed")
                raise self.PdfCropError(e.output)

        try:
            """
            If the conversion fails, edit /etc/ImageMagick-?/policy.xml' to
            allow a conversion from PDF to PNG:
                <policy domain="coder" rights="read" pattern="PDF" />
            """
            subprocess.check_output(
                [
                    "convert",
                    "-density",
                    "150",
                    self._fullname.with_suffix(".pdf"),
                    "-quality",
                    "90",
                    self._fullname.with_suffix(".png"),
                ],
                stderr=subprocess.STDOUT,
            )
            logger.debug(f"{self._fullname.name}: PDF to PNG successful")
        except subprocess.CalledProcessError as e:
            logger.error(f"{self._fullname.name}: PDF to PNG failed")
            raise self.PdfToPngError(e.output)

        if dest_files:
            n = len(dest_files)
            if n == 1:
                source_files = [self._fullname.with_suffix(".png")]
            else:
                source_files = [
                    self._fullname.parent / f"{self._fullname.stem}-{i}.png"
                    for i in range(n)
                ]

            for source, dest in zip(source_files, dest_files):
                try:
                    shutil.move(source, dest)
                except Exception:
                    raise self.MoveError(source, dest)

    def clean(self, extensions: list[str]) -> None:
        logger.debug(f"Remove {self._fullname.stem} [{','.join(extensions)}]")
        for ext in extensions:
            self._fullname.with_suffix(ext).unlink(missing_ok=True)

    def move_pdf(self, dest: Path | None) -> None:
        if not dest and self._fullname.is_symlink():
            dest = self._fullname.resolve().with_suffix(".pdf")
        if dest:
            try:
                shutil.move(self._fullname.with_suffix(".pdf"), dest)
            except Exception:
                raise self.MoveError(self._fullname.with_suffix(".pdf"), dest)
