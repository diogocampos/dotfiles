#!/usr/bin/env python3

import argparse
import datetime as dt
from random import random
import re
import sys


IMAWA = '今は'
REIJI = '零時'
SHOUGO = '正午'
GOZEN = '午前'
GOGO = '午後'
JI = '時'
FUN = '分'
HAN = '半'
CHOUDO = 'ちょうど'
GORO = 'ごろ'
DESU = 'です。'


def main(argv):
    args = parse_args(argv)

    time = args.time or dt.datetime.now().time()
    phrase = generate_phrase(time.hour, time.minute)

    if not sys.stdout.isatty(): print(phrase, file=sys.stderr)
    print(phrase)


def parse_args(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('time', nargs='?', type=hhmm,
        help='a time in HH:MM format to use instead of the current time')

    return parser.parse_args(argv[1:])


def hhmm(string):
    try:
        assert re.match(r'^\d\d?:\d\d$', string)
        hh, mm = map(int, string.split(':'))
        return dt.time(hh, mm)
    except:
        raise argparse.ArgumentTypeError(f'{string!r} is not a valid time')


def generate_phrase(hour, minute):
    imawa = IMAWA if coinflip() else ''

    choudo = CHOUDO if (minute == 0 or minute == 30) and coinflip() else ''

    goro = ''
    rounded = coinflip() and round(hour, minute)
    if rounded and rounded != (hour, minute):
        hour, minute = rounded
        goro = GORO

    ampm = ''
    if coinflip():
        ampm = GOZEN if hour < 12 else GOGO
        hour %= 12

    hh = (REIJI if (hour, minute) == (0, 0)
        else SHOUGO if (hour, minute) == (12, 0)
        else f'{hour}{JI}')

    mm = ('' if minute == 0
        else HAN if minute == 30 and (goro or coinflip())
        else f'{minute}{FUN}')

    time = f'{hh}{mm}{choudo}' if ampm or coinflip() else f'{choudo}{hh}{mm}'

    return f'{imawa}{ampm}{time}{goro}{DESU}'


def round(hour, minute):
    if minute < 5:
        minute = 0
    elif 25 < minute < 30 or 30 < minute < 35:
        minute = 30
    elif 55 < minute:
        hour = (hour + 1) % 24
        minute = 0

    return hour, minute


def coinflip():
    return random() > 0.5


if __name__ == '__main__':
    main(sys.argv)
