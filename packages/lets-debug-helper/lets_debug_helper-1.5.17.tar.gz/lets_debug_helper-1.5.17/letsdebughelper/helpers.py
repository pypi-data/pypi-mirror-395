#!/usr/bin/env python3
import argparse
import re

from typing import Any


class ValidateArgRegex:
    """
    Supports checking if arg matches install, domain, order_id, or IPv6/IPv4 pattern
    """

    patterns = {
        'domain': re.compile(r'^([*]\.)?[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    }

    def __init__(self, argtype: Any) -> None:
        if argtype not in self.patterns:
            raise KeyError('{} is not a supported argument pattern, choose from:'
                           ' {}'.format(argtype, ','.join(self.patterns)))
        self._argtype = argtype
        self._pattern = self.patterns[argtype]

    def __call__(self, value: Any) -> Any:
        if not self._pattern.match(value):
            raise argparse.ArgumentTypeError("'{}' is not a valid argument - does not match {} pattern".format(
                value, self._argtype))
        return value
