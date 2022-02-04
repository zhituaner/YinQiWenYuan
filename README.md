# `.py` 使用说明（v1.0）

:o:本程序为自用，限于精力~~（懒）~~，**当前仅支持Chrome**浏览器，如有其他需求，请自行修改源码。鉴于GitHub上传限制和浏览器种类、版本的多样性，此处不含**selenium浏览器驱动**，请根据**浏览器版本**自行下载【[**Chrome**](http://chromedriver.storage.googleapis.com/index.html)；[**Firefox**](https://github.com/mozilla/geckodriver/releases/)；[**IE**](http://selenium-release.storage.googleapis.com/index.html)】，并将其放在**Python安装目录**下（或添加至**环境变量**）。

## 编写目的概述

[**殷契文渊**](http://jgw.aynu.edu.cn/ajaxpage/home2.0/index.html)，由安阳师范学院甲骨文信息处理教育部重点实验室、中国社会科学院甲骨学殷商史研究中心合作建设而成，收录有蔚为大观的**甲骨著录、甲骨图像和甲骨论著**（持续更新中），在**甲骨学殷商史研究**中具有十分重要的参考价值。本程序旨在利用其**释文检索**功能，在输入检索词后，将所有结果（**目前包括甲骨片号、“拓片细览”详情页链接**）以表格形式写入文件储存，以方便后期初步的整理工作。

## 运行结果示例

以搜索释文“巫”（对释文一般进行模糊搜索）为例，将会在程序同级路径下生成`【殷契文渊】巫.md`：

<img src="https://raw.githubusercontent.com/zhituaner/picBed/master/SearchByText_Example.png" style="zoom:75%;" />

## 局限性及前瞻

1. 因某些错误，暂时无法使用pyinstaller将`.py`打包为`.exe`文件。因此，运行需要**Python环境**。依赖的第三方库：**os**、**selenium**、**pyautogui**。

2. 本程序为自用，目前仅支持**GoogleChrome**，且仅将结果存储为**Markdown**文件（`.md`）~~（说白了就是懒得再写）~~。如有其他需求，需修改`.py`文件源码。

   > 推荐一款非常好用且免费（旧版）的**Markdown**编辑器：**Typora**，[Windows64位免费下载地址](https://zhituaner.lanzouw.com/iSlSKzjyb0j)（密码：3qqm；亦可自行搜索[Typora旧版](https://www.baidu.com/s?ie=UTF-8&wd=typora旧版下载)）

3. 修改代码和处理报错需要具备一定的Python基础。**可能需要修改的地方有：**

   - 变量`time_sleep`：为保证**网页加载完全、数据提取完整**而设定，取决于网速，默认为2秒。

   - 如何支持**其他浏览器**：:one:根据浏览器版本下载相应的**浏览器驱动**；:two:修改两处源码：

     - ```python
       from selenium.webdriver import Chrome
       web=Chrome()
       ```
     
   - 见于其他具体情况的异常，如本程序使用`assert`语句；当**数据提取不完整**时抛出提示等。
   
4. 建议在使用本程序前自行搜索，**以查看结果总页数**，如页数过多（>50）会减小运行的成功率。

5. 源码第一部分为自动登录，因获取所需信息无需登录而全部注释掉。最初编写此部分是为了进入“拓片细览”页面，以批量下载甲骨摹本、照片、拓片等，但发现**实际情况复杂、终究不能脱离网站的丰富信息**，因而仅保存最初设想的功能，只获取**甲骨片号和详情页链接**以便于后期整理。

6. 本程序写于2022年1月，如网站结构后续发生变化，程序可能失效。

