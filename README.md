# Gmail Agent (谷歌邮箱助手智能体)

[![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C.svg?logo=langchain&logoColor=white)](https://www.langchain.com/)
[![Gmail](https://img.shields.io/badge/Gmail-D14836.svg?logo=gmail&logoColor=white)](https://mail.google.com/)
[![Markdown](https://img.shields.io/badge/Markdown-000000.svg?logo=markdown&logoColor=white)](https://daringfireball.net/projects/markdown/)

> 使用 Python | LangChain 结合 Gmail 获取未读邮件.生成 Markdown 文件内容, 支持将邮件标记为已读

## 使用

1. 克隆仓库
2. 去 Google Cloud Console 创建 OAuth 客户端 ID（桌面应用）
3. 把下载的 credentials.json 放项目根目录
4. 安装依赖：pip install - r requirements.txt
5. 运行 python main.py
6. 第一次会弹出浏览器授权，之后自动保存 token
7. 看桌面 Markdown → 输入 y 标记已读 → 收件箱清零！

## 流程

1. 采用 langchain_google_community get_google_credentials 完成 Google Gmail 授权, 授权成功之后,会生成一个 token.json 文件
2. 使用 GmailToolkit 获取未读的 Gmail 邮件列表
3. 将邮件列表 写入 Markdown 文件内. 保存到桌面
4. 支持一键将获取到的邮件标记为已读

## Gmail 授权流程

> 1. <a href="https://developers.google.com/workspace/gmail/api/quickstart/python?hl=zh-cn#authorize_credentials_for_a_desktop_application">开发者授权文档</a>
>
> 2. <a href="https://console.cloud.google.com/auth/clients">授权客户端</a>
>
> 3. <a href="https://console.cloud.google.com/apis/api/gmail.googleapis.com/metrics">授权 Gmail API</a>
