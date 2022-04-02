#!/usr/bin/env python
# coding: utf-8

import os
import re
import time
import requests
import pyautogui
from pprint import pprint
from zhconv import convert
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

# 【1】配置浏览器：无头+禁止加载图片
time_start=time.time()
opt=Options()
opt.add_argument('--headless')
opt.add_argument('--disable-gpu')
opt.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
web=Chrome(options=opt)
web.get('http://jgw.aynu.edu.cn/AyjgwSingleSearchHomeIndex?id=1&name=BONE&displayDBName=著录库&Type=2&grade=3&searchFieldJG=&conditionKey=题名')

# 【2】在左侧下拉列表中选择检索项：甲骨片号【默认】；释文；著拓号；分期；记录形式；出处；馆藏编号
try:
    WebDriverWait(web,15,0.3).until(lambda x:x.find_element(By.XPATH,'//*[@id="ConditionKey"]'))
    Select(web.find_element(By.XPATH,'//*[@id="ConditionKey"]')).select_by_visible_text('释文')
    interval_start=time.time()
    Keyword=pyautogui.prompt(text='请输入一个检索关键词：', title='殷契文渊释文检索', default='') # 检索关键词
    interval_end=time.time()
    WebDriverWait(web,15,0.3).until(lambda x:x.find_element(By.XPATH,'//*[@id="ConditionValue"]'))
    web.find_element(By.XPATH,'//*[@id="ConditionValue"]').send_keys(Keyword,Keys.ENTER)
except Exception as e:
    pyautogui.alert(text=f'selenium浏览器启动失败！\n{e}',title='Error!')
    assert 0 # selenium浏览器启动失败，终止运行
# 【3】获取总页数、总条数；编写函数GetData()获取甲骨片号、URL，函数GetInfo()获取分期和释文
WebDriverWait(web,15,0.3).until(lambda x:x.find_element(By.XPATH,'//*[@id="docList"]/div[1]/div[2]')) # 如assert bool(el_ls)==True处抛出AssertionError，请增加此处时间
page_txt=web.find_element(By.XPATH,'//*[@id="docList"]/div[1]/div[2]').text
items,pages=page_txt.split('条结果 1 /')[0].strip(),page_txt.split('条结果 1 /')[1].strip()
print(f'★在殷契文渊检索释文“{Keyword}”，得到{items}条结果，共{pages}页。')

def GetData(Data): # 获取单页所有项的ID（甲骨片号）、url，返回字典
    WebDriverWait(web,15,0.3).until(lambda x:x.find_element(By.XPATH,'//*[@id="docList"]/ul/li/dl/dd/div[1]/a'))
    el_ls=web.find_elements(By.XPATH,'//*[@id="docList"]/ul/li/dl/dd/div[1]/a')
    assert bool(el_ls)==True # 如抛出AssertionError说明el_ls为空列表，请增加检索后等待的时间
    for el in el_ls:
        Dict={}
        BoneID=el.text # 甲骨片号，形如合1
        confirmDialog=el.get_attribute('onclick') # str，形如"confirmDialog(1,'BONE','著录库','168484','176190')"，决定每个详情页的url
        temp=eval(confirmDialog.strip('confirmDialog')) # tuple，形如(1,'BONE','著录库','168484','176190')
        URL=f'''http://jgw.aynu.edu.cn/ajaxpage/home2.0/d/view.html?dbID={temp[0]}&dbName={temp[1]}&DisplayDBName={temp[2]}&sysID={temp[3]}&drnext={temp[4]}''' # 详情页url
        Dict['BoneID']=BoneID
        Dict['URL']=URL
        Data.append(Dict)

t1=time.time()
Data=[]
print('……正在加载第1页……',end='\r')
GetData(Data) # 第1页
for i in range(int(pages)-1):
    try:
        WebDriverWait(web,15,0.3).until(lambda x:x.find_element(By.LINK_TEXT,'下一页'))
        web.find_element(By.LINK_TEXT,'下一页').click()
#         按梯度设置等待时间，以同时保证运行速度和数据提取完整
        if i+2<=10:
            time.sleep(2)
        elif i+2<=25:
            time.sleep(3.5)
        elif i+2<40:
            time.sleep(5)
        else:
            time.sleep(7)
        print(f'……正在加载第{i+2}页……',end='\r')
#         WebDriverWait(web,15,0.3).until(lambda x:x.find_element(By.LINK_TEXT,'下一页'))
        WebDriverWait(web,15,0.3).until(lambda x:x.find_element(By.CLASS_NAME,'botOther')) # 等待页面底端加载
        if i+2==int(pages):
            time.sleep(1.5) # 防止最后一页数据抓取失败
        GetData(Data)
        if i+2==int(pages):
            time.sleep(1.5) # 防止最后一页数据抓取失败
    except Exception as e:
        pyautogui.alert(text=f'在殷契文渊检索释文时，第{i+2}页因为网速原因加载失败，程序中止运行！\n{e}',title='Error!',button='OK')
        assert 0 # 加载失败，程序终止

Data_temp=[] # Data去重并保持原有顺序
for i in Data:
    if i not in Data_temp:
        Data_temp.append(i)
Data=Data_temp
web.quit()
try:
    assert len(Data)==eval(items) # 检查有无遗漏
