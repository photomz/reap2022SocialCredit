import os
import json

class StatInfo:
    def __init__(self, name='', code='', scope='',score='', level='',
                 basic_info=-1, main_staff=-1, mgr_info=-1,
                 fin_tax=-1, fin_info=-1, tax_info=-1,
                 mgr_abi=-1, prod_qual=-1, sec_prod=-1, env_prot=-1,
                 law_obey=-1, adm_mgr=-1, law_info=-1, bad_cred=-1,
                 soc_resp=-1, wel_info=-1, trust_info=-1, rank='', histDate=None, histScore=None):
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
        self.histDate = histDate
        self.histScore = histScore
        self.hlistDate = []

    def toContent(self):
        deli = '\t'
        retstr =  str(self.name) + deli + str(self.code) + deli + self.scope + deli + str(self.score) + deli + str(self.level) + deli + \
               str(self.basic_info) + deli + str(self.main_staff) + deli + str(self.mgr_info) + deli + str(self.fin_tax) + deli + \
               str(self.fin_info) + deli + str(self.tax_info) + deli + str(self.mgr_abi) + deli + str(self.prod_qual) + deli + \
               str(self.sec_prod) + deli + str(self.env_prot) + deli + str(self.law_obey) + deli + str(self.adm_mgr) + deli + \
               str(self.law_info) + deli + str(self.bad_cred) + deli + \
               str(self.soc_resp) + deli + str(self.wel_info) + deli + str(self.trust_info) + deli + self.rank
        for i in range(len(self.hlistDate)):
            retstr += deli + str(self.histScore[i])
        return retstr


srcDir = "./test"
files = os.listdir(srcDir)
for file in files:
    fpath = os.path.join(srcDir, file)
    text = ""
    with open(fpath, 'r', encoding='utf-8') as f:
        for line in f:
            text = text + line
    retobj = json.loads(text)
    # retobj = json.dumps(jsonobj, ensure_ascii=False)

    hlistDate = []
    hlistScore = []
    # print(str(retobj['data']['indicatorList'][4]['indicatorName']))
    # print(str(retobj['data']['indicatorList'][4]['points']))
    # print(str(retobj['data']['indicatorList'][4]['score']))
    info = StatInfo(retobj['data']['name'], retobj['data']['uscc'], retobj['data']['businessScope'],
                    retobj['data']['score'],
                    retobj['data']['creditStatus'],
                    retobj['data']['indicatorList'][0]['score'],
                    retobj['data']['indicatorList'][0]['childList'][0]['score'],
                    retobj['data']['indicatorList'][0]['childList'][1]['score'],
                    retobj['data']['indicatorList'][1]['score'],
                    retobj['data']['indicatorList'][1]['childList'][0]['score'],
                    retobj['data']['indicatorList'][1]['childList'][1]['score'],
                    retobj['data']['indicatorList'][2]['score'],
                    retobj['data']['indicatorList'][2]['childList'][0]['score'],
                    retobj['data']['indicatorList'][2]['childList'][1]['score'],
                    retobj['data']['indicatorList'][2]['childList'][2]['score'],
                    retobj['data']['indicatorList'][3]['score'],
                    retobj['data']['indicatorList'][3]['childList'][0]['score'],
                    retobj['data']['indicatorList'][3]['childList'][1]['score'],
                    retobj['data']['indicatorList'][3]['childList'][2]['score'],
                    retobj['data']['indicatorList'][4]['score'],
                    retobj['data']['indicatorList'][4]['childList'][0]['score'],
                    retobj['data']['indicatorList'][4]['childList'][1]['score'], retobj['data']['creditRank'],
                    hlistDate, hlistScore)
    # 这里print了一些数据，然后直接拷贝到excel就可以了
    print(info.toContent())



