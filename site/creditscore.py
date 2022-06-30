import gzip
import json
import time
import uuid
from datetime import datetime

import requests

class StatInfo:
    def __init__(self, name='', code='', scope='',score='', level='',
                 basic_info=-1, main_staff=-1, mgr_info=-1,
                 fin_tax=-1, fin_info=-1, tax_info=-1,
                 mgr_abi=-1, prod_qual=-1, sec_prod=-1, env_prot=-1,
                 law_obey=-1, adm_mgr=-1, law_info=-1, bad_cred=-1,
                 soc_resp=-1, wel_info=-1, trust_info=-1, rank=''):
        self.name = name
        self.code = code
        self.scope = scope
        self.score = score
        self.level = level
        self.basic_info = basic_info
        self.main_staff = main_staff
        self.mgr_info = mgr_info
        self.fin_tax = fin_tax
        self.fin_info = fin_info
        self.tax_info = tax_info
        self.mgr_abi = mgr_abi
        self.prod_qual = prod_qual
        self.sec_prod = sec_prod
        self.env_prot = env_prot
        self.law_obey = law_obey
        self.adm_mgr = adm_mgr
        self.law_info = law_info
        self.bad_cred = bad_cred
        self.soc_resp = soc_resp
        self.wel_info = wel_info
        self.trust_info = trust_info
        self.rank = rank

    def toContent(self):
        deli = '\t'
        return str(self.name) + deli + str(self.code) + deli + self.scope + deli + str(self.score) + deli + str(self.level) + deli + \
               str(self.basic_info) + deli + str(self.main_staff) + deli + str(self.mgr_info) + deli + str(self.fin_tax) + deli + \
               str(self.fin_info) + deli + str(self.tax_info) + deli + str(self.mgr_abi) + deli + str(self.prod_qual) + deli + \
               str(self.sec_prod) + deli + str(self.env_prot) + deli + str(self.law_obey) + deli + str(self.adm_mgr) + deli + \
               str(self.law_info) + deli + str(self.bad_cred) + deli + \
               str(self.soc_resp) + deli + str(self.wel_info) + deli + str(self.trust_info) + deli + self.rank


class DownloadData:
    def __init__(self, code='', status='', brange='', name='', credit=-1,
                 level='', cap='', rank='', date='', bcode='', host='', addr='', reg='', ccode=''):
        self.code = code
        self.status = status
        self.brange = brange
        self.name = name
        self.credit = credit
        self.level = level
        self.cap = cap
        self.rank = rank
        self.date = date
        self.bcode = bcode
        self.host = host
        self.addr = addr
        self.reg = reg
        self.ccode = ccode

    def toString(self):
        return '' + self.code + '^' + self.status + '^' + self.brange + '^' + \
               self.name + '^' + str(self.credit) + '^' + self.level + '^' + self.cap + '^' + self.rank + '^' + \
               self.date + '^' + self.bcode + '^' + self.host + '^' + self.addr + '^' + self.reg + '^' + self.ccode


def writeContentToTxt(path, content):
    output = open(path, 'a', encoding='utf8')
    output.write(content)
    output.write('\n')
    output.close()


def getDetailInfo(code):
    nuuid = str(uuid.uuid1()).replace('-','')
    tts = int(datetime.timestamp(datetime.now())* 1000)
    header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-SG,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '288',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'xyxx.zjzwfw.gov.cn',
        'Referer': 'https://credit.zj.gov.cn/',
        'Origin': 'https://credit.zj.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'secret': nuuid,
        'time': str(tts),
    }

    data = json.dumps({'condition': code, 'source': '3', 'type': 'E', 'pageNo': 1, 'pageSize': 20})
    surl = 'https://xyxx.zjzwfw.gov.cn/router/api/p/creditSearchCityArchivalInfo'
    requests.packages.urllib3.disable_warnings()
    response = requests.post(surl, headers=header, data=data, timeout=5, verify=False)  # 获取文件数目，页的数目
    try:
        response.raise_for_status()
        print(f"Content: {response.content}")
        print("code = " + str(response.status_code))
        res_content = gzip.decompress(response.content).decode(encoding="utf-8")
        print(res_content)
        retobj = json.loads(res_content)
        if retobj['code'] == 0:
            return retobj['data'][0]['name'], retobj['data'][0]['uscc'], retobj['data'][0]['type']
        else:
            print('[DOWNLOAD-1] error! code = {}, msg = {}'.format(retobj['code'], retobj['msg']))
            return None
    except Exception as e:
        print('[DOWNLOAD-1]: exception = ' + str(e) + ', creditid = ' + code)
        return None


def getCompInfo(compname, code, type):
    header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'xyxx.zjzwfw.gov.cn',
        'Referer': 'https://xyxx.zjzwfw.gov.cn/index/',
        'Origin': 'http://xyxx.zjzwfw.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    }
    url = "https://xyxx.zjzwfw.gov.cn/router/api/p/creditSearchCreditArchivalInfo"
    data = json.dumps({'name': compname, 'type': type, 'uscc': code})
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url, headers=header, data=data, timeout=5, verify=False)  # 获取文件数目，页的数目
    try:
        response.raise_for_status()
        res_content = response.content.decode()
        retobj = json.loads(res_content)
        if retobj['code'] == 0:
            return retobj
        else:
            print('[DOWNLOAD-2] error! compcode = {} code = {}, msg = {}'.format(code, retobj['code'], retobj['msg']))
            return None
    except Exception as e:
        print('[DOWNLOAD-2]: exception = ' + str(e) + ', compcode = ' + code)
        return None

def getCompBadInfo(code):
    header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Host': 'xyxx.zjzwfw.gov.cn',
        'Referer': 'https://xyxx.zjzwfw.gov.cn/index/',
        'Origin': 'http://xyxx.zjzwfw.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    }
    url = "https://xyxx.zjzwfw.gov.cn/router/api/p/creditGetCreditArchivalTableDetailInfo"
    # {tableName: "sfy_dwwlxsxcpxx_zz_ne    w_da,sxbzxr", uscc: "913300000753389389"}
    data = json.dumps({'tableName': 'punishment_pjda', 'uscc': code})  #   sfy_dwwlxsxcpxx_zz_new_da
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url, headers=header, data=data, timeout=5, verify=False)  # 获取文件数目，页的数目
    try:
        response.raise_for_status()
        res_content = response.content.decode()
        retobj = json.loads(res_content)
        if retobj['code'] == 0:
            return retobj
        else:
            print('[DOWNLOAD-3] error! compcode = {} code = {}, msg = {}'.format(code, retobj['code'], retobj['msg']))
            return None
    except Exception as e:
        print('[DOWNLOAD-3]: exception = ' + str(e) + ', compcode = ' + code)
        return None

datalist = []
with open('./data20210608.txt', 'r', encoding='utf-8') as f:  # /data20210608.txt
    cnt = 0
    for line in f:
        line = line.strip()
        print('{} : {}'.format(cnt, line))
        try:

            info = getDetailInfo(line)
            if info is None:
                continue
            data = getCompInfo(info[0], info[1], info[2])
            if data is None:
                continue
            data2 = getCompBadInfo(line)
            if data is None:
                continue
            wct = info[0] + "^^^" + info[1] + "^^^" + json.dumps(data) + "^^^" + json.dumps(data2)
            writeContentToTxt('data20220502.txt', wct)
            time.sleep(3)
        except Exception as e:
            print('[DOWNLOAD]: exception = ' + str(e) + ', creditid = ' + line)
        cnt += 1

