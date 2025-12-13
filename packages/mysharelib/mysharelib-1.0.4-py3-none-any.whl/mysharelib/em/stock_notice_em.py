import pandas as pd
import requests
import json
from typing import Optional


def stock_notice_em(symbol: str = "600325", page_size: int = 20) -> pd.DataFrame:
    """
    从东方财富网获取指定股票的公告信息
    
    参数:
    symbol -- 股票代码，如"600325"
    page_size -- 每页返回的公告数量，默认20条
    
    返回:
    pd.DataFrame -- 包含公告信息的DataFrame，列包括：
                    - 标题: 公告标题
                    - 发布时间: 发布时间
                    - 分类: 来源/分类
                    - 链接: 文章链接
    """
    # 构建请求URL
    base_url = "https://np-anotice-stock.eastmoney.com/api/security/ann"
    
    # 构建请求参数
    params = {
        "sr": "-1",
        "page_size": str(page_size),
        "page_index": "1",
        "ann_type": "A",
        "client_source": "web",
        "stock_list": symbol,
        "f_node": "0",
        "s_node": "0"
    }
    
    # 设置请求头，严格按照curl命令配置
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Connection": "keep-alive",
        "Origin": "https://data.eastmoney.com",
        "Referer": "https://data.eastmoney.com/stockcomment/stock/600325.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
        "sec-ch-ua": '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }
    
    try:
        # 发送GET请求，设置超时时间
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # 检查HTTP错误状态码
        
        # 解析JSON数据
        data = response.json()
        
        # 检查API返回的数据结构
        if "data" not in data or "list" not in data["data"]:
            print(f"API返回数据结构异常: {data}")
            return pd.DataFrame(columns=["标题", "发布时间", "分类", "链接"])
        
        # 提取公告列表
        announcements = data["data"]["list"]
        
        # 检查是否有数据
        if not announcements:
            print(f"未找到股票 {symbol} 的公告数据")
            return pd.DataFrame(columns=["title", "notice_date", "column_name", "article_link"])
        
        # 解析数据并构建DataFrame
        records = []
        for item in announcements:
            # 提取标题（优先使用中文标题）
            title = item.get("title_ch") or item.get("title", "")
            
            # 提取发布时间
            notice_date = item.get("notice_date", "")
            
            # 提取来源/分类（取第一个分类）
            columns_list = item.get("columns", [])
            column_name = columns_list[0].get("column_name", "") if columns_list else ""
            
            # 构建文章链接
            art_code = item.get("art_code", "")
            # 从codes列表中获取stock_code
            codes_list = item.get("codes", [])
            stock_code = codes_list[0].get("stock_code", symbol) if codes_list else symbol
            article_link = f"https://data.eastmoney.com/notices/detail/{stock_code}/{art_code}.html"
            
            records.append({
                "标题": title,
                "发布时间": notice_date,
                "分类": column_name,
                "链接": article_link
            })
        
        # 创建DataFrame
        df = pd.DataFrame(records)
        return df
    
    except requests.exceptions.Timeout:
        print(f"请求超时: 连接 {base_url} 超时")
        return pd.DataFrame(columns=["title", "notice_date", "column_name", "article_link"])
    except requests.exceptions.ConnectionError as e:
        print(f"网络连接错误: {e}")
        return pd.DataFrame(columns=["title", "notice_date", "column_name", "article_link"])
    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误: {e}")
        return pd.DataFrame(columns=["title", "notice_date", "column_name", "article_link"])
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return pd.DataFrame(columns=["title", "notice_date", "column_name", "article_link"])
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        return pd.DataFrame(columns=["title", "notice_date", "column_name", "article_link"])
    except KeyError as e:
        print(f"数据解析错误，缺少关键字段: {e}")
        return pd.DataFrame(columns=["title", "notice_date", "column_name", "article_link"])
    except Exception as e:
        print(f"发生未知错误: {e}")
        return pd.DataFrame(columns=["title", "notice_date", "column_name", "article_link"])


# 使用示例
if __name__ == "__main__":
    # 获取华发股份（600325）的公告信息
    df = stock_notice_em(symbol="600325", page_size=5)
    
    if not df.empty:
        print("华发股份公告信息:")
        print(df)
        print(f"\n共获取 {len(df)} 条公告")
        print(f"\n示例文章链接: {df.iloc[0]['链接']}")
    else:
        print("未能获取数据")
