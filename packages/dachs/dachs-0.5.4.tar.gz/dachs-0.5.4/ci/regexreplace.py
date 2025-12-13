import re

from jinja2.ext import Extension


# Custom filter method
def regex_replace(s, find, replace):
    """A non-optimal implementation of a regex filter"""
    return re.sub(find, replace, s)


class RegExReplace(Extension):
    # a set of names that trigger the extension.
    tags = {"regex_replace"}

    def __init__(self, environment):
        super().__init__(environment)

        # add the defaults to the environment
        environment.filters["regex_replace"] = regex_replace
