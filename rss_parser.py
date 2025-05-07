import feedparser
import html2text
import os
from datetime import datetime

# 配置项
RSS_FEEDS = [
    "https://rss.politico.com/politics-news.xml",
    "https://rss.politico.com/congress.xml"
]
OUTPUT_DIR = "dailynews" # 输出文件夹名称

def fetch_and_save_rss_news():
    """
    抓取RSS源，解析新闻条目，并按日期保存为Markdown文件。
    """
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 初始化HTML到Markdown转换器
    html_converter = html2text.HTML2Text()
    html_converter.body_width = 0  # 设置为0以避免自动换行，保持原始内容的换行

    # 用于存储按日期分组的新闻条目
    # 结构: {"YYYYMMDD": ["markdown_formatted_news_item_1", "markdown_formatted_news_item_2"]}
    news_by_date = {}

    print("开始处理RSS源...")
    for feed_url in RSS_FEEDS:
        print(f"正在抓取和解析: {feed_url}")
        
        # 解析RSS源
        feed = feedparser.parse(feed_url)

        # 检查解析是否成功（bozo位通常表示格式不佳的源）
        if feed.bozo:
            print(f"警告: RSS源 '{feed_url}' 可能存在格式问题. "
                  f"错误类型: {feed.bozo_exception.__class__.__name__}, "
                  f"原因: {feed.bozo_exception}")

        for entry in feed.entries:
            title = entry.get("title", "无标题")
            link = entry.get("link", "无链接")
            
            # 获取并解析发布日期
            published_time_struct = entry.get("published_parsed")
            if not published_time_struct:
                print(f"警告: 条目 '{title}' ({link}) 缺少发布日期，将跳过。")
                continue
            
            try:
                # time.struct_time -> datetime object -> "YYYYMMDD" string
                dt_object = datetime(*published_time_struct[:6])
                date_str_for_filename = dt_object.strftime("%Y%m%d")
            except ValueError as e:
                print(f"警告: 无法解析条目 '{title}' ({link}) 的发布日期 '{published_time_struct}', "
                      f"错误: {e}，将跳过。")
                continue

            # 提取 <content:encoded> (首选) 或 summary (备选)
            content_html = ""
            if hasattr(entry, 'content') and entry.content:
                # entry.content 是一个列表，通常包含一个字典，其 'value' 键对应 <content:encoded>
                content_html = entry.content[0].get('value', '')
            
            if not content_html and hasattr(entry, 'summary'):
                content_html = entry.summary
            
            if not content_html:
                print(f"警告: 条目 '{title}' ({link}) 既无 <content:encoded> 内容也无 summary，内容将为空。")
            
            # 将HTML内容转换为Markdown
            content_md = html_converter.handle(content_html) if content_html else "无内容"

            # 格式化单个新闻条目的Markdown文本
            news_item_markdown = f"标题：{title}\n链接：{link}\n\n{content_md.strip()}\n\n---\n"

            # 按日期分组
            if date_str_for_filename not in news_by_date:
                news_by_date[date_str_for_filename] = []
            news_by_date[date_str_for_filename].append(news_item_markdown)

    print("\n开始写入新闻到Markdown文件...")
    # 将分组后的新闻写入对应的Markdown文件
    for date_str, items_markdown_list in news_by_date.items():
        filepath = os.path.join(OUTPUT_DIR, f"{date_str}.md")
        print(f"正在写入 {len(items_markdown_list)} 条新闻到: {filepath}")
        try:
            # 使用 "w" 模式，每次运行脚本时会覆盖旧的每日文件，
            # 以确保文件内容总是反映当前RSS源中该日期的所有新闻。
            with open(filepath, "w", encoding="utf-8") as f:
                for item_md in items_markdown_list:
                    f.write(item_md)
            print(f"成功写入到 {filepath}")
        except IOError as e:
            print(f"错误: 无法写入文件 {filepath}. 原因: {e}")

def main():
    """主函数，用于被其他模块调用"""
    fetch_and_save_rss_news()

if __name__ == "__main__":
    main()
    print("\n所有RSS源处理完毕。")