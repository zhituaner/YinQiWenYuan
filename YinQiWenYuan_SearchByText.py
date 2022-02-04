#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import time
import pyautogui
from pprint import pprint
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

# 为确保数据提取完整，需设置爬取下一个页面前的时间间隔time_sleep。
time_sleep=2
time_start=time.time()
web=Chrome()
web.get('http://jgw.aynu.edu.cn/ajaxpage/home2.0/index.html')
time.sleep(1)

# 【1】登录：若不进入详情页“拓片细览”（进行下载），可将此部分注释掉
# web.find_element(By.XPATH,'//*[@id="loginLink"]').click()
# web.find_element(By.XPATH,'//*[@id="myusercode"]').send_keys('【您的用户名】')
# web.find_element(By.XPATH,'//*[@id="mypassword"]').send_keys('【您的密码】')
# web.find_element(By.XPATH,'//*[@id="LoginForm"]/div[4]/div[2]/a').click()

# 【2】按搜索模式编写函数（甲骨片号ID？释文Text？……/模糊True？精确False？）并调用进行检索
web.find_element(By.XPATH,'//*[@id="submitButtonZN"]').click()
web.switch_to.window(web.window_handles[-1])
# 【搜索模式：按照释文模糊搜索（精确搜索一般不适用于释文）】
# 在左侧下拉列表中选择检索项：甲骨片号【默认】；释文；著拓号；分期；记录形式；出处；馆藏编号
Select(web.find_element(By.XPATH,'//*[@id="ConditionKey"]')).select_by_visible_text('释文')
time.sleep(1)
# 在右侧下拉列表中选择检索模式：模糊【默认】；精确
# Select(web.find_element(By.XPATH,'//*[@id="SubConditionQuery"]')).select_by_visible_text('精确')
# time.sleep(1)
Keyword=pyautogui.prompt(text='请输入一个检索关键词：', title='殷契文渊释文检索', default='') # 检索关键词
web.find_element(By.XPATH,'//*[@id="ConditionValue"]').send_keys(Keyword,Keys.ENTER)
time.sleep(2) # 检索后等待页面加载，如assert bool(el_ls)==True处抛出AssertionError，请增加此处时间

# 【3】存储：获取总页数、总条数；函数GetData()提取单页所有项的ID（甲骨片号）、url，返回数据列表：[ID,url]
page_txt=web.find_element(By.XPATH,'//*[@id="docList"]/div[1]/div[2]').text
items,pages=page_txt.split('条结果 1 /')[0].strip(),page_txt.split('条结果 1 /')[1].strip()
print(f'检索释文“{Keyword}”，得到{items}条结果，共{pages}页。')
print(f'本程序运行速度和成功率均取决于网速。如网络条件允许，可减小变量time_sleep的值（当前为{time_sleep}秒）。')
def GetData():
    data_ls=[]
    el_ls=web.find_elements(By.XPATH,'//*[@id="docList"]/ul/li/dl/dd/div[1]/a')
    assert bool(el_ls)==True # 如抛出AssertionError说明el_ls为空列表，请增加检索后time.sleep的时间
    for el in el_ls:
        ID=el.text # 甲骨片号，形如合1
        confirmDialog=el.get_attribute('onclick') # str，形如"confirmDialog(1,'BONE','著录库','168484','176190')"，决定每个详情页的url
        temp=eval(confirmDialog.strip('confirmDialog')) # tuple，形如(1,'BONE','著录库','168484','176190')
        url=f'''http://jgw.aynu.edu.cn/ajaxpage/home2.0/d/view.html?\
dbID={temp[0]}&dbName={temp[1]}&DisplayDBName={temp[2]}&sysID={temp[3]}&drnext={temp[4]}''' # 详情页url
        data_ls.append([ID,url])
    return data_ls
Data=[]
print('正在爬取第1页……')
Data.extend(GetData()) # 第1页
for i in range(int(pages)-1):
    try:
        time.sleep(1)
        web.find_element(By.LINK_TEXT,'下一页').click()
        print(f'正在爬取第{i+2}页……')
        time.sleep(time_sleep)
        if i+2==int(pages):
            time.sleep(time_sleep) # 防止最后一页数据抓取失败
        Data.extend(GetData())
        if i+2==int(pages):
            time.sleep(time_sleep) # 防止最后一页数据抓取失败
    except:
        pyautogui.alert(text=f'第{i+2}页获取失败，程序中止运行！',title='Error',button='OK')
        break
# Data去重并保持原有顺序
Data_temp=[]
for i in Data:
    if i not in Data_temp:
        Data_temp.append(i)
Data=Data_temp
print(f'成功获取数据{len(Data)}条。开始写入文件……')
# pprint(Data)

# 【4】写入文件。如成功获取全部数据，则关闭浏览器并打开结果文件；如有部分数据未获取，则不关闭浏览器并弹窗提示
path=f'【殷契文渊】{Keyword}.md'
with open (path,'w',encoding='utf-8') as f:
    f.write(f'## 【殷契文渊释文】{Keyword}（{len(Data)}/{items}）\n\n')
    f.write('### Time: '+time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime()))
    f.write('\n\n')
    f.write('|    | 片号 | 分期 | 释文 | 备注 |\n')
    f.write('| --- | ---- | ---- | ---- | ---- |\n')
    for i in range(len(Data)):
        f.write(f'| **{i+1}** | [**{Data[i][0]}**]({Data[i][1]}) |  |  |  |\n')
print(f'写入文件完毕，程序总用时{round(time.time()-time_start,2)}秒。')
if int(items)==len(Data):
    web.quit()
    os.system(path)
else:
    pyautogui.alert(text=f'''有{int(items)-len(Data)}条数据因网速加载抓取失败，请稍微增大变量time_sleep（当前为{time_sleep}秒）。\n
如未抓取数量少（每页12条），请检查是否为最后一页数据遗漏，可手动补充。''',title='Error',button='OK')
