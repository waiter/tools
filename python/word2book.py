#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# python word2book.py /Users/waiter/Documents/study/py2/word_e.json /Users/waiter/Documents/study/py2/book.json

def get_json_content(filePath):
    with open(filePath, 'r') as fp:
        return json.load(fp)

def put_json_file(filePath, new_dict):
    with open(filePath, "w") as f:
        json.dump(new_dict, f)

print '参数个数为:', len(sys.argv), '个参数。'
print '参数列表:', str(sys.argv)

if len(sys.argv) < 3:
    raise '使用方法: python word2book.py /path/to/word.json /path/to/book.json'

wordJson = get_json_content(sys.argv[1])
toBookJson = get_json_content(sys.argv[2])

if wordJson['bookId'] != toBookJson['bookId']:
    raise '数据和书不匹配，可能是不同的书'

for k,v in wordJson['items'].iteritems():
    if len(v) > 0:
        a = k.split('_', 1)
        u = int(a[0])
        p = a[1]
        print u, p
        for np in toBookJson['list'][u]['list']:
            if np['id'] == p:
                for rect in np['rects']:
                    if len(rect['chinese']) > 0 and v.has_key(rect['chinese']):
                        rect['text'] = v.get(rect['chinese'])

put_json_file('book.json', toBookJson)