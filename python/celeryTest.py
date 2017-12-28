# -*- coding: utf8 -*-
from celery import chain
from celeryProj.tasks import add, mul, xsum, hello


if __name__ == '__main__':
    hello.delay()
    chain(add.s(4, 4) | mul.s(8))()

