# POLITICO 中文 RSS 生成器 📰➡️🇨🇳

欢迎使用 POLITICO 中文 RSS 生成器！🎉 这是一个 Python 项目，它会自动抓取 POLITICO 的最新新闻，使用 Gemini API 将其翻译成简体中文，然后生成一个全新的 RSS Feed (`feed.xml`)。更酷的是，它还会将这个中文 RSS Feed 同步到您指定的 GitHub 仓库，方便您随时订阅和分享！

## ✨ 主要功能

*   **自动新闻抓取**: 定期从 POLITICO RSS 源获取最新文章。
*   **智能翻译**: 利用 Google Gemini API 将英文新闻内容高质量翻译为简体中文。
*   **RSS Feed 生成**: 将翻译后的新闻条目构建为标准的 RSS 2.0 Feed (`feed.xml`)。
*   **GitHub 同步**: 自动将生成的 `feed.xml` 推送到您的 GitHub 仓库。
*   **Web 服务**: 通过 Flask 提供一个简单的 Web 服务，可以直接访问生成的 RSS Feed。
*   **定时任务**: 使用 APScheduler 自动执行每日新闻更新和翻译流程。
*   **保持活跃**: 内置 "ping self" 功能，以保持在某些免费托管平台（如 Render）上的服务持续运行。
*   **智能初始化**: 启动时会尝试从 GitHub 同步 `feed.xml`，确保使用最新版本。

## ⚙️ 工作流程

项目大致遵循以下流程：

1.  **抓取 (Parse)**: `rss_parser.py` 脚本从 POLITICO 的 RSS 源抓取新闻，并将每条新闻保存为 Markdown 文件到 `dailynews/` 目录。
2.  **翻译 (Translate)**: `translate_news.py` 脚本检测 `dailynews/` 目录中的新文件，使用 Gemini API 将其内容翻译成中文，并保存到 `translate/` 目录。
3.  **生成 (Generate)**: `generate_rss.py` 脚本读取 `translate/` 目录中的翻译稿件，生成包含这些新闻的 `feed.xml` 文件。
4.  **同步 (Sync)**: `github_sync.py` 脚本将本地的 `feed.xml` 文件推送到您在环境变量中配置的 GitHub 仓库。
5.  **服务 (Serve)**: `app.py` (Flask 应用) 启动后，会运行一个定时任务（默认每天美国东部时间 22:00），自动执行以上1-4步。同时，它还提供 `/feed.xml` 端点供 RSS 阅读器订阅。

## 📂 项目结构

```
.
├── .gitattributes
├── README.md               # 本说明文件
├── app.log                 # 应用运行日志 (自动生成)
├── app.py                  # Flask 主应用，包含定时任务和 Web 服务
├── dailynews/              # 存放从 POLITICO 抓取的原始英文新闻 (Markdown 格式)
│   └── YYYYMMDD.md         # 例如: 20231026.md
├── feed.xml                # 生成的中文 RSS Feed 文件
├── generate_rss.py         # 从翻译后的 Markdown 文件生成 feed.xml
├── github_sync.py          # 同步 feed.xml 到 GitHub 仓库
├── requirements.txt        # Python 依赖库
├── rss_parser.py           # 抓取并解析 POLITICO RSS 源
├── translate/              # 存放翻译后的中文新闻 (Markdown 格式)
│   └── YYYYMMDD.md
└── translate_news.py       # 使用 Gemini API 翻译新闻文件
```

## 📋 环境准备

在开始之前，请确保您的系统已安装：

*   Python 3.7+
*   pip (Python 包安装器)

## 🛠️ 安装与配置

1.  **克隆仓库**:
    ```bash
    git clone https://github.com/your_username/your_repo_name.git
    cd your_repo_name
    ```
    请将 `your_username/your_repo_name` 替换为您自己的 GitHub 用户名和仓库名。

