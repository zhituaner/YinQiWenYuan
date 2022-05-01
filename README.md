# `SearchByText.py` 使用说明（v3.1）

## 功能介绍

为最大限度、最高效率地利用**甲骨文数据库**进行研究，本程序已实现在[**殷契文渊**](http://jgw.aynu.edu.cn/)自动化检索释文，获取所有结果的**①甲骨片号、②详情页链接**；确认数据提取完整后，以甲骨片号为线索，进入[**国学大师网**](http://www.guoxuedashi.net/jgwhj/)检索已支持著录的**③释文**，并计算片号中常用著录的**④分期**；接着进入[**殷契文渊缀合库**](http://jgw.aynu.edu.cn/AyjgwZHKSingleSearch?autoLoad=1&id=16&name=ZHUIHEHD&displayDBName=%E7%BC%80%E5%90%88%E6%95%B0%E6%8D%AE%E5%BA%93)、[**先秦史研究室**](https://www.xianqin.org/)检索**⑤缀合片号、⑥缀合链接**，最终将以上信息全部写入**Markdown**文件存储。**以此程序配合《殷墟甲骨刻辞类纂》等工具书使用**，往往可以收到事半功倍的效果。

## 使用说明

- 使用Python库：**os、re、time、requests、pyautogui、pprint、zhconv**

- 需要修改文件**存储路径**`savepath`（在源码末），最终存储为**Markdown**文件（~~懒得写Excel~~）

- 甲骨片号对应链接需要先[**登录殷契文渊**](http://jgw.aynu.edu.cn/Account/Login?ReturnUrl=%2Fajaxpage%2Fhome2.0%2Findex.html)才能正常打开

- 程序除最初接收输入、弹窗报错、最终打开文件外将**全部在后台运行**，**且一旦弹窗报错将使用assert语句自动终止**

- 以下为正常情况下的所有输出：（已将生成的此文件重命名为`SearchByText结果示例.md`并上传）

- ```python
  ★在殷契文渊检索释文“宗”，得到474条结果，共40页。
  ……正在加载第40/40页……
  ★成功获取数据474条，用时49.58秒。即将开始检索分期（自定义）、释文（国学大师网）：
  ……完成检索释文 474/474：铁零89……
  ★检索释文完毕，用时132.08秒。
  ★计算分期完毕，用时0.02秒。即将在殷契文渊/先秦史研究室缀合库检索缀合情况：
  ……完成检索殷契文渊/先秦史研究室缀合库 474/474：铁零89……
  ★检索缀合情况完成，用时588.13秒。即将开始写入文件：
  ★存储Markdown完毕，程序总用时12.86分钟。即将打开文件：X:\YinQiWenYuan\【殷契文渊】宗.md
  ```

## 版本更新

### v3.1：20220501（最新）

隔离时无聊，突然想既然昨晚能把缀合库查询方式由selenium改为requests，那么何不同样修改殷契文渊的释文检索方式，于是花一个小时改好啦（~~其实最初试过但因学艺不精失败了~~）。:star:本次更新彻底将**selenium**改为**requests**，**极大减少运行时间**，**显著增加成功率**。至此，**编写此程序的期望基本已完全达成**。同时希望[**汉达文库**](http://web.chant.org/)、[**史语所甲骨文拓片数据库**](https://ihparchive.ihp.sinica.edu.tw/ihpkmc/ihpkm_op)、[**籍合网殷墟甲骨文数据库**](http://obid.ancientbooks.cn/)的建设将会大有作为！

### v3.0：20220430

1. :star:**将[殷契文渊缀合库](http://jgw.aynu.edu.cn/AyjgwZHKSingleSearch?autoLoad=1&id=16&name=ZHUIHEHD&displayDBName=%E7%BC%80%E5%90%88%E6%95%B0%E6%8D%AE%E5%BA%93)检索方式由selenium改为requests，大大降低所用时间**（约缩短至三分之一）
2. 鉴于[**殷契文渊缀合库**](http://jgw.aynu.edu.cn/AyjgwZHKSingleSearch?autoLoad=1&id=16&name=ZHUIHEHD&displayDBName=%E7%BC%80%E5%90%88%E6%95%B0%E6%8D%AE%E5%BA%93)更新停滞，因此增加在[**先秦史研究室**](https://www.xianqin.org/)网站检索缀合的功能

### v2.0：20220331

1. :star:增加《甲骨文合集》、《甲骨文合集补编》、《小屯南地甲骨》、《殷墟花园庄东地甲骨》四种著录在[**国学大师网**](http://www.guoxuedashi.net/jgwhj/)检索**释文**的功能（当前仅支持此四种。虽然部分生僻字无法显示，**但基本完全满足筛选有用信息的要求**）【**requests**】
2. :star:增加所有甲骨片号在[**殷契文渊缀合库**](http://jgw.aynu.edu.cn/AyjgwZHKSingleSearch?autoLoad=1&id=16&name=ZHUIHEHD&displayDBName=%E7%BC%80%E5%90%88%E6%95%B0%E6%8D%AE%E5%BA%93)检索缀合片号和缀合链接的功能【**selenium**】
3. 增加《卡内基博物馆所藏甲骨研究》、《旅顺博物馆所藏甲骨》自动生成**分期**并写入表格的功能
4. **将存储数据的列表更改为字典**，便于后续修改
5. 增加**运行出错时（函数内部除外）使用pyautogui弹窗报错并使用assert语句自动终止运行**
6. 其他：封装分期计算、存储文件函数；改用`\r`（使用IDLE可能失效），缀合片号只显示前15个字符以美化输出等

### v1.2：20220322

增加《甲骨文合集》、《甲骨文合集补编》自动生成分期并写入表格的功能

### v1.1：20220216

1. 将`time.sleep`大部分更改为`selenium.webdriver.support.ui.WebDriverWait`

2. **添加浏览器参数**：无头浏览器、禁止加载图片，以优化运行速度

3. **优化部分代码细节**，如删除登录部分、最终打印文件绝对路径等

