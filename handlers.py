#!/usr/bin/env python3

import re
import time
import logging
import requests
import concurrent.futures as cf
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
    def __init__(self, url):
        super().__init__()

        # Class setup
        self.web_hook = url
        self.formats = []
        self.sformat = ''
        self.tags = [
            'header',
            'section',
            'divider'
        ]

        # Set up asynchronous posting
        self.pipeline = Pipeline()
        self.threads = cf.ThreadPoolExecutor(max_workers=1)
        self.threads.submit(self.__post_to_slack)

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

        # Parse and prepare the format string
        s_fmt = self.__parse_aliases(s_fmt)

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
        # Generate the message payload
        layout_blocks = self.format(record)
        payload = {
            "blocks": layout_blocks
        }
        # Queue the payload
        self.__queue_message(payload)

    # region Private Helpers

    def __queue_message(self, payload: dict):
        """Queues the message to be picked up by the consumer"""
        self.pipeline.queue_item(payload)

    def __post_to_slack(self, tick=1, max_tries=3):
        """
        Should be run on a separate thread.
        Consumes messages in the pipeline, sending
        them to the Slack channel.
        """
        while self.pipeline.run:
            while True:
                # Get the first in message
                payload: dict = self.pipeline.get_first_in_item()
                if payload is None:
                    break

                # Send to Slack
                r = requests.post(self.web_hook, json=payload)

                # Check for backoff and retry after the specified time
                tries = 0
                while r.status_code == 429:
                    tries += 1
                    time.sleep(r.headers.get('Retry-After', tick))
                    r = requests.post(self.web_hook, json=payload)
                    if tries >= max_tries:
                        break

                # Raise an error for these status codes
                if r.status_code in [400, 404, 410, 429, 500]:
                    r.raise_for_status()

                time.sleep(tick)

    @staticmethod
    def __gen_layout_block(type: str, txt: str) -> dict:
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

    @staticmethod
    def __parse_aliases(format_string: str) -> str:
        """
        Replaces the tags with their aliases to allow more flexible
        / shorthand tagging.
        """
        aliases = [
            ('h', 'header'),
            ('hdr', 'header'),
            ('s', 'section'),
            ('sect', 'section'),
            ('d', 'divider')
        ]

        # Find and replace aliases
        for f, r in aliases:
            format_string = re.sub(
                pattern=rf'(<[\/]?)({f})(>)',
                repl=rf'\g<1>{r}\g<3>',
                string=format_string)

        # Find and replace unclosed dividers
        format_string = re.sub(
            pattern=r'<divider>(?!</divider>)|(?<!<divider>)</divider>',
            repl=r'<divider></divider>',
            string=format_string
        )

        return format_string

    # endregion


class Pipeline():
    """
    A container that producers and consumers can
    set to and get from respectively.

    This container operates on a fifo
    (first in, first out) basis,
    """
    def __init__(self):
        self.queue = []
        self.__run = True

    def queue_item(self, item):
        """Adds an item to the queue"""
        self.queue.append(item)

    def get_first_in_item(self):
        """Returns the first-in item"""
        if len(self.queue) == 0:
            return
        item = self.queue.pop(0)
        return item

    def flag_closed(self):
        """
        Flags this queue as closed.

        This attribute does nothing by itself. It is intended to be
        a mechanism by which a consumer running on a loop can break
        the loop and end execution.
        """
        self.run = False

    @property
    def run(self):
        """Indicates this pipeline expects to continue receiving items"""
        return self.__run
