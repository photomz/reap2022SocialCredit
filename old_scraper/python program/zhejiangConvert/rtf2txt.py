import os
import json
from win32com.client import Dispatch
import time



def read_rtf_to_text(srcPath, dstPath):
    try:
        word = Dispatch('Word.Application')
        word.Visible = False
        word.DisplayAlerts = False
        doc = word.Documents.Open(FileName=srcPath, Encoding='gbk')
        with open(dstPath, 'w', encoding='utf-8') as f:
            for text in doc.paragraphs:
                f.write(str(text))
            f.flush()
        doc.Close()
        word.Quit()
    except Exception as e:
        print('---> [exception]:  ' + repr(e))


if __name__ == "__main__":
    srcDir = r"C:\\Users\\riwei\\Dropbox\\CSCS score\\rtf-format\\"
    dstDir = r"test\\"
    filelist = os.listdir(srcDir)
    cnt = 1
    for file in filelist:
        newname = file.replace("rtf", "txt")
        srcPath = srcDir + file
        dstPath = dstDir + newname
        if os.path.exists(dstPath) and os.path.getsize(dstPath) > 0:
            print("[{}]: exists {}".format(cnt, srcPath))
            cnt = cnt + 1
            continue
        print("[{}]: {}".format(cnt, srcPath))
        read_rtf_to_text(srcPath, dstPath)
        cnt = cnt + 1
        time.sleep(1)


