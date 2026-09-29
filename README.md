# Xiaohang Yang · 学术个人主页

一个可直接上传到 GitHub Pages 的原创静态主页。白底、蓝绿色标题与链接、衬线字体，桌面端双栏，手机端自动调整为单栏。无外部字体、无 JavaScript 依赖、无追踪脚本，也不需要 Jekyll、Hugo 或 Node.js。

## 1. 先预览

解压整个压缩包，双击 `index.html`，用浏览器打开。请保留 `assets` 文件夹和其他 HTML 文件的位置；不要只移动一个 HTML 文件。

导航栏目分别是：Home、Research、Notes & Talks、Teaching、CV。

## 2. 发布之前核对个人信息

当前页面中的姓名为 **Xiaohang Yang**；个人简介按北京大学 / BICMR、数学博士生，以及表示论、自守形式、Langlands 纲领的方向写成初稿。请在公开发布前核对所有表述。

邮箱、中文姓名、照片、办公室、GitHub、ORCID、论文、讲义、课程、详细教育经历和 CV PDF 均未代填。没有提供邮箱时，不显示邮箱栏目；没有提供照片时，显示 `XY` 字母标记；没有提供 CV 文件时，不显示虚假的下载链接。空的材料列表只表示当前网站未列出材料，不表示作者没有相应成果或经历。

上传到公开仓库前，确认文件均可公开。不要上传学生信息、私人通信、未获准公开的合作稿、密码或访问令牌。

## 3. 用 GitHub 网页发布（不用命令行）

1. 登录 GitHub，新建一个仓库。仓库名用 **`你的GitHub用户名.github.io`**，用户名改为你的真实 GitHub 用户名（小写）。这是用户名，不是显示姓名。普通免费账户选择 **Public**，可以勾选添加 README。
2. 在仓库首页，选择 **Add file → Upload files**。上传本文件夹里的文件和子文件夹，然后提交。
3. **`index.html` 必须在仓库根目录。** 不要只上传 ZIP，也不要把整个 `xiaohang-academic-homepage` 文件夹再嵌套到仓库里。
4. 进入 **Settings → Pages → Build and deployment**，把 **Source** 设为 **Deploy from a branch**；Branch 选择 **main**，Folder 选择 **/ (root)**，然后保存。
5. 等待 GitHub 完成部署。官方说明更新可能需要最多约 10 分钟。Pages 设置中会显示站点地址；点击 **Visit site** 查看。

个人主页地址为：

```text
https://你的GitHub用户名.github.io/
```

仓库根目录里的 `.nojekyll` 用于跳过 Jekyll 处理，压缩包已经包含它。在 Mac Finder 中可按 **Command + Shift + .** 显示隐藏文件。上传时一并上传。没有使用任何 GitHub 主题，不需要选择主题或创建 `_config.yml`。

如果该用户名对应的 `username.github.io` 仓库已经存在，先备份旧内容，不要直接覆盖。也可使用普通项目仓库，例如 `academic-homepage`；采用同样的 Pages 设置后，地址通常为 `https://用户名.github.io/academic-homepage/`。本网站使用相对链接，可以放在这个子路径下。

## 4. 以后如何更新

### 推荐：集中修改资料

`site.json` 保存姓名、简介、研究方向和材料列表；`build.py` 会把这些资料写入所有页面，避免反复修改重复信息。

1. 使用纯文本编辑器打开 `site.json`，修改需要的内容。JSON 使用英文双引号，不能写注释，也不要在最后一项后多写逗号。
2. 在这个文件夹里打开终端，运行（需要 Python 3.9 或更高版本，无需额外安装 Python 包）：

   ```bash
   python3 build.py
   ```

3. 再次打开 `index.html` 检查，然后把更新后的 HTML 和相关文件上传到 GitHub。

**只修改 `site.json` 不会自动改变线上页面**；需要运行上面的命令，并提交重新生成的 HTML。本方案故意没有配置自动构建工作流，初次部署不需要处理 Actions 权限或构建环境。

### 也可直接编辑 HTML

如果只是临时改一句话，可以直接编辑对应的 HTML 页面，上传后即生效。但下一次运行 `build.py` 会覆盖这些直接修改。因此，长期维护请以 `site.json` 为准。修改样式只需编辑 `assets/style.css`，不必运行生成器。

## 5. 常用修改示例

### 邮箱与照片

在 `profile` 中填写自己的信息：

```json
"email": "你的真实邮箱",
"photo": "files/portrait.jpg"
```

先把你的照片放到 `files/portrait.jpg`，再运行生成器。照片字段留空就继续使用字母标记；不要把他人的照片当成自己的头像。

其他可选字段包括 `chinese_name`、`office`、`github_url`、`orcid_url`。这些值留空时，对应信息不会显示。

### CV

把已经准备好、可公开的个人简历放到 `files/cv.pdf`，再把 `profile.cv_pdf` 改成：

```json
"cv_pdf": "files/cv.pdf"
```

生成后，CV 页面会出现有效的 PDF 下载链接。

### 添加一篇论文

把 `research.papers` 中的空数组 `[]` 改成条目列表，例如以下**格式示例**（先替换成真实信息再公开，不要把示例当作论文）：

```json
[
  {
    "title": "论文的真实标题",
    "year": "2026",
    "authors": "作者姓名",
    "venue": "Preprint",
    "description": "可选：简短说明。",
    "links": [
      {"label": "PDF", "url": "files/paper.pdf"}
    ]
  }
]
```

PDF 请一并放入相应位置。网页链接可以使用 `https://...`；站内文件用相对路径，例如 `files/paper.pdf`，不要写电脑上的绝对路径。给 `links` 增加条目即可添加 arXiv、Slides、Video 等链接。

`notes.items` 和 `teaching.items` 使用相同结构；教学条目还可设置 `role`（例如你真实担任的课程角色）。`cv.sections` 可以增加带标题的经历栏目，每个栏目有 `title` 和 `items`。

### 修改颜色

在 `assets/style.css` 开头修改：

```css
--accent: #176f73;       /* 标题、链接等的蓝绿色 */
--accent-dark: #10575c;  /* 较深的蓝绿色 */
--accent-soft: #edf5f3;  /* 字母标记的浅色底 */
```

例如更偏绿色可尝试 `#18766d`，更偏蓝色可尝试 `#176b80`。字体通过 CSS 中的 `--serif` 和 `--sans` 设置，调用访客设备已有字体；没有附带任何字体文件。

## 6. 文件结构

```text
index.html          首页
research.html       研究与论文
notes.html          笔记与报告
teaching.html       教学
cv.html             简历
404.html            页面不存在时的提示
assets/style.css    全站样式
files/              存放你要公开的 PDF、照片等
site.json           集中编辑个人资料与各栏目内容
build.py            可选的本地生成器
.nojekyll           跳过 Jekyll 处理
.gitignore          排除常见本地临时文件
README.md           本说明
```

## 7. 官方部署文档

- GitHub Pages 快速入门：<https://docs.github.com/en/pages/quickstart>
- 创建站点与入口文件：<https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site>
- 配置发布来源：<https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>

界面路径按 2026 年 9 月检索到的官方文档整理；界面以后可能调整，以官方说明为准。

设计仅参考了你指定主页的学术信息组织方式（顶部导航、正文和个人信息侧栏）。未复制参考网站的源代码、CSS、照片或个人简介。这些文件尚未部署到你的 GitHub 账户。
