#!/usr/bin/env python
# coding: utf-8

import re
import os
import time
import pyautogui
from math import ceil
from pprint import pprint
from zhconv import convert
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

try:
    start=time.time()
    opt=Options()
    web=Chrome(options=opt)
    web.maximize_window()
    web.get('http://jgw.aynu.edu.cn/ajaxpage/home2.0/d/list.html?type=1&searchField=&conditionKey=题名&checkDatabaseID=&currentClassID=002')
    if '注销页' in web.title: # 有时候会莫名其妙跑到校园网注销页
        web.get('http://jgw.aynu.edu.cn/ajaxpage/home2.0/d/list.html?type=1&searchField=&conditionKey=题名&checkDatabaseID=&currentClassID=002')

    interval1=time.time()
    conf=pyautogui.confirm(title='殷契文渊文献库',text='请手动高级检索，完成后滑动到页面底端并点击确定。\n\n【注】高级检索将始终在前台运行，请勿关闭浏览器！')
    interval2=time.time()
    try:
        assert conf !='Cancel'
    except:
        web.quit()
        assert 0

    WebDriverWait(web,10,0.2).until(lambda x:x.find_element(By.XPATH,'//*[@id="Tabheadhead"]/div[2]/span'))
    nums=eval(web.find_element(By.XPATH,'//*[@id="Tabheadhead"]/div[2]/span').text)
    pages=ceil(nums/10) # 当前为每页显示10条结果，如网页变化需要修改
    print(f'在殷契文渊文献库进行高级检索，得到{nums}条结果，共{pages}页。')

    Data=[]
    count=1
    for i in range(pages):
        current_page=i+1
        print(f'……开始加载第{current_page}／{pages}页……',end='\r')
        if 1<current_page<=pages:
            WebDriverWait(web,10,0.2).until(lambda x:x.find_element(By.LINK_TEXT,'下一页'))
            time.sleep(0.5)
            web.find_element(By.LINK_TEXT,'下一页').click()
            time.sleep(0.5)
        bs=BeautifulSoup(web.page_source)
        table=bs.find_all('tbody',attrs={'id':'TabTr'})[0]
        el_ls=table.find_all('tr')
    #     pprint(el_ls)

    #     提取信息（由易到难）
        for el in el_ls:
            Dict={}
            Dict['Count']=count
    #         【1】作者
            author=re.compile(r'<td class="author_flag">(.*?)</td>',re.S).findall(str(el))
            if author:
                author=convert(author[0].replace(';','；'),'zh-hans')
            else:
                author=''
            Dict['Author']=author
    #         【2】来源、日期
            origin_date=re.compile(r'<td align="center">(.*?)</td><td align="center">(.*?)</td>',re.S).findall(str(el))
            if origin_date:
                origin=convert(origin_date[0][0].replace(';','；'),'zh-hans')
                origin=origin[:origin.find('(')] if '(' in origin else origin # 简化
                origin=origin[:origin.find('（')] if '（' in origin else origin
                origin=origin[:origin.find('-')] if '-' in origin else origin
                origin=origin.replace(' ','')
                origin=origin.replace('\n','')
                date=origin_date[0][1]
                date=date[:date.find('-')] if '-' in date else date # 简化：只保留年
            else:
                origin,date='',''
            Dict['Origin']=origin
            Dict['Date']=date
    #         【3】标题【难点：将标题中图像链接转为Markdown语法】
            title=re.compile(r'<span>(.*?)</span></a>',re.S).findall(str(el))
            if title:
                title=title[0]
                for i in ['<span style="color:red;margin: 0px">','<span>','</span>','<img alt="" src=','/>','"']:
                    title=title.replace(i,'')
                if 'alt' in title:
                    for i in range(5,30):
                        for j in ['<img alt=','src=','height='+str(i),"width="+str(i)]:
                            title=title.replace(j,'')
                title=title.replace(' ','')
                if 'jpg' in title:
                    title=title.replace('/File','<img src="http://jgw.aynu.edu.cn/File')
                    title=title.replace('.jpg','.jpg" style="zoom: 50%;" />')
                elif 'png' in title:
                    title=title.replace('/File','<img src="http://jgw.aynu.edu.cn/File')
                    title=title.replace('.png','.png" style="zoom: 50%;" />')
            else:
                title=''
            title=title.replace('\n','')
    #         title=title[:title.find('——')] if '——' in title and len(title)>20 else title # 简化
            Dict['Title']=convert(title,'zh-hans')        
    #         【4】URL
            url_ls=re.compile(r"dbID=(.*?)&amp;dbName=(.*?)&amp;sysID=(.*?)'",re.S).findall(str(el))
            try:
                url=f'http://jgw.aynu.edu.cn/ajaxpage/home2.0/d/detail.html?dbID={url_ls[0][0]}&dbName={url_ls[0][1]}&sysID={url_ls[0][2]}'
            except:
                url=''
            Dict['Url']=url
            Data.append(Dict)
            count+=1
        current_page+=1
    web.quit()
    # print()
    # pprint(Data)

    interval3=time.time()
    filename=pyautogui.prompt(title='殷契文渊文献库',text='请输入文件命名：\n\n（文件名非法字符：\ / : * ? " < > |）',default='【文献库】')
    interval4=time.time()

    savepath=f'X:/YinQiWenYuan/{filename}.md'
    with open (savepath,'w',encoding='utf-8') as f:
        f.write(f'## {filename}（{len(Data)}/{nums}）\n\n')
        f.write('### Time: '+time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime()))
        f.write('\n\n')
        f.write('|      | 题名 | 作者 | 来源 | 时间 | 链接 |\n')
        f.write('| ---- | ---- | ---- | ---- | ---- | ---- |\n')
        for Dict in Data:
            Count=Dict['Count']
            Title=Dict['Title']
            Author=Dict['Author']
            Origin=Dict['Origin']
            Date=Dict['Date']
            Url=Dict['Url']
            f.write(f'| {Count} | {Title} | {Author} | {Origin} | {Date} | [★]({Url}) |\n')
    print(f'\n存储完毕，程序总用时{round(time.time()-start-(interval4-interval3)-(interval2-interval1),2)}秒。即将打开：{os.path.abspath(savepath)}')
    os.system(savepath)
except Exception as e:
    pyautogui.confirm(title='文献库错误',text=f'高级检索遇到错误，程序已自动终止！\n{e}')
    assert 0