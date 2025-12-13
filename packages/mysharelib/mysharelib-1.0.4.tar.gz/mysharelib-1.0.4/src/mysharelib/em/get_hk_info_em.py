import requests
import pandas as pd
import time
from typing import Tuple

def get_hk_info_em(symbol: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    获取港股基本信息和与上年同期对比的数据
    
    参数:
    symbol (str): 股票代码，例如 '01088.HK'
    
    返回:
    Tuple[pd.DataFrame, pd.DataFrame]: 
        - 第一个DataFrame: 基本数据表格
        - 第二个DataFrame: 与上年同期对比的数据表格
    """
    # 构建URL
    base_url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    
    # 生成随机v参数，使用当前时间戳
    v_param = str(int(time.time() * 1000))
    
    # 参数
    params = {
        "reportName": "RPT_CUSTOM_HKF10_FN_MAININDICATORMAX",
        "columns": "ORG_CODE,SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,SECURITY_INNER_CODE,REPORT_DATE,BASIC_EPS,PER_NETCASH_OPERATE,BPS,BPS_NEDILUTED,COMMON_ACS,PER_SHARES,ISSUED_COMMON_SHARES,HK_COMMON_SHARES,TOTAL_MARKET_CAP,HKSK_MARKET_CAP,OPERATE_INCOME,OPERATE_INCOME_SQ,OPERATE_INCOME_QOQ,OPERATE_INCOME_QOQ_SQ,HOLDER_PROFIT,HOLDER_PROFIT_SQ,HOLDER_PROFIT_QOQ,HOLDER_PROFIT_QOQ_SQ,PE_TTM,PE_TTM_SQ,PB_TTM,PB_TTM_SQ,NET_PROFIT_RATIO,NET_PROFIT_RATIO_SQ,ROE_AVG,ROE_AVG_SQ,ROA,ROA_SQ,DIVIDEND_TTM,DIVIDEND_LFY,DIVI_RATIO,DIVIDEND_RATE,IS_CNY_CODE",
        "quoteColumns": "",
        "filter": f"(SECUCODE=\"{symbol}\")",
        "pageNumber": "1",
        "pageSize": "1",
        "sortTypes": "-1",
        "sortColumns": "REPORT_DATE",
        "source": "F10",
        "client": "PC",
        "v": v_param  # 使用动态生成的v参数
    }
    
    # 请求头
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6',
        'Connection': 'keep-alive',
        'Origin': 'https://emweb.securities.eastmoney.com',
        'Referer': 'https://emweb.securities.eastmoney.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    
    try:
        # 发送请求
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析JSON
        data = response.json()
        
        # 检查数据是否有效
        if data.get('result') is None or data['result'].get('data') is None or len(data['result']['data']) == 0:
            raise ValueError(f"未找到 {symbol} 的数据")
        
        # 获取第一条记录
        stock_data = data['result']['data'][0]
        
        # 辅助函数：格式化数字
        def format_number(value, is_shares=False, is_market_cap=False):
            if value is None or value == "":
                return "--"
            
            try:
                num = float(value)
                if is_shares and num > 100000000:
                    return f"{num/100000000:.2f}亿"
                elif is_market_cap and num > 100000000:
                    return f"{num/100000000:.2f}亿"
                elif is_market_cap and num > 10000:
                    return f"{num/10000:.2f}万"
                else:
                    return str(num)
            except (ValueError, TypeError):
                return str(value)
        
        # 辅助函数：格式化财务数据（收入、利润等）
        def format_financial(value, is_income=False):
            if value is None or value == "":
                return "--"
            
            try:
                num = float(value)
                if is_income and num >= 100000000:
                    return f"{num/100000000:.2f}亿"
                elif is_income and num >= 10000:
                    return f"{num/10000:.2f}万"
                else:
                    return str(num)
            except (ValueError, TypeError):
                return str(value)
        
        # 辅助函数：格式化百分比
        def format_percentage(value):
            if value is None or value == "":
                return "--"
            
            try:
                num = float(value)
                return f"{num:.2f}"
            except (ValueError, TypeError):
                return str(value)
        
        # 辅助函数：格式化比率
        def format_ratio(value):
            if value is None or value == "":
                return "--"
            
            try:
                num = float(value)
                return f"{num:.2f}"
            except (ValueError, TypeError):
                return str(value)
        
        # 定义基本数据表格
        basic_data = [
            ["基本每股收益(元)", format_number(stock_data.get("BASIC_EPS"))],
            ["每股股息TTM(港元)", format_number(stock_data.get("DIVIDEND_TTM"))],
            ["每股经营现金流(元)", format_number(stock_data.get("PER_NETCASH_OPERATE"))],
            ["每股净资产(元)", format_number(stock_data.get("BPS"))],
            ["派息比率(%)", format_percentage(stock_data.get("DIVI_RATIO"))],
            ["股息率TTM(%)", format_percentage(stock_data.get("DIVIDEND_RATE"))],
            ["已发行股本(股)", format_number(stock_data.get("ISSUED_COMMON_SHARES"), is_shares=True)],
            ["总市值(港元)", format_number(stock_data.get("TOTAL_MARKET_CAP"), is_market_cap=True)],
            ["已发行股本-H股(股)", format_number(stock_data.get("HK_COMMON_SHARES"), is_shares=True)],
            ["港股市值(港元)", format_number(stock_data.get("HKSK_MARKET_CAP"), is_market_cap=True)]
        ]
        
        # 创建基本数据DataFrame
        basic_df = pd.DataFrame(basic_data, columns=["指标", "数值"])
        basic_df.set_index("指标", inplace=True)
        
        # 定义与上年同期对比的数据表格
        comparison_data = [
            ["营业总收入(亿元)", format_financial(stock_data.get("OPERATE_INCOME"), is_income=True), 
             format_financial(stock_data.get("OPERATE_INCOME_SQ"), is_income=True)],
            ["营业总收入滚动环比增长(%)", format_percentage(stock_data.get("OPERATE_INCOME_QOQ")), 
             format_percentage(stock_data.get("OPERATE_INCOME_QOQ_SQ"))],
            ["销售净利率(%)", format_percentage(stock_data.get("NET_PROFIT_RATIO")), 
             format_percentage(stock_data.get("NET_PROFIT_RATIO_SQ"))],
            ["净利润(亿元)", format_financial(stock_data.get("HOLDER_PROFIT"), is_income=True), 
             format_financial(stock_data.get("HOLDER_PROFIT_SQ"), is_income=True)],
            ["净利润滚动环比增长(%)", format_percentage(stock_data.get("HOLDER_PROFIT_QOQ")), 
             format_percentage(stock_data.get("HOLDER_PROFIT_QOQ_SQ"))],
            ["股东权益回报率(%)", format_percentage(stock_data.get("ROE_AVG")), 
             format_percentage(stock_data.get("ROE_AVG_SQ"))],
            ["市盈率TTM(倍)", format_ratio(stock_data.get("PE_TTM")), 
             format_ratio(stock_data.get("PE_TTM_SQ"))],
            ["市净率MRQ(倍)", format_ratio(stock_data.get("PB_TTM")), 
             format_ratio(stock_data.get("PB_TTM_SQ"))],
            ["总资产回报率(%)", format_percentage(stock_data.get("ROA")), 
             format_percentage(stock_data.get("ROA_SQ"))]
        ]
        
        # 创建与上年同期对比的DataFrame
        comparison_df = pd.DataFrame(comparison_data, columns=["指标", "本期值", "上期值"])
        
        return basic_df, comparison_df
    
    except Exception as e:
        print(f"获取数据时出错: {e}")
        # 返回空的DataFrame
        return pd.DataFrame(columns=["指标", "数值"]), pd.DataFrame(columns=["指标", "本期值", "上期值"])

# 使用示例
if __name__ == "__main__":
    # 获取中国神华(01088.HK)的数据
    basic_df, comparison_df = get_hk_info_em("02800.HK")
    
    print("===== 基本数据 =====")
    print(basic_df)
    
    print("\n===== 与上年同期对比的数据 =====")
    print(comparison_df)