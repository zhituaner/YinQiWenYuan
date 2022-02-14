# `SearchByText.py` 使用说明（v1.1）

## 编写目的

[**殷契文渊**](http://jgw.aynu.edu.cn/ajaxpage/home2.0/index.html)，由安阳师范学院甲骨文信息处理教育部重点实验室、中国社会科学院甲骨学殷商史研究中心合作建设而成，收录有蔚为大观的**甲骨著录、甲骨图像和甲骨论著**（持续更新中），在**甲骨学殷商史研究**中具有十分重要的参考价值。本程序旨在利用其**释文检索**功能，在输入检索词后，将所有结果（**目前包括甲骨片号、“拓片细览”详情页链接**）以表格形式写入文件储存，以方便后期初步的整理工作。

## 运行示例

以搜索释文“巫”（对释文一般进行模糊搜索）为例，将会在程序同级路径下生成`【殷契文渊】巫.md`：

<img src="https://raw.githubusercontent.com/zhituaner/picBed/master/SearchByText_Example.png" style="zoom:75%;" />

## 使用说明

- :heavy_exclamation_mark:暂时无法使用pyinstaller将`.py`打包为`.exe`文件，运行需要**Python环境**。依赖的第三方库：**os**、**selenium**、**pyautogui**。

- :heavy_exclamation_mark:本程序为自用，**当前仅支持Chrome**，且仅将结果存储为**Markdown**文件（`.md`）~~（懒得再写）~~。如有其他需求，请自行修改源码（见下）。鉴于GitHub上传限制和浏览器种类、版本的多样性，此处**不含selenium浏览器驱动**，请根据**浏览器版本**自行下载【[**Chrome**](http://chromedriver.storage.googleapis.com/index.html)；[**Firefox**](https://github.com/mozilla/geckodriver/releases/)；[**IE**](http://selenium-release.storage.googleapis.com/index.html)】，并将其放在**Python安装目录**下（或添加至**环境变量**）。

  ```python
  from selenium.webdriver import Chrome
  from selenium.webdriver.chrome.options import Options
  web=Chrome(options=opt)
  ```

  > 推荐一款非常好用且免费（旧版）的**Markdown**编辑器：**Typora**，[Windows64位免费下载地址](https://zhituaner.lanzouw.com/iSlSKzjyb0j)（密码：3qqm；亦可自行搜索[Typora旧版](https://www.baidu.com/s?ie=UTF-8&wd=typora旧版下载)）

- 建议在使用本程序前自行搜索，**以查看结果总页数**，如页数过多（>50）可能会减小运行的成功率。

- 其他可能需要修改处：见于具体情况的异常，如本程序使用`assert`语句；当**数据提取不完整**时抛出提示等。

- v1.0第一部分为自动登录，因获取所需信息无需登录而全部注释掉。最初编写此部分是为了进入“拓片细览”页面，以**批量下载**甲骨摹本、照片、拓片等，但发现**实际情况复杂、终究不能脱离网站的丰富信息**，因而仅保存最初设想的功能，只获取**甲骨片号和详情页链接**以便于后期整理。

- 本程序写于2022年1月，如网站结构后续发生变化，程序可能失效。

## 版本更新

### v1.1（当前）

1. 为保证网页加载完全，v1.0使用大量`time.sleep`，降低了灵活性和运行速度，现更改为`selenium.webdriver.support.ui.WebDriverWait`。

   > 注：笔者尚不清楚**翻页后如何判断网页是否加载完全**，因而在翻页后暂时仍保留`time.sleep(2)`。

2. 添加浏览器参数：**无头浏览器**、**禁止加载图片**，以优化运行速度。

3. 优化部分代码细节，如**删除登录部分**、**最终打印文件绝对路径**等。
