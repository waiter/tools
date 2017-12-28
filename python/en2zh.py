# -*- coding: utf8 -*-
import json
import os
import shutil
from PIL import Image
from pydub import AudioSegment

audioDis = 1700
word = '朗文'
enword = 'langwen'
bookKey = '023002'
startNianJi = 1
endNianJi = 6
eng = 'english/'
dir = "/Users/waiter/Documents/study/testEng/%s_en/" % enword
outBase = "/Users/waiter/Documents/study/testEng/%s/" % enword
resBase = "reading/resources/%s/" % enword

audioDisS = audioDis / 1000
res = resBase + eng
out = outBase + eng

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


def makeSrcPath(key):
    return "%stape%s_%s/" % (dir, key, bookKey)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def getImageSize(filePath):
    im = Image.open(filePath)
    return im.size

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

def copyFile(sourceFile, targetDir):
    mkdir(targetDir)
    if os.path.isfile(sourceFile):
        shutil.copy(sourceFile, targetDir)

def coverFiles(sourceDir,  targetDir):
    mkdir(targetDir)
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir,  file)
        targetFile = os.path.join(targetDir,  file)
        #cover the files
        if os.path.isfile(sourceFile):
            open(targetFile, "wb").write(open(sourceFile, "rb").read())

def get_json_content(filePath):
    with open(filePath, 'r') as fp:
        return json.load(fp)

def put_json_file(filePath, new_dict):
    with open(filePath, "w") as f:
        json.dump(new_dict, f)

def checkSound(fromFileDir, fileName, toFileDir):
    mkdir(toFileDir)
    # all = fileName.split('_')
    # if len(all) < 2:
    #     print('name too short: ' + fileName)
    # newFileName = all[1].replace(' ', '_') + '.mp3'
    newFileName = fileName[7:]
    # return newFileName
    if not os.path.isfile(toFileDir + newFileName):
        song = AudioSegment.from_mp3(fromFileDir + fileName)
        newSong = song[audioDis:]
        newSong.export(toFileDir + newFileName)
    return newFileName

def pageName2id(name):
    n1 = name.split('_', 1)
    if len(n1) < 2:
        print('name too short: ' + name)
    n2 = n1[1].split('.', 1)
    if len(n2) < 2:
        print('name too short: ' + name + '  ' + n1[1])
    return n2[0]

mkdir(out)

homePage = {
    'iconUrl': resBase + 'icon.jpg',
    'titleText': word + '版',
    'list': []
}

for n in range(startNianJi, endNianJi + 1):
    for x in ['a', 'b']:
        it = "%d%s" % (n, x)
        print(it)
        baseSrc = makeSrcPath(it)
        baseDst = res + it
        baseOut = out + it
        baseImageDst = res + it + '/images/'
        baseImgaeOut = out + it + '/images/'
        baseSoundDst = res + it + '/sound/'
        baseSoundOut = out + it + '/sound/'
        copyFile(baseSrc + 'title.jpg', baseOut)
        coverFiles(baseSrc + 'bookshow', baseImgaeOut)
        iconPath = baseDst + '/title.jpg'
        bookPath = baseDst + '/book.json'
        homePage['list'].append({
            'bookImage': iconPath,
            'bookName': "%s年级%s册" % (nianji[str(n)], shangxia[x]),
            'bookUrl': bookPath
        })

        srcBookJson = get_json_content(baseSrc + 'book.json')
        srcUnits = srcBookJson['bookaudio']['bookitem']
        srcUnitLen = len(srcUnits)
        srcPages = srcBookJson['bookpage']
        srcPageLen = len(srcPages)
        unitPageCount = []
        dstBookJson = {
            'bookCoverUrl': iconPath,
            'bookName': "%s版 - %s年级%s册" % (word, nianji[str(n)], shangxia[x]),
            'bookId': enword + '_' + it,
            'list': []
        }
        srcImgSize = getImageSize(baseSrc + 'bookshow/' + srcPages[0]['page_name'])
        tempPageStart = 0
        for ind, srcUnit in enumerate(srcUnits):
            tempUnit = {
                'name': srcUnit['unit'] if srcUnit['unit'] == srcUnit['title'] else srcUnit['unit'] + ' ' + srcUnit['title'],
                'list': []
            }
            tempPageCount = srcPageLen - tempPageStart
            if ind < srcUnitLen - 1:
                tempPageCount = srcUnits[ind + 1]['page'] - srcUnit['page']
            for tp in range(0, tempPageCount):
                stp = srcPages[tempPageStart + tp]
                tempPage = {
                    'fg': [],
                    'id': pageName2id(stp['page_name']),
                    'imageUrl': baseImageDst + stp['page_name'],
                    'rects': []
                }
                for track in stp['track_info']:
                    aus = float(track['track_austart'])
                    if aus < audioDisS:
                        print("Error: %s" % track['mp3name'])
                    nmusicName = checkSound(baseSrc + 'hiq/', track['mp3name'], baseSoundOut)
                    text = track.get('track_txt') or ""
                    if 'song' == text.lower() or '无' == text:
                        text = ""
                    tempPage['rects'].append({
                        'audioStyle': 0,
                        'chinese': track['track_genre'],
                        'text': text.capitalize(),
                        'music': baseSoundDst + nmusicName,
                        'austart': aus - audioDisS,
                        'auend': float(track['track_auend']) - audioDisS,
                        'x': int(srcImgSize[0] * float(track['track_left'])),
                        'y': int(srcImgSize[1] * float(track['track_top'])),
                        'width': int(srcImgSize[0] * (float(track['track_right']) - float(track['track_left']))),
                        'height': int(srcImgSize[1] * (float(track['track_bottom']) - float(track['track_top'])))
                    })
                tempUnit['list'].append(tempPage)
            tempPageStart += tempPageCount
            dstBookJson['list'].append(tempUnit)
        put_json_file(baseOut + '/book.json', dstBookJson)
        # break
    # break
put_json_file(out + '/homepage.json', homePage)
print(homePage)