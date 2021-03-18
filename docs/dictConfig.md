# SlackHandler Object
As the SlackHandler extends a standard logging.Handler, the preferred way to configure is using a dictConfig.

Create a file called config.json and place it in the root directory. Add the following to it.

```json
{
    "version": 1,
    "formatters": {
        "slack": {
            "format":       "<hdr>%(levelname)s</hdr><sect>%(asctime)s %(name)s</sect></d><s>`%(message)s`</s>",
            "datefmt":      "%Y-%m-%d %H:%M:%S"
        },
        "simple": {
            "format":       "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class":        "logging.StreamHandler",
            "level":        "DEBUG",
            "formatter":    "simple",
            "stream":       "ext://sys.stdout"
        },
        "slack": {
            "class":        "handlers.SlackHandler",
            "url":          "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
            "level":        "ERROR",
            "formatter":    "slack"
        }
    },

    "loggers": {
        "": {
            "handlers":     ["console"],
            "level":        "DEBUG",
            "propagate":    false
        },
        "__main__": {
            "handlers":     ["slack"],
            "level":        "DEBUG",
            "propagate":    true
        }
    }
}
```

## Explanation
### Version
A version must be present as a root name and the value must be 1. This is to future proof logging so that backwards incompatible changes can be handled with a version. Currently there is only one version.

### Formatters
Formatters are attached to Handlers and define how records are formatted when they are emitted. Above are examples of a simple formatter that you might use for a StreamHandler and a slack formatter that includes the layout block tags. Date formatting is optional. If it is missing, a default is used.

Constructor arguments are passed in by key word. The SlackHandler requires a url webhook on construction so it is added as a key word.

### Handlers
Handlers are attached to Loggers. They listen for logging events and handle them. One or more handlers can be attached to a logger.

### Loggers
Loggers are hierarchical with all named loggers being attached to the root logger - defined by `""`. Hierarchy is defined by name, similar to Python's module hierarchy. Names separated by dots, e.g. `ancestor.parent.child`. Propagate must be set to True for messages to flow up the heirarchy.

They can have multiple handlers so this is defined as a list.


### Notes
Both Handlers and Loggers have a level attribute. A message will only be logged if it meets the level requirement of the handler and the logger. In this way you could create an INFO level logger and two handlers, one INFO and one WARNING. All records higher than DEBUG will pass through the first handler but only those WARNING or above will go through both.

Propagated messages ignore the level of the parent Logger.



## Contact
If any information is missing, incorrect, or otherwise difficult to understand. Feel free to open an issue on the repo.