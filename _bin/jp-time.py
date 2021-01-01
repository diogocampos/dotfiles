#!/usr/bin/env python3

from datetime import datetime
import random
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


def main():
    phrase = generate_phrase(datetime.now())
    if not sys.stdout.isatty(): print(phrase, file=sys.stderr)
    print(phrase)


def generate_phrase(datetime):
    hour = datetime.hour
    minute = datetime.minute

    imawa = IMAWA if coinflip() else ''

    choudo = CHOUDO if (minute == 0 or minute == 30) and coinflip() else ''

    goro = ''
    rounded = coinflip() and round(hour, minute)
    if rounded and rounded != (hour, minute):
        hour, minute = rounded
        goro = GORO

    ampm = ''
    if (hour % 12) > 0 and coinflip():
        ampm = GOZEN if hour < 12 else GOGO
        hour %= 12

    hh = (REIJI if (hour, minute) == (0, 0)
        else SHOUGO if (hour, minute) == (12, 0)
        else f'{hour}{JI}')

    mm = ('' if minute == 0
        else HAN if minute == 30 and (goro or coinflip())
        else f'{minute}{FUN}')

    hhmm = f'{hh}{mm}'
    time = f'{hhmm}{choudo}' if ampm or coinflip() else f'{choudo}{hhmm}'

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
    return random.random() > 0.5


if __name__ == '__main__':
    main()
