# `SearchByText.py` 使用说明（v3.0）

## 功能介绍

为最大限度、最高效率地利用**甲骨文数据库**进行研究，本程序已实现在[**殷契文渊**](http://jgw.aynu.edu.cn/)自动化检索释文，获取所有结果的**①甲骨片号、②详情页链接**；确认数据提取完整后，以甲骨片号为线索，进入[**国学大师网**](http://www.guoxuedashi.net/jgwhj/)检索已支持著录的**③释文**，并计算片号中常用著录的**④分期**；接着进入[**殷契文渊缀合库**](http://jgw.aynu.edu.cn/AyjgwZHKSingleSearch?autoLoad=1&id=16&name=ZHUIHEHD&displayDBName=%E7%BC%80%E5%90%88%E6%95%B0%E6%8D%AE%E5%BA%93)、[**先秦史研究室**](https://www.xianqin.org/)检索**⑤缀合片号、⑥缀合链接**，最终将以上信息全部写入**Markdown**表格存储。**以此程序配合《殷墟甲骨刻辞类纂》等工具书使用**，往往可以收到事半功倍的效果。

## 使用说明

- 使用Python库：**os、re、time、requests、pyautogui、pprint、zhconv、selenium**

- **当前仅支持Chrome**，且仅将结果存储为**Markdown**文件（懒得再写）。**需自行下载浏览器驱动**【[**Chrome**](http://chromedriver.storage.googleapis.com/index.html)；[**Firefox**](https://github.com/mozilla/geckodriver/releases/)；[**IE**](http://selenium-release.storage.googleapis.com/index.html)】，并将其放在**Python安装目录**下（或指定路径）

- 需要修改文件**存储路径**`savepath`（在源码末）

- 甲骨片号对应链接需要先[**登录殷契文渊**](http://jgw.aynu.edu.cn/Account/Login?ReturnUrl=%2Fajaxpage%2Fhome2.0%2Findex.html)才能正常打开

- **程序运行成功率显著取决于网速**，内部`time.sleep`绝大多数用于使用**selenium**时，保证网页加载完全、且无法运用`WebDriverWait`的情况。**sleep数值按一般的网速设计**，如频繁因加载原因报错，请检查代码无误后，待网速更好时使用，或增加sleep的数值

- 程序除最初接收输入、弹窗报错、最终打开文件外将**全部在后台运行**，**且一旦弹窗报错将使用assert语句自动终止**

- 以下为正常情况下的所有输出：（已将生成的此文件重命名为`SearchByText结果示例.md`并上传）

- ```python
  ★在殷契文渊检索释文“降”，得到126条结果，共11页。
  ……正在加载第11/11页……
  ★成功获取数据126条，用时34.27秒。即将开始检索分期（自定义）、释文（国学大师网）：
  ……完成检索释文 126/126：辑佚372……
  ★检索释文完毕，用时23.51秒。
  ★计算分期完毕，用时0.0秒。即将在殷契文渊/先秦史研究室缀合库检索缀合情况：
  ……完成检索殷契文渊/先秦史研究室缀合库 126/126：辑佚372……
  ★检索缀合情况完成，用时123.62秒。即将开始写入文件：
  ★存储Markdown完毕，程序总用时3.12分钟。即将打开文件：X:\YinQiWenYuan\【殷契文渊】降.md
  ```

## 版本更新

### v3.0：20220430（最新）

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