except Exception as e:
    pyautogui.alert(text=f'在殷契文渊检索释文，有条{eval(items)-len(Data)}数据因网速原因获取失败！\n{e}',title='Error!')
    assert 0
print(f'\n★成功获取数据{len(Data)}条，用时{round(time.time()-t1,2)}秒。即将开始检索分期（自定义）、释文（国学大师网）：')
# pprint(Data)

# 为Data内部字典增加编号
count=1
for Dict in Data:
    Dict['Count']=count
    count+=1

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

# ★在国学大师网检索释文（不使用其分期）
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
        print("……完成检索释文 "+str(Dict['Count'])+"："+str(Dict['BoneID'])+"……",end='\r')
        time.sleep(0.05)
#  ★自定义计算分期
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
    print(f'★计算分期完毕，用时{round(time.time()-t3,2)}秒。即将在殷契文渊缀合库检索缀合情况（用时最长）：')
except Exception as e:
    pyautogui.alert(text=f'计算自定义分期时出现错误！\n{e}',title='Error!')
    assert 0
    
# 【4】在殷契文渊缀合库检索缀合情况【耗时最长】
t4=time.time()
try:
    web_join=Chrome(options=opt)
    web_join.get('http://jgw.aynu.edu.cn/AyjgwZHKSingleSearch?autoLoad=1&id=16&name=ZHUIHEHD&displayDBName=缀合数据库')
    WebDriverWait(web_join,15,0.3).until(lambda x:x.find_element(By.XPATH,'//*[@id="docList"]/div[1]/div[2]/div/span'))
    for Dict in Data:
        BoneID=Dict['BoneID']
        WebDriverWait(web_join,15,0.3).until(lambda x:x.find_element(By.XPATH,'//*[@id="ConditionValue"]')) # 等待输入框加载
        web_join.find_element(By.XPATH,'//*[@id="ConditionValue"]').clear() # 清空输入框
        web_join.find_element(By.XPATH,'//*[@id="ConditionValue"]').send_keys(BoneID,Keys.ENTER) # 检索
        time.sleep(0.5)
    #     查看结果数量
#         WebDriverWait(web_join,15,0.3).until(lambda x:x.find_element(By.XPATH,'//*[@id="docList"]/div[1]/div[2]/div/span'))
        time.sleep(1.25)
        num_join=re.compile(r'(.*?)条结果',re.S).findall(web_join.find_element(By.XPATH,'//*[@id="docList"]/div[1]/div[2]/div/span').text)
        assert num_join !=[] # 否则正则存在问题，无法获得结果数量
        num_join=eval(num_join[0][0])
    #     print(num_join)

        JoinID,JoinURL='',''
        if num_join==0: # 查无结果
            JoinID,JoinURL='',''
        elif num_join>0: # 有结果时，仅获取第一行（默认降序排列，第一行最为完整）
            WebDriverWait(web_join,15,0.3).until(lambda x:x.find_element(By.XPATH,'//*[@id="table_list"]/tbody/tr[1]')) # 等待第一行加载
            code_join=web_join.find_element(By.XPATH,'//*[@id="table_list"]/tbody/tr[1]').get_attribute('innerHTML')
            obj_join=re.compile(r'<td>.*?<a target="_blank" style="color:.*?" href="(.*?)">(.*?)</a>.*?</td>',re.S)
            result_join=obj_join.findall(code_join)
            try:
                JoinURL='http://jgw.aynu.edu.cn'+result_join[0][0]
                JoinURL=JoinURL.replace('amp;','')            
            except: # 表示正则表达式无匹配
                JoinURL='Error!'
            try:
                JoinID=result_join[0][1]
                for j in [' ','\n']:
                    JoinID=JoinID.replace(j,'')
            except: # 表示正则表达式无匹配
                JoinID='Error!'
        else:
            JoinID,JoinURL='Error!','Error!'
    #     print(JoinID,JoinURL)
        Dict['JoinID']=JoinID
        Dict['JoinURL']=JoinURL
        print("……完成检索殷契文渊缀合库 "+str(Dict['Count'])+"："+str(Dict['BoneID']+"……"),end='\r')
    web_join.quit()
    print(f'\n★检索缀合情况完成，用时{round(time.time()-t4,2)}秒。即将开始写入文件：')
except Exception as e:
    pyautogui.alert(text=f'殷契文渊缀合库查询错误！\n{e}',title='Error!')
    assert 0 # 弹窗报错后结束运行
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
            if len(JoinID)>15:
                JoinID=JoinID[:15]+'……'
            JoinURL=Dict['JoinURL']
            if JoinID=='' and JoinURL=='':
                f.write(f'| **{Count}** | [**{BoneID}**]({URL}) | {Period} | {Text} |  |\n')
            else:
                f.write(f'| **{Count}** | [**{BoneID}**]({URL}) | {Period} | {Text} | [**{JoinID}**]({JoinURL}) |\n')

try:
    savepath=f'X:/YinQiWenYuan/【殷契文渊】{Keyword}.md'
    SaveToMd()
    print(f'★存储Markdown完毕，程序总用时{round((time.time()-time_start-(interval_end-interval_start))/60,2)}分钟。')
    print(f'即将打开文件：{os.path.abspath(savepath)}')
    os.system(savepath)
except Exception as e:
    pyautogui.alert(text=f'保存、打开文件失败！\n{e}',title='Error!')
    assert 0
