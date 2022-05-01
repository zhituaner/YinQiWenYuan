#!/usr/bin/env python
# coding: utf-8

import os
import re
import time
import requests
import pyautogui
from pprint import pprint
from zhconv import convert

sleep_time=0.2 # 设置爬虫间隔
# 【1】检索殷契文渊释文，得到总页数、总条目数；爬取所有页的甲骨片号及其链接，写入字典
Keyword=pyautogui.prompt(text='请输入一个检索关键词：', title='殷契文渊释文检索', default='') # 检索关键词
time_start=time.time()
with open('library.txt','r',encoding='utf-8') as f: # 存储著录库，如有更新需要修改
    library=f.read()
    
# post请求的表单数据：（动态变化：ConditionValue、beforeConditionValue、pageIndexNow）
datals={'ConditionKey2': 'YW','ConditionValue2': '','SubConditionQuery0': 2,'ConditionKey': 'SW','ConditionValue': Keyword,
    'SubConditionQuery': 2,'beforeQueryValue': 2,'beforeConditionValue': Keyword,'beforeConditionValue2': '','beforeConditionKey': 'SW',
    'searchFieldJG': '','beforecheckedCatID': library,'beforeselectedCatTypeID': 2,'fieldName': '','fieldValue': '','currentSubid': 0,
    'checkedCatID': library,'selectedCatTypeID': 2,'pageIndexNow': 1,'sortField': '','sortFieldBefore': '','sortInit': '',
    'sortDescAsc': '','listOrabst': '','dbID': 1,'dbName': 'BONE','MediaType': 5,'topicCLSCode': '','topicCLSNodeCode': '',
    'AutoLoad': True,'SearchFrom': 'SingleSearch','pageSize': 12,'swid': '','swid': '','SubConditionType0': 0,'SubConditionKey0': 'PM',
    'SubConditionValue0': '','X-Requested-With': 'XMLHttpRequest'}
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

# 获取总页数、总条目数
search_code=requests.post(url='http://jgw.aynu.edu.cn/AyjgwSingleSearch/Search',data=datals,headers=headers).text
# print(search_code)
search_info=re.compile(r'<span>(.*?)条结果.*?/(.*?)</span>',re.S).findall(search_code)
try:
    assert search_info !=[]
except Exception as e:
    pyautogui.alert(text=f'殷契文渊释文检索：总页数、总条目数正则表达式无匹配！\n{e}',title='Error!')
    assert 0
items=eval(search_info[0][0].replace(' ',''))
pages=eval(search_info[0][1].replace(' ',''))
print(f'★在殷契文渊检索释文“{Keyword}”，得到{items}条结果，共{pages}页。')

# 分页爬虫
Data=[]
Count=1
for page in range(pages):
    current_page=page+1
    print(f'……正在加载第{current_page}/{pages}页……',end='\r')
    try:
        if current_page==1:
            search_code_child=search_code
        else:
            datals['pageIndexNow']=current_page
            search_code_child=requests.post(url='http://jgw.aynu.edu.cn/AyjgwSingleSearch/Search',data=datals,headers=headers).text
        search_result=re.compile(r'''<div class='tc mb10'>.*?<a onclick="confirmDialog(.*?)" href=".*?">(.*?)</a>''',re.S).findall(search_code_child)
        try:
            assert search_result !=[]
        except Exception as e:
            pyautogui.alert(text=f'殷契文渊释文检索：第{current_page}页数据正则表达式无匹配！\n{e}',title='Error!')
            assert 0
        for i in search_result:
            Dict={'Count':Count}
            temp=eval(i[0]) # tuple，形如(1,'BONE','著录库','168484','176190')
            URL=f'http://jgw.aynu.edu.cn/ajaxpage/home2.0/d/view.html?dbID={temp[0]}&dbName={temp[1]}&DisplayDBName={temp[2]}&sysID={temp[3]}&drnext={temp[4]}' # 详情页url
            Dict['URL']=URL
            BoneID=i[1]
            for j in ['\r','\n','\t',' ']:
                BoneID=BoneID.replace(j,'')
            Dict['BoneID']=BoneID
            Data.append(Dict)
            Count+=1
    except Exception as e:
        pyautogui.alert(text=f'在殷契文渊检索释文“{Keyword}”，第{current_page}页爬虫失败！\n{e}',title='Error!')
        assert 0
    time.sleep(sleep_time)
    
