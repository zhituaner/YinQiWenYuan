#!/usr/bin/env python
# coding: utf-8

import os
import time
import pyautogui
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
WebDriverWait(web,15,0.3).until(lambda x:x.find_element(By.XPATH,'//*[@id="ConditionKey"]'))
Select(web.find_element(By.XPATH,'//*[@id="ConditionKey"]')).select_by_visible_text('释文')
interval_start=time.time()
Keyword=pyautogui.prompt(text='请输入一个检索关键词：', title='殷契文渊释文检索', default='') # 检索关键词
interval_end=time.time()
WebDriverWait(web,15,0.3).until(lambda x:x.find_element(By.XPATH,'//*[@id="ConditionValue"]'))
web.find_element(By.XPATH,'//*[@id="ConditionValue"]').send_keys(Keyword,Keys.ENTER)

# 【3】存储：获取总页数、总条数；函数GetData()提取单页所有项的ID（甲骨片号）、url，返回数据列表：[ID,url]
WebDriverWait(web,15,0.3).until(lambda x:x.find_element(By.XPATH,'//*[@id="docList"]/div[1]/div[2]')) # 如assert bool(el_ls)==True处抛出AssertionError，请增加此处时间
page_txt=web.find_element(By.XPATH,'//*[@id="docList"]/div[1]/div[2]').text
items,pages=page_txt.split('条结果 1 /')[0].strip(),page_txt.split('条结果 1 /')[1].strip()
print(f'检索释文“{Keyword}”，得到{items}条结果，共{pages}页。')
def GetData():
    data_ls=[]
    WebDriverWait(web,15,0.3).until(lambda x:x.find_element(By.XPATH,'//*[@id="docList"]/ul/li/dl/dd/div[1]/a'))
    el_ls=web.find_elements(By.XPATH,'//*[@id="docList"]/ul/li/dl/dd/div[1]/a')
    assert bool(el_ls)==True # 如抛出AssertionError说明el_ls为空列表，请增加检索后等待的时间
    for el in el_ls:
        ID=el.text # 甲骨片号，形如合1
        confirmDialog=el.get_attribute('onclick') # str，形如"confirmDialog(1,'BONE','著录库','168484','176190')"，决定每个详情页的url
        temp=eval(confirmDialog.strip('confirmDialog')) # tuple，形如(1,'BONE','著录库','168484','176190')
        url=f'''http://jgw.aynu.edu.cn/ajaxpage/home2.0/d/view.html?dbID={temp[0]}&dbName={temp[1]}&DisplayDBName={temp[2]}&sysID={temp[3]}&drnext={temp[4]}''' # 详情页url
        data_ls.append([ID,url])
    return data_ls
Data=[]
print('正在加载第1页……',end='')
Data.extend(GetData()) # 第1页
for i in range(int(pages)-1):
    try:
        WebDriverWait(web,15,0.3).until(lambda x:x.find_element(By.LINK_TEXT,'下一页'))
        web.find_element(By.LINK_TEXT,'下一页').click()
        time.sleep(2)
        print(f'正在加载第{i+2}页……',end='')
        WebDriverWait(web,15,0.3).until(lambda x:x.find_element(By.LINK_TEXT,'下一页'))
        Data.extend(GetData())
        if i+2==int(pages):
            time.sleep(1) # 防止最后一页数据抓取失败
    except:
        pyautogui.alert(text=f'第{i+2}页加载失败，程序中止运行！',title='Error',button='OK')
        break
Data_temp=[] # Data去重并保持原有顺序
for i in Data:
    if i not in Data_temp:
        Data_temp.append(i)
Data=Data_temp
print(f'\n成功获取数据{len(Data)}条。开始写入文件……')
path=f'【殷契文渊】{Keyword}.md'
with open (path,'w',encoding='utf-8') as f:
    f.write(f'## 【殷契文渊释文】{Keyword}（{len(Data)}/{items}）\n\n')
    f.write('### Time: '+time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime()))
    f.write('\n\n')
    f.write('|      | 片号 | 分期 | 释文 | 备注 |\n')
    f.write('| ---- | ---- | ---- | ---- | ---- |\n')
    for i in range(len(Data)):
        f.write(f'| **{i+1}** | [**{Data[i][0]}**]({Data[i][1]}) |  |  |  |\n')
print(f'存储完毕，程序总用时{round((time.time()-time_start-(interval_end-interval_start))/60,2)}分钟。')
if int(items)==len(Data):
    web.quit()
    print(f'即将打开文件：{os.path.abspath(path)}')
    os.system(path)
else:
    pyautogui.alert(text=f'''有{int(items)-len(Data)}条数据因网速加载抓取失败。
如未抓取数量少（每页12条），请检查是否为最后一页数据遗漏，可手动补充。''',title='Error',button='OK')