2.  **安装依赖**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **设置环境变量 🔑**:
    项目依赖以下环境变量来正常工作。建议在项目根目录下创建一个 `.env` 文件，并填入您的配置信息。当应用启动时，会自动加载此文件中的变量。

    **`.env` 文件示例:**
    ```env
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    GITHUB_TOKEN="YOUR_GITHUB_TOKEN"
    GITHUB_REPO_URL="https://github.com/your_username/your_rss_repo.git"

    # 可选配置
    # GEMINI_MODEL="gemini-2.5-pro-exp-03-25" # 或其他支持的模型
    # HOST="0.0.0.0"
    # PORT="8080"
    ```

    **环境变量详解:**

    *   `GEMINI_API_KEY`: **必需**。您的 Google Gemini API 密钥。用于翻译新闻文章。您可以从 [Google AI Studio](https://aistudio.google.com/app/apikey) 获取。
    *   `GITHUB_TOKEN`: **必需**。您的 GitHub Personal Access Token (PAT)。需要至少有 `repo` 范围的权限，用于读取和写入 `feed.xml` 到您的 GitHub 仓库。您可以从 GitHub 的开发者设置中创建。
    *   `GITHUB_REPO_URL`: **必需**。您希望存储 `feed.xml` 的目标 GitHub 仓库的完整 URL。例如：`https://github.com/your_username/your_politico_rss_feed.git`。脚本会从此 URL 解析出 `owner` 和 `repo` 名称。
    *   `GEMINI_MODEL`: 可选。指定用于翻译的 Gemini 模型。如果未设置，默认为 `gemini-2.5-pro-exp-03-25` (在 `translate_news.py` 中定义，您可以按需修改默认值或通过此环境变量覆盖)。
    *   `HOST`: 可选。Flask 应用监听的主机地址。默认为 `localhost`。在部署时可能需要设置为 `0.0.0.0`。
    *   `PORT`: 可选。Flask 应用监听的端口号。默认为 `5000`。

    ⚠️ **重要提示**:
    *   `generate_rss.py` 脚本中包含硬编码的 RSS Channel 链接 (`https://github.com/your_username/your_repo`) 和文章链接前缀 (`https://github.com/my_username/my_repo/`). 您可能需要根据您的 `GITHUB_REPO_URL` 手动修改这些值以确保 RSS Feed 中的链接正确。未来版本可能会考虑通过环境变量配置这些。

## 🚀 使用说明

1.  **启动应用服务**:
    配置好 `.env` 文件后，运行主应用：
    ```bash
    python app.py
    ```
    应用启动后：
    *   会立即尝试从 GitHub 同步 `feed.xml`。
    *   启动定时任务，默认在美国东部时间 (EST) 每天 22:00 自动执行完整的新闻更新、翻译、生成 RSS 和同步流程。
    *   启动一个 Flask Web 服务。您可以访问 `http://<HOST>:<PORT>/feed.xml` (例如 `http://localhost:5000/feed.xml`) 来获取 RSS Feed。
    *   首页 `http://<HOST>:<PORT>/` 会提供一个简单的提示页面。

2.  **手动执行脚本 (可选)**:
    如果您想立即执行特定步骤，可以单独运行相应的脚本：
    *   **抓取新闻**:
        ```bash
        python rss_parser.py
        ```
        (注意: `rss_parser.py` 的具体行为和参数可能需要查看其内部实现，当前信息主要基于其在 `app.py` 中的调用方式。)
    *   **翻译新闻**:
        翻译 `dailynews/` 目录下最新的 `.md` 文件：
        ```bash
        python translate_news.py
        ```
        翻译指定文件 (例如 `dailynews/20231026.md`):
        ```bash
        python translate_news.py 20231026
        # 或者
        python translate_news.py 20231026.md
        ```
    *   **生成 RSS Feed**:
        此脚本会处理 `translate/` 目录下的所有 `.md` 文件并更新 `feed.xml`。
        ```bash
        python generate_rss.py
        ```
    *   **同步到 GitHub**:
        此脚本会将本地的 `feed.xml` 推送到 GitHub。
        ```bash
        python github_sync.py
        ```

3.  **订阅 RSS Feed**:
    将 `http://<your_domain_or_ip>:<PORT>/feed.xml` 地址添加到您的 RSS 阅读器中。如果您在本地运行，地址通常是 `http://localhost:5000/feed.xml`。

## ☁️ 部署建议

*   该应用设计为可以部署在支持 Python 的平台上，例如 Heroku, Render, Google Cloud Run 等。
*   `ping_self` 功能有助于在某些免费托管层 (如 Render 的免费 Web 服务) 保持应用唤醒状态，防止因不活跃而休眠。
*   部署时，请确保正确设置了所有必需的环境变量。
*   您可能需要一个 `Procfile` (例如，对于 Heroku 或 Render) 来指定如何启动应用，通常是使用 `gunicorn`:
    ```Procfile
    web: gunicorn app:app
    ```

## 🕰️ 时区和定时任务

*   项目中的日期和时间处理（如文件名、RSS `lastBuildDate`、定时任务触发时间）默认使用美国东部时间 (`America/New_York`)。这是在 `app.py` 和 `generate_rss.py` 中通过 `TIMEZONE_EST` 常量定义的。如果需要更改，可以直接修改代码中的时区设置。
*   每日 RSS 更新任务默认在 `app.py` 中设置为美国东部时间 22:00 执行。您可以根据需要修改 `CronTrigger` 的参数。

## 🤝 贡献

欢迎各种形式的贡献！如果您有任何改进建议或发现了 Bug，请随时创建 Issue 或提交 Pull Request。

1.  Fork 本仓库
2.  创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3.  提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4.  推送到分支 (`git push origin feature/AmazingFeature`)
5.  打开一个 Pull Request