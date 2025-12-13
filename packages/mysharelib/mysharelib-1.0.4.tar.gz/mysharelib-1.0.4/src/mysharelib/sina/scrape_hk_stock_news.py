import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_hk_stock_news(stock_code):
    """
    抓取新浪财经港股个股新闻资讯（修正编码+时间过滤版本）
    参数: stock_code (str) - 港股代码，例如 '00981'
    返回: pandas DataFrame 包含新闻标题、时间、链接
    """
    
    # 构建URL
    url = f"https://stock.finance.sina.com.cn/hkstock/news/{stock_code}.html"
    
    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 发送GET请求
        response = requests.get(url, headers=headers)
        
        # 自动检测编码
        response.encoding = response.apparent_encoding
        
        # 检查请求是否成功
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return None
        
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找新闻列表
        news_items = []
        
        # 查找所有新闻链接
        news_links = soup.find_all('a', href=True)
        
        for link_element in news_links:
            title = link_element.get_text().strip()
            href = link_element['href']
            
            # 跳过无效或过短的标题
            if len(title) < 5:
                continue
                
            # 获取发布时间 - 查找符合时间格式的文本
            time_text = ""
            
            # 在父元素中查找时间
            parent = link_element.parent
            if parent:
                all_text = parent.get_text()
                # 匹配时间格式如 "2025-04-01 13:06:49"
                time_pattern = r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})'
                time_matches = re.findall(time_pattern, all_text)
                
                if time_matches:
                    time_text = time_matches[0]
                else:
                    # 尝试在兄弟元素中查找
                    next_sibling = link_element.find_next_sibling(string=True)
                    if next_sibling:
                        sibling_matches = re.findall(time_pattern, next_sibling)
                        if sibling_matches:
                            time_text = sibling_matches[0]
            
            # **关键修改：严格过滤时间数据**
            # 只保留时间格式正确且非空的数据
            if time_text and re.match(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$', time_text):
                news_items.append({
                    'title': title,
                    'date': time_text,
                    'url': href
                })
            else:
                # 跳过时间为空或格式不正确的数据
                continue
        
        # 创建DataFrame
        if news_items:
            df = pd.DataFrame(news_items, columns=['title', 'date', 'url'])
            
            # 去重
            df = df.drop_duplicates(subset=['title', 'url'])
            
            # 按时间排序
            try:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                # 再次过滤掉无法转换为时间的数据
                df = df.dropna(subset=['date'])
                df = df.sort_values('date', ascending=False)
                df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
            except Exception as e:
                print(f"时间排序时出现错误: {e}")
                return None
            
            #df.set_index('date', inplace=True)
            return df
        else:
            print("未找到有效的时间数据")
            return None
            
    except Exception as e:
        print(f"抓取过程中出现错误: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    stock_code = "00300"  # 中芯国际
    print(f"正在抓取股票代码 {stock_code} 的新闻资讯...")
    
    news_df = scrape_hk_stock_news(stock_code)
    
    if news_df is not None and not news_df.empty:
        print(f"\n成功抓取 {len(news_df)} 条新闻")
        print("=" * 80)
        
        # 显示前15条新闻
        for index, row in news_df.head(15).iterrows():
            print(f"标题: {row['title']}")
            print(f"时间: {row['date']}")
            print(f"链接: {row['url']}")
            print("-" * 80)
    else:
        print("未能抓取到有效的新闻数据")