import os
import glob
import markdown
import pytz
from datetime import datetime
import xml.etree.ElementTree as ET

# 定义常量
TRANSLATE_DIR = "translate"
FEED_FILE = "feed.xml"
MAX_ITEMS = 50
TIMEZONE_EST = pytz.timezone('America/New_York')

def convert_md_to_html(md_content):
    """将 Markdown 内容转换为 HTML"""
    return markdown.markdown(md_content)

def create_rss_item(md_file_path):
    """创建单个 RSS 条目"""
    filename = os.path.basename(md_file_path)
    date_str = filename.split('.')[0]  # 假设文件名格式为 YYYYMMDD.md
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_content = convert_md_to_html(md_content)
    pub_date = datetime.now(TIMEZONE_EST).strftime('%a, %d %b %Y %H:%M:%S %z')
    guid = f"POLITICORSS{filename}"
    title = f"POLITICO 每日综述 {date_str}"
    link = f"https://github.com/my_username/my_repo/{date_str}"
    
    return {
        'title': title,
        'link': link,
        'description': html_content,
        'pubDate': pub_date,
        'guid': guid
    }

def build_rss_feed(items, output_file):
    """构建 RSS Feed 并写入文件"""
    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')
    
    ET.SubElement(channel, 'title').text = "POLITICO 每日中文综述"
    ET.SubElement(channel, 'link').text = "https://github.com/your_username/your_repo"
    ET.SubElement(channel, 'description').text = "POLITICO 每日中文综述 RSS"
    ET.SubElement(channel, 'language').text = "zh-cn"
    ET.SubElement(channel, 'lastBuildDate').text = datetime.now(TIMEZONE_EST).strftime('%a, %d %b %Y %H:%M:%S %z')
    
    for item in items:
        item_elem = ET.SubElement(channel, 'item')
        for key, value in item.items():
            if key == 'guid':
                elem = ET.SubElement(item_elem, key, isPermaLink="false")
            else:
                elem = ET.SubElement(item_elem, key)
            elem.text = value
    
    tree = ET.ElementTree(rss)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def update_feed():
    """更新 RSS Feed"""
    md_files = glob.glob(os.path.join(TRANSLATE_DIR, "*.md"))
    new_items = [create_rss_item(md_file) for md_file in md_files]
    
    if os.path.exists(FEED_FILE):
        tree = ET.parse(FEED_FILE)
        root = tree.getroot()
        existing_items = root.find('channel').findall('item')
        existing_items_data = [
            {child.tag: child.text for child in item}
            for item in existing_items
        ]
        
        # 使用字典来去重，确保guid唯一
        all_items_dict = {item['guid']: item for item in existing_items_data}
        for new_item in new_items:
            all_items_dict[new_item['guid']] = new_item
        
        all_items = list(all_items_dict.values())
        all_items = sorted(all_items, key=lambda x: x['pubDate'], reverse=True)[:MAX_ITEMS]
    else:
        all_items = new_items[:MAX_ITEMS]
    
    build_rss_feed(all_items, FEED_FILE)

if __name__ == "__main__":
    update_feed()