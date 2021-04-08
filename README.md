# Grassed Logging Handler
Python logging handler that can be configured to send messages to a Slack channel.

[![License](https://img.shields.io/badge/License-GPL3-blue.svg)](https://github.com/SSlinky/VBA-ExtendedDictionary/blob/master/README.md#license)
[![Python](https://img.shields.io/badge/Python-3.8-yellow?logo=python)](https://docs.python.org/3/)
[![Slack](https://img.shields.io/badge/Slack-Webhooks-%23007a5a)](https://slack.com/intl/en-au/)

`SlackLogger` builds on the base built-in `logging.Handler` to allow logging messages to logged via HTTPS to a Slack channel.

In addition to this, the handler also builds on the `logging.Formatter` class to help build fancier Slack messages
using their [layout blocks](https://api.slack.com/messaging/composing/layouts).
The following tags are supported:
* Header: plain text
* Section: supports markdown
* Divider: no text support

## Getting Started
The package can be installed from the PyPi repository with `pip install grassed` or cloned from the [git repo](https://github.com/SSlinky/GrassedSlackHandler).

## Documentation
[Read the docs](https://sslinky.github.io/SlackLogger/#/) for usage and examples.

Check out Slack's documentation for [Incoming Webhooks](https://api.slack.com/messaging/webhooks) to learn how to set up a Slack app that can handle the incoming messages.

## Message Rate Limits
SlackHandler is designed to log important messages to a place where people can view them immediately and respond.
Note that Slack imposes message rate limits which SlackHandler respects.

## Licence
Released under [GPLv3](/LICENCE) by [Sam Vanderslink](https://github.com/SSlinky).
Free to modify and reuse.
