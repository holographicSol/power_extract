""" Written by Benjamin Jack Cullen """

from datetime import datetime
import re
import random
import string
import variable_strings


def get_dt() -> str:
    return str(datetime.now()).replace(':', '-').replace('.', '-').replace(' ', '_')


def randStr(chars=string.ascii_uppercase + string.digits, n=32) -> str:
    return ''.join(random.choice(chars) for _ in range(n))


def sub_str(_buffer: bytes) -> str:
    return re.sub(variable_strings.digi_str, '', str(_buffer))
