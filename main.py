import os
from datetime import datetime
from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import(
    build_gmail_service,
    get_google_credentials,
)

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def authenticate_gmail():
    """授权"""

    creds = get_google_credentials(
        token_file="token.json",
        scopes=SCOPES,
        client_secrets_file="credentials.json",
    )
    service = build_gmail_service(creds)
    return service


def unread_emails():
    """获取未读邮件"""

    try:
        service = authenticate_gmail()
        gmail_toolkit = GmailToolkit(service=service)
        tools = gmail_toolkit.get_tools()

        search_tool = None
        for tool in tools:
            if "search" in tool.name.lower() and "gmail" in tool.name.lower():
                search_tool = tool
                break

        if not search_tool:
            print("未找到搜索工具，可用工具：", [t.name for t in tools])
            return []
        
        query = "is:unread"
        result = search_tool.run({
            "query": query,
            "max_results": 10,
        })

        if not result:
            print("没有未读邮件")
            return []

        if isinstance(result, str):
            print("返回的是字符串")
            return []
        
        elif isinstance(result, list):
            print(f"成功获取 {len(result)} 封未读邮件")
            emails = []
            for email in result:
                emails.append({
                    "subject": email.get("subject", "（无主题）"),
                    "sender": email.get("from", "未知发件人"),
                    "date": email.get("date", "未知日期"),
                    "snippet": email.get("snippet", ""),
                    "message_id": email.get("id", ""),
                })
            return emails

        else:
            print(f"未知返回类型：{type(result)}")
            return []
        
    except Exception as e:
        print(f"获取未读邮件时出错: {e}")
        return []

def write_to_markdown(emails, filename=None):
    """将未读邮件列表写入 Markdown 文件，保存到 macOS 桌面"""

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"unread_emails_{timestamp}.md"
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
    
    try: 
        with open(desktop_path, "w", encoding="utf-8") as f:
            now_str = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
            f.write("# 📬 未读邮件汇总\n\n")
            f.write(f"**更新时间**: {now_str}\n\n")
            f.write(f"**未读邮件总数**: {len(emails)} 封\n\n")
            f.write("---\n\n")

            if len(emails) == 0:
                f.write("> 🎉 恭喜！收件箱已清空，没有未读邮件。\n")
            else:
                for i, email in enumerate(emails, 1):
                    subject = email.get("subject", "（无主题）")
                    sender = email.get("sender", "未知发件人")
                    date = email.get("date", "未知日期")
                    snippet = email.get("snippet", "无预览内容")

                    f.write(f"### {i}. {subject}\n\n")
                    f.write(f"- **发件人**: {sender}\n")
                    f.write(f"- **日期**: {date}\n")
                    f.write(f"- **预览**: {snippet}\n\n")
                    f.write("---\n\n")

        print(f"✅ 未读邮件已成功保存到桌面：")
        print(f"   {desktop_path}")          

    except Exception as e:
        print(f"❌ 写入 Markdown 文件失败: {e}")

def mark_unread_as_read(emails):
    """标记已读"""

    if not emails:
        print("没有未读邮件，无需标记。")
        return True
    
    try:
        service = authenticate_gmail()
        
        message_ids = [email["message_id"] for email in emails if email.get("message_id")]
        if not message_ids:
            print("邮件列表中缺少 message_id,无法标记已读。")
            return False
        
        print(f"正在将 {len(message_ids)} 封未读邮件标记为已读...")

        body = {
            "ids": message_ids,
            "removeLabelIds": ["UNREAD"]
        }
        service.users().messages().batchModify(
            userId="me",
            body=body
        ).execute()

        print("✅ 所有未读邮件已成功标记为已读！")
        return True

    except Exception as e:
        print(f"❌ 标记已读时出错: {e}")
        import traceback
        traceback.print_exc()
        return False  

def main():
    emails = unread_emails()
    write_to_markdown(emails=emails)

    print("\n是否要将这些未读邮件全部标记为已读?")
    print("输入 y 或 yes 确认，其他任意键取消: ")
    choice = input("> ").strip().lower()
    if choice in ["y", "yes", "是"]:
        mark_unread_as_read(emails)
    else:
        print("已取消标记已读操作。未读邮件保持原样。")

if __name__ == "__main__":
    main()   
