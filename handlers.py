import re
import requests
import logging

from logging import Handler, LogRecord


class Formatter(logging.Formatter):
    """
    Formatter instances are used to convert a LogRecord to text.
    See base class for further information.
    """

    def format(self, record):
        """
        Format the specified record as text.

        Simplifies the base format method to remove exception
        formatting as this is handled in a separate method.
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
