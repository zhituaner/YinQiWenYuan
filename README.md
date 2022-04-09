# :one:`SearchByText.py` 使用说明（v2.0）

## 功能介绍

为最大限度、最高效率地利用**甲骨文数据库**进行研究，本程序已实现在[**殷契文渊**](http://jgw.aynu.edu.cn/)自动化检索释文，获取所有结果的**①甲骨片号、②详情页链接**；确认数据提取完整后，以甲骨片号为线索，进入[**国学大师网**](http://www.guoxuedashi.net/jgwhj/)检索已支持著录的**③释文**，并计算片号中常用著录的**④分期**；接着进入[**殷契文渊缀合库**](http://jgw.aynu.edu.cn/AyjgwZHKSingleSearch?autoLoad=1&id=16&name=ZHUIHEHD&displayDBName=%E7%BC%80%E5%90%88%E6%95%B0%E6%8D%AE%E5%BA%93)检索**⑤缀合片号、⑥缀合链接**，最终将以上信息全部写入Markdown文件存储。**以此程序配合《殷墟甲骨刻辞类纂》等工具书使用**，往往可以收到事半功倍的效果。又，鉴于[汉达文库](http://www.chant.org/)和[史语所甲骨文词汇资料库](https://inscription.asdc.sinica.edu.tw/c_index.php)的局限性，本程序不予使用。

## 使用说明

- 使用Python库：**os、re、time、requests、pyautogui、pprint、zhconv、selenium**

- **当前仅支持Chrome**，且仅将结果存储为**Markdown**文件~~（懒得再写）~~。鉴于GitHub上传限制和浏览器种类、版本的多样性，此处**不含selenium浏览器驱动**，请根据**浏览器版本**自行下载【[**Chrome**](http://chromedriver.storage.googleapis.com/index.html)；[**Firefox**](https://github.com/mozilla/geckodriver/releases/)；[**IE**](http://selenium-release.storage.googleapis.com/index.html)】，并将其放在**Python安装目录**下（或添加至环境变量）

- 需要修改文件**存储路径**`savepath`（在源码末）

- **程序运行成功率显著取决于网速**，内部`time.sleep`绝大多数用于使用**selenium**时，保证网页加载完全、且无法运用`WebDriverWait`的情况。**sleep数值按一般的网速设计**，如频繁因加载原因报错，请检查代码无误后，待网速更好时使用，或增加sleep的数值

- **耗时最多**的部分为在[**殷契文渊缀合库**](http://jgw.aynu.edu.cn/AyjgwZHKSingleSearch?autoLoad=1&id=16&name=ZHUIHEHD&displayDBName=%E7%BC%80%E5%90%88%E6%95%B0%E6%8D%AE%E5%BA%93)检索缀合片号和缀合链接。此处选用selenium，为防止因网速、网页刷新等原因加载失败，使用较多`time.sleep`，每条片号共计2秒（**实际上确认无误后可以直接双击运行**，程序除最初接收输入、弹窗报错、最终打开文件外将**全部在后台运行**，**且一旦弹窗报错将使用assert语句自动终止运行**，~~【划重点】运行时间可以忽略不计~~）

- 以下为正常情况下的所有输出：（已将生成的此文件重命名为`SearchByText结果示例：【殷契文渊】宗.md`并上传）

- ```python
  ★在殷契文渊检索释文“宗”，得到474条结果，共40页。
  ……正在加载第40页……
  ★成功获取数据474条，用时187.96秒。即将开始检索分期（自定义）、释文（国学大师网）：
  ……完成检索释文 474：铁零89……
  ★检索释文完毕，用时63.51秒。
  ★计算分期完毕，用时0.03秒。即将在殷契文渊缀合库检索缀合情况（用时最长）：
  ……完成检索殷契文渊缀合库 474：铁零89……
  ★检索缀合情况完成，用时963.94秒。即将开始写入文件：
  ★存储Markdown完毕，程序总用时20.36分钟。
  即将打开文件：X:\YinQiWenYuan\【殷契文渊】宗.md
  ```

## 版本更新

### v2.0：20220331（最新）

1. :star:增加《甲骨文合集》、《甲骨文合集补编》、《小屯南地甲骨》、《殷墟花园庄东地甲骨》四种著录在[**国学大师网**](http://www.guoxuedashi.net/jgwhj/)检索**释文**的功能【**requests**】
2. :star:增加所有甲骨片号在[**殷契文渊缀合库**](http://jgw.aynu.edu.cn/AyjgwZHKSingleSearch?autoLoad=1&id=16&name=ZHUIHEHD&displayDBName=%E7%BC%80%E5%90%88%E6%95%B0%E6%8D%AE%E5%BA%93)检索**缀合片号和缀合链接**的功能【**selenium**】
3. 增加《卡内基博物馆所藏甲骨研究》、《旅顺博物馆所藏甲骨》自动生成**分期**并写入表格的功能
4. **将存储数据的列表更改为字典**，便于后续修改
5. 增加**运行出错时（函数内部除外）使用pyautogui弹窗报错并使用assert语句自动终止运行**
6. 其他：封装分期计算、存储文件函数；改用`\r`（使用IDLE可能失效），缀合片号只显示前15个字符以美化输出等

### v1.2：20220322

增加《甲骨文合集》、《甲骨文合集补编》自动生成**分期**（董作宾先生五期分法）并写入表格的功能

### v1.1：20220216

1. 将`time.sleep`大部分更改为`selenium.webdriver.support.ui.WebDriverWait`

2. **添加浏览器参数**：无头浏览器、禁止加载图片，以优化运行速度

3. **优化部分代码细节**，如删除登录部分、最终打印文件绝对路径等

# :two:`SearchThesis.py`使用说明

功能：**检索殷契文渊文献库，获取结果中所有文献的题名、作者、来源、发表时间和链接，以便于筛选和阅读。**包含简单检索`SearchThesis_Simple.py`和高级检索`SearchThesis_Advanced.py`，**前者除接收检索条件、弹窗报错外全部在后台运行；后者在前台运行，运行时需保持窗口在最前端。**使用Python库：re、os、time、pyautogui、math、pprint、zhconv、selenium。以下为后者高级检索正常运行时的所有输出，并将生成的文件上传（已重命名为`SearchThesis_Advanced结果示例：【文献库】题名或摘要或关键词：祖先.md`）：

```Python
在殷契文渊文献库进行高级搜索，得到180条结果，共18页。
……开始加载第18／18页……
存储完毕，程序总用时27.65秒。即将打开：X:\YinQiWenYuan\【文献库】题名或摘要或关键词：祖先.md
```

