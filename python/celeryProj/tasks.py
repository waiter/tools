# -*- coding: utf8 -*-
from .celery import app
import random


class bug(object):
    _bigThing = []

    @classmethod
    def why(cls):
        cls._bigThing.insert(0, random.randint(1, 100))
        return cls._bigThing[0]


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@app.task
def hello():
    return 'hello world + %d' % bug.why()


@app.task
def hello2():
    return 'hello world + %d' % bug.why()

