# -*- coding: utf8 -*-
import requests
import os


outBase = '/Users/waiter/Documents/study/testEnRes'

nianji = {
    '1': '一',
    '2': '二',
    '3': '三',
    '4': '四',
    '5': '五',
    '6': '六',
}

shangxia = {
    'a': '上',
    'b': '下'
}

def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

def downloadFile(url, filePath, fileName):
    mkdir(filePath)
    r = requests.get(url, stream=True)
    with open(filePath + fileName, 'wb') as fd:
        for chunk in r.iter_content(None):
            fd.write(chunk)



for n in range(1, 7):
    for x in ['a', 'b']:
        it = "%d%s" % (n, x)
        print(it)
        r = requests.get("http://namibox.com/api/app/tape/bookList?vdir=/v/menu/%s&wxapp=1" % it)
        base = r.json()
        sections = base['sections'] or []
        for section in sections:
            print(section['sectionname'])
            if len(section['section']) > 1:
                print('真的有大于1的')
            for section_c in section['section']:
                print(section_c['itemname'])
                for item in section_c['item']:
                    if item['downloadurl'] and len(item['downloadurl']) > 0 and section_c['itemname'] != '人教版':
                        dd = item['downloadurl']
                        if item['category_lesson'] == '英语' and dd.find('charge') > -1 and dd.find('fake_') > -1:
                            dd = dd.replace('charge', 'd')
                            dd = dd.replace('fake_', '')
                            filePath = "%s/%s/%s/%s/" % (outBase, section_c['itemname'], item['category_lesson'], item['bookname'])
                            fileName = item['bookid'] + '.zip'
                            print("%s-%s-%s-%s" % (item['category_lesson'], item['bookname'], item['bookid'], dd))
                            downloadFile(dd, filePath, fileName)
        # break
    # break



