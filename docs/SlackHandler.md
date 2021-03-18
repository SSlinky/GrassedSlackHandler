# SlackHandler Object
A SlackHandler is an implementation of a [logging.Handler](https://docs.python.org/3/library/logging.html#handler-objects). It sends logging output to HTTPS POST in a format required by the [Slack API](https://api.slack.com/).

_class_ **SlackHandler(**_url, fmt=None, datefmt=None, style='%'_**)**

<table class="docs">
    <tr>
        <td colspan=2>
            Returns a new instance of the SlackHandler class. The url is the Slack webhook. The remaining arguments are used to create the <a href='https://docs.python.org/3/library/logging.html#logging.Formatter'>Formatter()</a> if provided.
        </td>
    </tr>
    <tr>
        <td colspan=2><b>emit(</b><em>record</em><b>)</b></td>
    </tr>
    <tr >
        <td class="indent"></td>
        <td>
            <p>
                If a formatter is specified, it is used to format the record. The record is then posted to the Slack webhook url. If exception information is present, it is formatted using traceback.print_exception() and appended to the layout blocks.
            </p>
            This method is not called directly but by a logger through an event handler.
        </td>
    </tr>
    <tr>
        <td colspan=2><b>format(</b><em>record</i><b>)</b></td>
    </tr>
    <tr >
        <td class="indent"></td>
        <td>
            <p>
                Converts a logging record into layout blocks using the <a href='https://docs.python.org/3/library/logging.html#logging.Formatter'>Formatter()</a>. The result can be interpreted by a Slack webhook endpoint. For more information, see Slack's docs for <a href='https://api.slack.com/reference/block-kit/'>block-kit</a>.
                If there is exception information, it is formatted using <a href='https://docs.python.org/3/library/logging.html#logging.Formatter.formatException'>logging.Formatter.formatException()</a> and appended to the layout blocks in a section. If stack information is available, it’s appended after the exception information, using <a href='https://docs.python.org/3/library/logging.html#logging.Formatter.formatStack'>logging.Formatter.formatStack()</a> to transform it if necessary. The exception and stack trace are formatted as a code block.
            </p>
            <p>Note: Only Header, Section, and Divider blocks are currently supported.</p>
            This method is not called directly but by the emit() method.
        </td>
    </tr>
    <tr>
        <td colspan=2><b>setFormatter(</b><em>fmt</i><b>)</b></td>
    </tr>
    <tr >
        <td class="indent"></td>
        <td>
            <p>Sets the formatter for this handler to fmt.</p>
            <p>
                This method can be called directly as part of setting up the handler but it is considered best practice to do so indirectly using dictConfig.
            </p>
            Official documentation for <a href='https://docs.python.org/3/library/logging.config.html#configuration-dictionary-schema'>logging.config.dictConfig()</a>.
        </td>
    </tr>
</table>


# Formatter Object
A Formatter is an implementation of a [logging.Formatter](https://docs.python.org/3/library/logging.html#logging.Formatter). It is responsible for converting a [LogRecord](https://docs.python.org/3/library/logging.html#logging.LogRecord) into a dict that can be sent in the payload of an http POST.

_class_ **Formatter(**_fmt=None, datefmt=None, style='%'_, _validate=True_**)**

<table class="docs">
    <tr>
        <td colspan=2>
            <p>
                Returns a new instance of the Formatter class. The instance is initialized with a format string for the message as a whole, as well as a format string for the date/time portion of a message. If no fmt is specified, <code>'%(message)s'</code> is used. If no datefmt is specified, a format is used which is described in the <a href='https://docs.python.org/3/library/logging.html#logging.Formatter.formatTime'>formatTime()</a> documentation.
            </p>
            <p>
                The style parameter can be one of <code>'%'</code>, <code>'{'</code>, or <code>'$'</code> and determines how the format string will be merged with its data.
            </p>
            If <code>validate</code> is true, incorrect or mismatched style and fmt will raise a <code>ValueError</code>. For example: <code>Formatter('%(asctime)s - %(message)s', style='{')</code> will raise an exception because style is <code>{</code> but fmt is written in <code>%</code> style.
        </td>
    </tr>
    <tr>
        <td colspan=2><b>format(</b><em>record</em><b>)</b></td>
    </tr>
    <tr >
        <td class="indent"></td>
        <td>
            <p>
                If a formatter is specified, it is used to format the record. If exception information is present, it is formatted using <a href='https://docs.python.org/3/library/traceback.html#traceback.print_exception'>traceback.print_exception()</a> and appended to the layout blocks in a Section.
            </p>
            This method is not called directly but by a logging event through the SlackHandler.emit() method.
        </td>
    </tr>
    <tr>
        <td colspan=2><b>format_exception(</b><em>record</em><b>)</b></td>
    </tr>
    <tr >
        <td class="indent"></td>
        <td>
            <p>
                Formats the exception message, if there is one, as a code block and wraps it in a Section.
            </p>
            This method is not called directly but by a logging event through the SlackHandler.format() method.
        </td>
    </tr>
</table>