try:
    assert len(Data)==items # 检查有无遗漏
except Exception as e:
    pyautogui.alert(text=f'在殷契文渊检索释文“{Keyword}”，有{items-len(Data)}条数据获取失败！\n{e}',title='Error!')
    assert 0
print(f'\n★成功获取数据{len(Data)}条，用时{round(time.time()-time_start,2)}秒。即将开始检索分期（自定义）、释文（国学大师网）：')
# pprint(Data)

# 【2】检索释文：国学大师网（暂不使用其分期）
def SplitBoneID(Dict): # 分离甲骨片号中的著录名和数字
    BoneID=Dict['BoneID']
    tempBoneID=BoneID
#         分离甲骨片号中的甲骨著录简称和数字
    while not tempBoneID[-1].isdigit():
        tempBoneID=tempBoneID[:-1]
    Book,numID='',''
    for i in tempBoneID:
        numID+=i if i.isdigit() else ''
        Book+=i if not i.isdigit() else ''
    while numID[0]=='0':
        numID=numID[1:]
    numID=eval(numID)
    return Book,numID

def GetText(Data):
    for Dict in Data: # Dict有两个键：BoneID和URL
        Book,numID=SplitBoneID(Dict)[0],SplitBoneID(Dict)[1]
        if Book in ['合','合补','屯南','花东']:
            try:
                if Book=='合':
                    bhfl=1
                elif Book=='合补':
                    bhfl=2
                elif Book=='屯南':
                    bhfl=3
                elif Book=='':
                    bhfl=4
                gxdsURL=f'http://www.guoxuedashi.net/jgwhj/?bhfl={bhfl}&bh={numID}&jgwfl='
    #             print(gxdsURL)
                obj_gxds=re.compile(r'<tr><td width=.*?>(.*?)</td><td width=.*?>'
                        r'(.*?)</td><td >(.*?)</td><td width=.*?>.*?</td></tr>',re.S)
                result_gxds=obj_gxds.findall(requests.get(gxdsURL).text)
                if not result_gxds==[]: # 检索有结果
                    if len(result_gxds)==1:
                        Text=result_gxds[0][2]
                        Text=convert(Text,'zh-hans')
                        Dict['Text']=Text
                    else:
                        gxdsID=[]; Text=''
                        for r in result_gxds:
                            gxdsID.append(r[0])
                        if len(set(gxdsID))==1:
                            for r in result_gxds:
                                Text+=f'{r[1]}：{r[2]}'
                                Text+='<br />' if not r==result_gxds[-1] else ''
                        else:
                            for r in result_gxds:
                                Text+=f'{r[0]}-{r[1]}：{r[2]}'
                                Text+='<br />' if not r==result_gxds[-1] else ''
                        Text=convert(Text,'zh-hans')
                        Dict['Text']=Text
                else: # 检索结果为空
                    Dict['Text']=''
            except:
                Dict['Text']='Error!'
        else: # 目前无法检索释文
            Dict['Text']=''
        Text=Dict['Text']
        if Text !='': # 筛选无用信息
            if Text[0].isalpha() or Text[-1].isdigit() or Text[0]=='<' or Text[-1]=='>' or 'a href' in Text:
                Dict['Text']=''
        print("……完成检索释文 "+str(Dict['Count'])+"/"+str(items)+"："+str(Dict['BoneID'])+"……",end='\r')
        time.sleep(sleep_time)

