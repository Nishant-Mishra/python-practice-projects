#!/usr/bin/env python3
from  enum import Enum


__all__ = ["Player"]


class Player(Enum):
    COMPUTER = "Computer"
    USER = "You"

