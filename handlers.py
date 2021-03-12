import re
import requests
import logging

from logging import Handler, LogRecord


class Formatter(logging.Formatter):
    """
    Formatter instances are used to convert a LogRecord to text.

    Formatters need to know how a LogRecord is constructed. They are
    responsible for converting a LogRecord to (usually) a string which can
    be interpreted by either a human or an external system. The base Formatter
    allows a formatting string to be specified. If none is supplied, the
    the style-dependent default value, "%(message)s", "{message}", or
    "${message}", is used.

    The Formatter can be initialized with a format string which makes use of
    knowledge of the LogRecord attributes - e.g. the default value mentioned
    above makes use of the fact that the user's message and arguments are pre-
    formatted into a LogRecord's message attribute. Currently, the useful
    attributes in a LogRecord are described by:

    %(name)s            Name of the logger (logging channel)
    %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                        WARNING, ERROR, CRITICAL)
    %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                        "WARNING", "ERROR", "CRITICAL")
    %(pathname)s        Full pathname of the source file where the logging
                        call was issued (if available)
    %(filename)s        Filename portion of pathname
    %(module)s          Module (name portion of filename)
    %(lineno)d          Source line number where the logging call was issued
                        (if available)
    %(funcName)s        Function name
    %(created)f         Time when the LogRecord was created (time.time()
                        return value)
    %(asctime)s         Textual time when the LogRecord was created
    %(msecs)d           Millisecond portion of the creation time
    %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                        relative to the time the logging module was loaded
                        (typically at application startup time)
    %(thread)d          Thread ID (if available)
    %(threadName)s      Thread name (if available)
    %(process)d         Process ID (if available)
    %(message)s         The result of record.getMessage(), computed just as
                        the record is emitted
    """

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True):
        """
        Initialize the formatter with specified format strings.

        Initialize the formatter either with the specified format string, or a
        default as described above. Allow for specialized date formatting with
        the optional datefmt argument. If datefmt is omitted, you get an
        ISO8601-like (or RFC 3339-like) format.

        Use a style parameter of '%', '{' or '$' to specify that you want to
        use one of %-formatting, :meth:`str.format` (``{}``) formatting or
        :class:`string.Template` formatting in your format string.
        """
        super().__init__(fmt, datefmt, style, validate)

    def format(self, record):
        """
        Format the specified record as text.

        The record's attribute dictionary is used as the operand to a
        string formatting operation which yields the returned string.
        Before formatting the dictionary, a couple of preparatory steps
        are carried out. The message attribute of the record is computed
        using LogRecord.getMessage(). If the formatting string uses the
        time (as determined by a call to usesTime(), formatTime() is
        called to format the event time. If there is exception information,
        it is formatted using formatException() and appended to the message.

        This overrides the base method and removes the exception formatting
        so that it can be called separately for greater control.
        """
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        return self.formatMessage(record)

    def format_exception(self, record):
        """
        Formats the exception message, if there is one, as a code block.
        """
        s = '```'
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s + '\n```'


class SlackHandler(Handler):
    """
    Handler instances dispatch logging events to specific destinations.

    The Slack handler class builds on the base handler to emit formatted
    log records to a Slack channel.
    """
    def __init__(self, url, fmt=None, datefmt=None, style='%'):
        super().__init__()
        self.web_hook = url
        self.formats = []
        self.sformat = ''
        self.style = style
        self.tags = [
            'header',
            'section',
            'divider'
        ]

        if fmt is not None:
            self.setFormatter(fmt, datefmt, style)

    def format(self, record: LogRecord) -> list:
        """Builds a json payload that the Slack API can process"""
        blocks = []

        # Generate the main layout blocks
        for name, fmt in self.formats:
            if name in self.tags:
                blocks.append(
                    self.__gen_layout_block(
                        name, fmt.format(record)
                    ))
            else:
                t = ", ".join(self.tags)
                raise ValueError(
                    f'{name} not a valid tag name. Must be in [{t}]')

        # Generate the exception block if there is one
        if record.exc_info:
            fmt = Formatter(fmt='')
            blocks.append(
                self.__gen_layout_block(
                    'section', fmt.format_exception(record)
                )
            )

        return blocks

    def setFormatter(self, fmt: Formatter) -> None:
        """
        Allows for a more complex formatter, including tags to
        separate out formatters into blocks that Slack interprets.
        """

        # Get the format attributes
        style = self.__find_style_type(fmt._style)
        s_fmt = fmt._fmt
        d_fmt = fmt.datefmt

        # Reset the class format values
        self.sformat = s_fmt
        self.formats = []

        # Regex on the tags
        pattern = self.__pattern()

        # Check for no matches found
        if not re.search(pattern, s_fmt):
            self.formats.append(('section', fmt))
            return

        # Loop through matches
        format_tags = re.finditer(pattern, s_fmt)
        for ftag in format_tags:
            n = ftag.group(1)
            f = Formatter(ftag.group(2), d_fmt, style)
            self.formats.append((n, f))

    def emit(self, record: LogRecord) -> None:
        """
        Emits the record to Slack using an HTTP POST
        """
        layout_blocks = self.format(record)
        payload = {
            "blocks": layout_blocks
        }
        r = requests.post(self.web_hook, json=payload)
        r.raise_for_status()

    # region Private Helpers

    @staticmethod
    def __gen_layout_block(type: str, txt=None) -> dict:
        """
        Generates a layout 'block' that forms the post payload
        https://api.slack.com/reference/block-kit/blocks
        """
        # Basic block template
        block = {
            "type": type
        }

        # Add the text if not a divider
        if type != "divider":
            block["text"] = {
                "text": txt
            }

            # Add the text formatting type
            block["text"]["type"] = "plain_text" if type == "header" \
                else "mrkdwn"

        return block

    @staticmethod
    def __find_style_type(style) -> str:
        """Determines the style type and returns the symbol indicator"""
        if isinstance(style, logging.PercentStyle):
            return '%'
        elif isinstance(style, logging.StrFormatStyle):
            return '{'
        elif isinstance(style, logging.StringTemplateStyle):
            return '$'
        raise ValueError('Unknown style type {type(style)}')

    def __pattern(self) -> str:
        """Generates a regex pattern based on the tags"""
        return rf'<({"|".join(self.tags)})>(.*?)</(\1)>'

    # endregion
