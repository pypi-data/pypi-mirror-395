import logging
import re

class DevOpsFormatter(logging.Formatter):
    error_format  = "##vso[task.logissue type=error][%(name)s]   %(message)s"
    warning_format = "##vso[task.logissue type=warning][%(name)s]   %(message)s"
    dbg_fmt  = "DBG: %(module)s: %(lineno)d: %(msg)s"
    info_format = "%(message)s"
    section_format = "%(message)s"

    def __init__(self, fmt="%(levelno)s: %(msg)s", section_info = False):
        super().__init__(fmt=fmt)
        self._section_info = section_info

    def parse_progress(self, message:str) -> str:
        """
            Parses Method for progress information
        """
        progress_pattern = re.compile(r".*PROGRESS\s\[\s*'(?P<x>\d+)\/(?P<y>\d+)'\s*\].*", re.IGNORECASE | re.MULTILINE)

        if (progress_pattern.match(message)):
            progress_match = progress_pattern.search(message)
            x = int(progress_match.group('x'))
            y = int(progress_match.group('y'))
            progress_value = round((x / y)*100)
            return  f"##vso[task.setprogress value={progress_value};]script progress\n"

        return ""

    def parse_group_start(self, message:str) -> str:
        """
            Parses if its a group start and prepends a command string to the message
        """
        start_pattern = re.compile(r".*START\s(?P<gname>.+?\s\[\s*'.*'\s*\]).*", re.IGNORECASE | re.MULTILINE)

        if (start_pattern.match(message)):
            start_match = start_pattern.search(message)
            return f"##[group]{start_match.group('gname')}\n"

        return ""

    def parse_group_end(self, message:str) -> str:
        """
            Parses if its a group end and appends a command string to the message
        """
        end_pattern = re.compile(r".*FINISHED\s.+?\s\[\s*'.*'\s*\].*", re.IGNORECASE | re.MULTILINE)

        if (end_pattern.match(message)):
            return "\n##[endgroup]"

        return ""

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        if (record.levelno == logging.INFO):
            record_message = f"{record.msg}"

            return f"{self.parse_progress(record.msg)}{self.parse_group_start(record.msg)}{record_message}{self.parse_group_end(record.msg)}"

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._fmt = DevOpsFormatter.dbg_fmt
        elif record.levelno == logging.INFO and not self._section_info:
            self._style._fmt = DevOpsFormatter.info_format

        elif record.levelno == logging.INFO and self._section_info:
            self._style._fmt = DevOpsFormatter.section_format

        elif record.levelno == logging.ERROR:
            self._style._fmt = DevOpsFormatter.error_format

        elif record.levelno == logging.WARNING:
            self._style._fmt = DevOpsFormatter.warning_format

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result

def configure_dev_ops_logger(logger: logging.Logger) -> None:
    """
        Configure logging for azure devops
    """
    snf_logger = logging.getLogger('snowflake.connector.ocsp_snowflake')
    snf_logger.disabled = True
    section_formatter = DevOpsFormatter(section_info=True)
    section_handler = logging.StreamHandler()
    section_handler.setFormatter(section_formatter)
    logger.addHandler(section_handler)
