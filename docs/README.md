# SlackLogger
Python Logger that can be configured to send messages to a Slack channel.

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/SSlinky/VBA-ExtendedDictionary/blob/master/README.md#license)
[![Python](https://img.shields.io/badge/Python-3.8-yellow?logo=python)](https://docs.python.org/3/)
[![Slack](https://img.shields.io/badge/Slack-Webhooks-%23007a5a)](https://slack.com/intl/en-au/)

`SlackLogger` builds on the base built-in `logging.Handler` to allow logging messages to logged via HTTPS to a Slack channel.

In addition to this, the handler also builds on the `logging.Formatter` class to help build fancier Slack messages
using their [layout blocks](https://api.slack.com/messaging/composing/layouts).
The following tags are supported:
* Header: plain text
* Section: supports markdown
* Divider: no text support

All tags require an open and a close tag. Tags cannot be nested.

## How it works
You would like logs formatted with the level name as the header, with the time and source in one section, and the log message in another section.
The sections should be separated with a divider.

``"<header>%(levelname)s</header><section>%(asctime)s %(name)s</section><divider></divider><section>`%(message)s`</section>"``

The above formatting string will build a stacked layout in the form of:

Block | Format
--- | :---
Header | `%(levelname)s`
Section | `%(asctime)s %(name)s`
Divider |
Section | `` `%(message)s` ``


The result for a call to `log.critical("You had better go and get mum!")` could look like this:

```json
{
    "blocks": [
        {
            "type": "header",
            "text": {
                "text": "CRITICAL",
                "type": "plain_text"
            }
        },
        {
            "type": "section",
            "text": {
                "text": "2021-03-10 16:57:06 __main__",
                "type": "mrkdwn"
            }
        },
        { "type": "divider" },
        {
            "type": "code",
            "text": {
                "text": "`You had better go and get mum!`",
                "type": "mrkdwn"
            }
        }
    ]
}
 ```