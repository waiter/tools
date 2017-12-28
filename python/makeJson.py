import os
import json

dir = '/Users/waiter/Documents/study/testEng/json2/'
out = '/Users/waiter/Documents/study/testEng/json2_o/'

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

def get_json_content(filePath, c='utf8'):
    with open(filePath, 'r', encoding=c) as fp:
        return json.load(fp)

def put_json_file(filePath, new_dict):
    with open(filePath, "w") as f:
        json.dump(new_dict, f)


for i in range(0, 8):
    rBookJson = {}
    now = 61251 + i
    nowPath = "%s%d/" % (dir, now)
    outPath = "%s%d/" % (out, now)
    mkdir(outPath)
    bookJson = get_json_content("%sbook%d.json" % (nowPath, now))
    rBookJson['bookCoverUrl'] = bookJson['bookCoverUrl']
    rBookJson['bookId'] = bookJson['bookId']
    rBookJson['bookName'] = bookJson['bookName']
    rBookJson['list'] = []
    for ui in bookJson['list']:
        rUnitJson = {
            'name': ui['name'],
            'list': []
        }
        uiFileName = ui['url'].replace("reading/resources/PEP/english/EliteEdition/%d/" % now, '')
        nowUnitJson = get_json_content("%s%s" % (nowPath, uiFileName))
        for pa in nowUnitJson['list']:
            rPageJson = {
                'fg': [],
                'imageUrl': pa['imageUrl'],
                'rects': []
            }
            nPageName = pa['url'].replace("reading/resources/PEP/english/EliteEdition/%d/pagejson/" % now, '')
            pageJson = get_json_content("%spageJsonSort/%s" % (nowPath, nPageName))
            rPageJson['id'] = pageJson['id']
            if pageJson['iconlist']:
                rPageJson['iconlist'] = pageJson['iconlist']
            for re in pageJson['rects']:
                rPageJson['rects'].append(re)
            rUnitJson['list'].append(rPageJson)
        rBookJson['list'].append(rUnitJson)
    put_json_file(outPath + 'book.json', rBookJson)
