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

## Documentation
[Read the docs](https://sslinky.github.io/SlackLogger/#/) for usage and examples.

Check out Slack's documentation for [Incoming Webhooks](https://api.slack.com/messaging/webhooks) to learn how to set up a Slack app that can handle the incoming messages.

## Licence
Released under [MIT](/LICENCE) by [Sam Vanderslink](https://github.com/SSlinky).
Free to modify and reuse.