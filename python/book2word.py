#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# python book2word.py /Users/waiter/Documents/study/py2/book.json

def get_json_content(filePath):
    with open(filePath, 'r') as fp:
        return json.load(fp)

def put_json_file(filePath, new_dict):
    with open(filePath, "w") as f:
        f.write(json.dumps(new_dict, ensure_ascii=False, indent=2))

print '参数个数为:', len(sys.argv), '个参数。'
print '参数列表:', str(sys.argv)

if len(sys.argv) < 2:
    raise '使用方法: python book2word.py /path/to/book.json'

oldJson = get_json_content(sys.argv[1])

newBook = {
    'bookId': oldJson['bookId'],
    'items': {},
}
emptyBook = {
    'bookId': oldJson['bookId'],
    'items': {},
}
for ind in range(len(oldJson['list'])):
    for pa in oldJson['list'][ind]['list']:
        pk = "%d_%s" % (ind, pa['id'])
        newBook['items'][pk] = {}
        emptyBook['items'][pk] = {}
        for rect in pa['rects']:
            if len(rect['chinese']) > 0:
                newBook['items'][pk][rect['chinese']] = rect['text'] or ''
                if len(rect['text']) < 1:
                    emptyBook['items'][pk][rect['chinese']] = ''

# print newBook
put_json_file('word.json', newBook)
put_json_file('word_e.json', emptyBook)