#  【3】计算分期：自定义
def GetPeriod(Data):
    for Dict in Data:
        Book,numID=SplitBoneID(Dict)[0],SplitBoneID(Dict)[1]
        if Book=='合':
            if 1<=numID<=19753 or 39477<=numID<=40814:
                Period='第一期'
            elif 19754<=numID<=22536 or 40815<=numID<=40910:
                Period='第一期附'
            elif 22537<=numID<=26878 or 40911<=numID<=41302:
                Period='第二期'
            elif 26879<=numID<=31968 or 41303<=numID<=41453:
                Period='第三期'
            elif 31969<=numID<=35342 or 41454<=numID<=41694:
                Period='第四期'
            elif 35343<=numID<=39476 or 41695<=numID<=41956:
                Period='第五期'
            else:
                Period='Error!'
        elif Book=='合补':
            if 1<=numID<=6543 or 13171<=numID<=13259:
                Period='第一期'
            elif 6544<=numID<=6954 or 13260<=numID<=13269:
                Period='第一期附'
            elif 6955<=numID<=8705 or 13270<=numID<=13326:
                Period='第二期'
            elif 8706<=numID<=10409 or 13327<=numID<=13383:
                Period='第三期'
            elif 10410<=numID<=10940 or 13384<=numID<=13422:
                Period='第四期'
            elif 10941<=numID<=13170 or 13423<=numID<=13450:
                Period='第五期'
            else:
                Period='Error!'
        elif Book=='旅藏':
            if 1<=numID<=1331:
                Period='第一期'
            elif 1332<=numID<=1753:
                Period='第二期'
            elif 1754<=numID<=1860:
                Period='第三期'
            elif 1861<=numID<=1912:
                Period='第四期'
            elif 1913<=numID<=2211:
                Period='第五期'
            else:
                Period='Error!'
        elif Book=='卡':
            if 1<=numID<=12:
                Period='师组'
            elif numID==13:
                Period='丙种子卜辞（子组）'
            elif 14<=numID<=17:
                Period='师宾间组'
            elif 18<=numID<=70:
                Period='师历间组'
            elif 71<=numID<=95:
                Period='宾组'
            elif 96<=numID<=106:
                Period='历组'
            elif 107<=numID<=364:
                Period='出组'
            elif 365<=numID<=366:
                Period='历无'
            elif 367<=numID<=379:
                Period='何组'
            elif 380<=numID<=393:
                Period='无名组'
            elif 394<=numID<=402:
                Period='习刻'
            elif 403<=numID<=404:
                Period='伪刻'
            elif 405<=numID<=406:
                Period='遗失甲骨'
            elif 407<=numID<=609:
                Period='护身符'
            else:
                Period='Error!'
        else:
            Period=''
        Dict['Period']=Period

#  调用函数，得到释文和分期
try:
    t2=time.time()
    GetText(Data) # 如国学大师网发生变动，需修改或取消调用此函数！
    print(f'\n★检索释文完毕，用时{round(time.time()-t2,2)}秒。')
except Exception as e:
    pyautogui.alert(text=f'在国学大师网检索释文遇到错误！\n{e}',title='Error!')
    assert 0
try:
    t3=time.time()
    GetPeriod(Data)
    print(f'★计算分期完毕，用时{round(time.time()-t3,2)}秒。即将在殷契文渊/先秦史研究室缀合库检索缀合情况：')
except Exception as e:
    pyautogui.alert(text=f'计算自定义分期时出现错误！\n{e}',title='Error!')
    assert 0
    
# 【4】在殷契文渊缀合库检索缀合情况
t4=time.time()
for Dict in Data:
    BoneID=Dict['BoneID']
# 【缀合1】殷契文渊缀合库
    try:
        data={'ConditionKey2': '','ConditionValue2': '','SubConditionQuery2': 2,'ConditionKey': 'ZHPH','ConditionValue': BoneID,
        'SubConditionQuery': 0,'beforeQueryValue': 0,'beforeConditionValue': BoneID,'beforeConditionValue2': '','beforeConditionKey': 'ZHPH',
        'beforecheckedCatID': '','beforeselectedCatTypeID': '','fieldName': '','fieldValue': '','currentSubid': 0,'checkedCatID': '',
        'selectedCatTypeID': '','pageIndexNow': 1,'sortField': '','sortFieldBefore': '','sortInit': '','sortDescAsc': '','listOrabst': '',
        'dbID': 16,'dbName': 'ZHUIHEHD','MediaType': 0,'topicCLSCode': '','topicCLSNodeCode': '','AutoLoad': True,'SearchFrom': 'SingleSearch',
        'pageSize': 10,'SubConditionType0': 0,'SubConditionKey0': 'ZHPH','SubConditionValue0': '','X-Requested-With': 'XMLHttpRequest'}
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
        join_code_yqwy=requests.post(url='http://jgw.aynu.edu.cn/AyjgwZHKSingleSearch/Search',data=data,headers=headers).text
        join_result_yqwy=re.compile(r'<td>.*?href="(.*?)">(.*?)</a>.*?</td>.*?<td>.*?</td>.*?<td>.*?</td>',re.S).findall(join_code_yqwy)
        if join_result_yqwy==[]:
            JoinID,JoinURL='',''
        else: # 一般情况下第一条结果最为全面，故仅取第一条
            JoinID=join_result_yqwy[0][1]
            JoinURL='http://jgw.aynu.edu.cn'+join_result_yqwy[0][0]
            for exclude in [' ','\r','\n']:
                JoinID=JoinID.replace(exclude,'')
    except Exception as e:
        pyautogui.alert(text=f'殷契文渊缀合库查询错误！\n{e}',title='Error!')
        assert 0 # 弹窗报错后结束运行
