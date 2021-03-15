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
            </p>
            <p>Currently only Header, Section, and Divider blocks are supported.</p>
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