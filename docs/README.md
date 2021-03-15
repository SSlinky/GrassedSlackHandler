# SlackHandler
Python logging handler that can be configured to send messages to a Slack channel.

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/SSlinky/SlackLogger/blob/master/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8-yellow?logo=python)](https://docs.python.org/3/)
[![Slack](https://img.shields.io/badge/Slack-Webhooks-%23007a5a)](https://slack.com/intl/en-au/)

`SlackHandler` builds on the base built-in `logging.Handler` to allow logging messages to logged via HTTPS to a Slack channel.

In addition to this, the handler also builds on the `logging.Formatter` class to help build fancier Slack messages
using their [layout blocks](https://api.slack.com/messaging/composing/layouts).
The following tags are supported with aliases for brevity / readability:
* Header
  - Plain text
  - Aliases: h, hdr
* Section
  - Markdown
  - Aliases: s, sect
* Divider
  - No text support
  - Aliases: d
  - Notes: Supports opening, closing, or both tags.

Tags cannot be nested.

## How it works
The SlackHandler uses a url and improved format string to log records to a Slack channel using a webhook url.

The format string is used to generate the layout blocks in the exact same way as the base handler would but with the addition of supporting block tags in html format.

## Example format
You would like logs formatted with the level name as the header, with the time and source in one section, and the log message in another section. The sections should be separated with a divider.

``"<hdr>%(levelname)s</hdr><sect>%(asctime)s %(name)s</sect><d><s>`%(message)s`</s>"``

The above formatting string will build a stacked layout in the form of:

Block   | Format
---     | :---
Header  | `%(levelname)s`
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