# 【缀合2】先秦史研究室（在殷契文渊缀合库没有结果时调用）
    try:
        if JoinID=='' and JoinURL=='':
            join_code_xq=requests.get(f'https://www.xianqin.org/?s={BoneID}').text
            join_result_xq=re.compile(r'<div id="search_page">.*?<li><a href="(.*?)" title="(.*?)">.*?</a></li>',re.S).findall(join_code_xq)
            if join_result_xq==[]:
                JoinID,JoinURL='',''
            else:
                if '缀' not in JoinID and '綴' not in JoinID and '拼' not in JoinID: # 文章名含有此字才是缀合文章
                    JoinID,JoinURL='',''
                else:
                    JoinID=join_result_xq[0][1]
                    JoinURL=join_result_xq[0][0]
    except Exception as e:
        pyautogui.alert(text=f'先秦史研究室缀合库查询错误！\n{e}',title='Error!')
        assert 0 # 弹窗报错后结束运行
    Dict['JoinID']=JoinID
    Dict['JoinURL']=JoinURL
    print("……完成检索殷契文渊/先秦史研究室缀合库 "+str(Dict['Count'])+"/"+str(items)+"："+str(Dict['BoneID']+"……"),end='\r')
    time.sleep(sleep_time)
print(f'\n★检索缀合情况完成，用时{round(time.time()-t4,2)}秒。即将开始写入文件：')
# pprint(Data) # ★用于检查

# 【5】将Data写入文件存储：提供MD格式函数（写入Excel、设置样式太麻烦了w）
def SaveToMd():
    with open (savepath,'w',encoding='utf-8') as f:
        f.write(f'## 【殷契文渊】{Keyword}（{len(Data)}/{items}）\n\n')
        f.write('### Time: '+time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime()))
        f.write('\n\n')
        f.write('|      | 片号 | 分期 | 释文 | 缀合 |\n')
        f.write('| ---- | ---- | ---- | ---- | ---- |\n')
        for Dict in Data:
            Count=Dict['Count']
            BoneID=Dict['BoneID']
            URL=Dict['URL']
            Period=Dict['Period']
            Text=Dict['Text'] # 使用Markdown语法换行符<br />
            JoinID=Dict['JoinID']
            if len(JoinID)>15: # 缀合片号过长时省略部分
                JoinID=JoinID[:15]+'……'
            JoinURL=Dict['JoinURL']
            if JoinID=='' and JoinURL=='':
                f.write(f'| **{Count}** | [**{BoneID}**]({URL}) | {Period} | {Text} |  |\n')
            else:
                f.write(f'| **{Count}** | [**{BoneID}**]({URL}) | {Period} | {Text} | [**{JoinID}**]({JoinURL}) |\n')

try:
    savepath=f'X:/YinQiWenYuan/【殷契文渊】{Keyword}.md'
    SaveToMd()
    print(f'★存储Markdown完毕，程序总用时{round((time.time()-time_start)/60,2)}分钟。即将打开文件：{os.path.abspath(savepath)}')
    os.system(savepath)
except Exception as e:
    pyautogui.alert(text=f'保存、打开文件失败！\n{e}',title='Error!')
    assert 0
