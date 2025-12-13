import pandas as pd
import requests
import json
from typing import Optional


def stock_report_em(symbol: str = "600325", begin_time: str = "2025-01-01", end_time: str = "2025-12-04", page_size: int = 20) -> pd.DataFrame:
    """
    从东方财富网获取指定股票的研报信息
    
    参数:
    symbol -- 股票代码，如"600325"
    begin_time -- 开始日期，格式"YYYY-MM-DD"
    end_time -- 结束日期，格式"YYYY-MM-DD"
    page_size -- 每页返回的研报数量，默认20条
    
    返回:
    pd.DataFrame -- 包含研报信息的DataFrame，列包括：
                    - 报告名称: 报告标题
                    - 东财评级: 东方财富评级
                    - 评级变动: 上一次评级
                    - 机构: 研究机构名称
                    - 日期: 发布日期
                    - article_link: 文章链接
    """
    # 构建请求URL
    base_url = "https://reportapi.eastmoney.com/report/list"
    
    # 构建请求参数
    params = {
        "pageNo": "1",
        "pageSize": str(page_size),
        "code": symbol,
        "industryCode": "*",
        "industry": "*",
        "rating": "*",
        "ratingchange": "*",
        "beginTime": begin_time,
        "endTime": end_time,
        "fields": "",
        "qType": "0",
        "sort": "publishDate,desc"
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
        if "data" not in data:
            print(f"API返回数据结构异常: {data}")
            return pd.DataFrame(columns=["报告名称", "东财评级", "评级变动", "机构", "日期", "文章链接"])
        
        # 提取研报列表
        reports = data["data"]
        
        # 检查是否有数据
        if not reports:
            print(f"未找到股票 {symbol} 在 {begin_time} 至 {end_time} 期间的研报数据")
            return pd.DataFrame(columns=["报告名称", "东财评级", "评级变动", "机构", "日期", "文章链接"])
        
        # 解析数据并构建DataFrame
        records = []
        for item in reports:
            # 提取报告名称
            title = item.get("title", "")
            
            # 提取东财评级
            em_rating_name = item.get("emRatingName", "")
            
            # 提取评级变动（上一次评级）
            last_em_rating_name = item.get("lastEmRatingName", "")
            
            # 提取机构名称
            org_name = item.get("orgName", "")
            
            # 提取发布日期
            publish_date = item.get("publishDate", "")
            
            # 构建文章链接
            info_code = item.get("infoCode", "")
            article_link = f"https://data.eastmoney.com/report/info/{info_code}.html" if info_code else ""
            
            records.append({
                "报告名称": title,
                "东财评级": em_rating_name,
                "评级变动": last_em_rating_name,
                "机构": org_name,
                "日期": publish_date,
                "文章链接": article_link
            })
        
        # 创建DataFrame
        df = pd.DataFrame(records)
        return df
    
    except requests.exceptions.Timeout:
        print(f"请求超时: 连接 {base_url} 超时")
        return pd.DataFrame(columns=["报告名称", "东财评级", "评级变动", "机构", "日期", "文章链接"])
    except requests.exceptions.ConnectionError as e:
        print(f"网络连接错误: {e}")
        return pd.DataFrame(columns=["报告名称", "东财评级", "评级变动", "机构", "日期", "文章链接"])
    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误: {e}")
        return pd.DataFrame(columns=["报告名称", "东财评级", "评级变动", "机构", "日期", "文章链接"])
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return pd.DataFrame(columns=["报告名称", "东财评级", "评级变动", "机构", "日期", "文章链接"])
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        return pd.DataFrame(columns=["报告名称", "东财评级", "评级变动", "机构", "日期", "文章链接"])
    except KeyError as e:
        print(f"数据解析错误，缺少关键字段: {e}")
        return pd.DataFrame(columns=["报告名称", "东财评级", "评级变动", "机构", "日期", "文章链接"])
    except Exception as e:
        print(f"发生未知错误: {e}")
        return pd.DataFrame(columns=["报告名称", "东财评级", "评级变动", "机构", "日期", "文章链接"])


# 使用示例
if __name__ == "__main__":
    # 获取华发股份（600325）的研报信息
    df = stock_report_em(symbol="600325", begin_time="2025-01-01", end_time="2025-12-04", page_size=10)
    
    if not df.empty:
        print("华发股份研报信息:")
        print(df)
        print(f"\n共获取 {len(df)} 条研报")
        print(f"\n示例文章链接: {df.iloc[0]['文章链接']}")
    else:
        print("未能获取数据")
