import pandas as pd
import requests
import json
from datetime import datetime

def process_base_data(record: dict) -> dict:
    """
    Process raw financial data record into formatted base data dictionary.
    
    Args:
        record (dict): Raw financial data record from API
    
    Returns:
        dict: Processed and formatted financial data with display names as keys
    """
    # Define the mapping of display names to record keys
    base_data_mapping = {
        '股票代码': 'SECUCODE',
        '证券代码': 'SECURITY_CODE',
        '证券简称': 'SECURITY_NAME_ABBR',
        '报告日期': 'REPORT_DATE',
        '报告类型': 'REPORT_TYPE',
        '基本每股收益(元)': ('EPSJB', 3),
        '扣非每股收益(元)': ('EPSKCJB', 3),
        '稀释每股收益(元)': ('EPSXS', 3),
        '每股净资产(元)': ('BPS', 3),
        '每股资本公积金(元)': ('MGZBGJ', 3),
        '每股未分配利润(元)': ('MGWFPLR', 3),
        '每股经营现金流(元)': ('MGJYXJJE', 3),
        '营业总收入(元)': ('TOTAL_OPERATEINCOME', None),
        '净利润(元)': ('PARENT_NETPROFIT', None),
        '扣非净利润(元)': ('KCFJCXSYJLR', None),
        '净资产收益率(%)': ('ROEJQ', 2, '%'),
        '销售毛利率(%)': ('XSMLL', 2, '%'),
        '资产负债率(%)': ('ZCFZL', 2, '%'),
        '总股本(股)': ('TOTAL_SHARE', None),
        '流通股本(股)': ('FREE_SHARE', None)
    }

    # Create base_data dictionary using a loop
    base_data = {}
    for display_name, field_info in base_data_mapping.items():
        if isinstance(field_info, str):
            # Simple field mapping
            field_key = field_info
            if field_key in record and record[field_key] is not None:
                if field_key == 'REPORT_DATE':
                    base_data[display_name] = record[field_key].split()[0]
                else:
                    base_data[display_name] = record[field_key]
            else:
                base_data[display_name] = 'N/A'
        elif isinstance(field_info, tuple):
            # Formatted field mapping
            field_key = field_info[0]
            decimal_places = field_info[1]
            suffix = field_info[2] if len(field_info) > 2 else ''
            
            if field_key in record and record[field_key] is not None:
                value = record[field_key]
                if decimal_places is not None:
                    if suffix:
                        base_data[display_name] = f"{value:.{decimal_places}f}{suffix}"
                    else:
                        base_data[display_name] = f"{value:.{decimal_places}f}"
                else:
                    base_data[display_name] = f"{value:,}"
            else:
                base_data[display_name] = 'N/A' if not suffix else f"0{suffix}"
    
    return base_data

def get_a_info_em(symbol: str) -> tuple:
    """
    从东方财富网获取指定股票的财务数据，并拆分为基本数据和对比数据两个表格
    
    参数:
    symbol -- 股票代码，格式如"600028.SH"
    
    返回:
    tuple -- (基本数据DataFrame, 对比数据DataFrame)
    """
    # 构建请求URL
    base_url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    params = {
        "reportName": "RPT_PCF10_FINANCEMAINFINADATA",
        "columns": "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,REPORT_DATE,REPORT_TYPE,EPSJB,EPSKCJB,EPSXS,BPS,MGZBGJ,MGWFPLR,MGJYXJJE,TOTAL_OPERATEINCOME,TOTAL_OPERATEINCOME_LAST,PARENT_NETPROFIT,PARENT_NETPROFIT_LAST,KCFJCXSYJLR,KCFJCXSYJLR_LAST,ROEJQ,ROEJQ_LAST,XSMLL,XSMLL_LAST,ZCFZL,ZCFZL_LAST,YYZSRGDHBZC_LAST,YYZSRGDHBZC,NETPROFITRPHBZC,NETPROFITRPHBZC_LAST,KFJLRGDHBZC,KFJLRGDHBZC_LAST,TOTALOPERATEREVETZ,TOTALOPERATEREVETZ_LAST,PARENTNETPROFITTZ,PARENTNETPROFITTZ_LAST,KCFJCXSYJLRTZ,KCFJCXSYJLRTZ_LAST,TOTAL_SHARE,FREE_SHARE,EPSJB_PL,BPS_PL",
        "quoteColumns": "",
        "filter": f"(SECUCODE=\"{symbol}\")",
        "sortTypes": "-1",
        "sortColumns": "REPORT_DATE",
        "pageNumber": "1",
        "pageSize": "1",
        "source": "HSF10",
        "client": "PC",
        "v": str(int(datetime.now().timestamp() * 1000))  # 使用当前时间戳作为随机参数
    }
    
    # 设置请求头
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Connection": "keep-alive",
        "Origin": "https://emweb.securities.eastmoney.com",
        "Referer": "https://emweb.securities.eastmoney.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }
    
    try:
        # Send GET request
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # Check if request was successful
        
        # 解析JSON数据
        data = response.json()
        
        # 检查API返回是否成功
        if not data.get("success", False):
            print(f"API请求失败: {data.get('message', '未知错误')}")
            return pd.DataFrame(), pd.DataFrame()
        
        # 检查是否有数据
        if not data["result"].get("data"):
            print(f"未找到股票 {symbol} 的财务数据")
            return pd.DataFrame(), pd.DataFrame()
        
        # 提取数据记录
        record = data["result"]["data"][0]
        
        # Process the base data
        base_data = process_base_data(record)

        # 财务指标字段映射
        indicators = [
            ('营业总收入', 'TOTAL_OPERATEINCOME', 'TOTAL_OPERATEINCOME_LAST'),
            ('净利润', 'PARENT_NETPROFIT', 'PARENT_NETPROFIT_LAST'),
            ('扣非净利润', 'KCFJCXSYJLR', 'KCFJCXSYJLR_LAST'),
            ('净资产收益率', 'ROEJQ', 'ROEJQ_LAST'),
            ('销售毛利率', 'XSMLL', 'XSMLL_LAST'),
            ('资产负债率', 'ZCFZL', 'ZCFZL_LAST'),
            ('营业收入同比增长率', 'YYZSRGDHBZC', 'YYZSRGDHBZC_LAST'),
            ('净利润同比增长率', 'NETPROFITRPHBZC', 'NETPROFITRPHBZC_LAST'),
            ('扣非净利润同比增长率', 'KFJLRGDHBZC', 'KFJLRGDHBZC_LAST'),
            ('营业总收入环比增长率', 'TOTALOPERATEREVETZ', 'TOTALOPERATEREVETZ_LAST'),
            ('净利润环比增长率', 'PARENTNETPROFITTZ', 'PARENTNETPROFITTZ_LAST'),
            ('扣非净利润环比增长率', 'KCFJCXSYJLRTZ', 'KCFJCXSYJLRTZ_LAST'),
        ]

        def safe_divide(a, b):
            if a is None or b is None: return None
            return (a - b) / b * 100 if b != 0 else 0

        def format_value(name, value, is_percent=False):
            #print(name, value, is_percent)
            if value is None:
                return value
            if is_percent:
                return f"{value:.2f}%"
            else:
                return f"{value:,}"

        comparison_data = {
            '指标': [name for name, _, _ in indicators],
            '本期值': [
                format_value(name, record.get(curr, 0), is_percent=name in [
                    '净资产收益率', '销售毛利率', '资产负债率',
                    '营业收入同比增长率', '净利润同比增长率', '扣非净利润同比增长率',
                    '营业总收入环比增长率', '净利润环比增长率', '扣非净利润环比增长率'
                ])
                for name, curr, _ in indicators
            ],
            '上期值': [
                format_value(name, record.get(last, 0), is_percent=name in [
                    '净资产收益率', '销售毛利率', '资产负债率',
                    '营业收入同比增长率', '净利润同比增长率', '扣非净利润同比增长率',
                    '营业总收入环比增长率', '净利润环比增长率', '扣非净利润环比增长率'
                ])
                for name, _, last in indicators
            ],
            '变化率': [
                format_value(name,
                    safe_divide(record.get(curr, 0), record.get(last, 0)),
                    is_percent=True
                )
                for name, curr, last in indicators
            ]
        }
        
        # 创建DataFrame
        df_base = pd.DataFrame([base_data]).T
        df_comparison = pd.DataFrame(comparison_data)
        df_base.index.name = "指标"
        df_base.rename(columns={0: "数值"}, inplace=True)
        
        return df_base, df_comparison
    
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return pd.DataFrame(), pd.DataFrame()
    except json.JSONDecodeError:
        print("响应解析失败")
        return pd.DataFrame(), pd.DataFrame()
    except KeyError as e:
        print(f"数据解析错误: {e}")
        return pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        print(f"发生未知错误: {e}")
        return pd.DataFrame(), pd.DataFrame()

# 使用示例
if __name__ == "__main__":
    # 获取中国石化的财务数据
    df_base, df_comparison = get_a_info_em("600036.SH")
    
    if not df_base.empty:
        # 打印基本数据
        print("基本财务数据:")
        print(df_base)
        
        # 打印对比数据
        print("\n财务数据对比:")
        print(df_comparison)
        
        # 保存到Excel文件
        filename = f"log/{df_base.iloc[2]['数值']}.xlsx"
        with pd.ExcelWriter(filename) as writer:
            df_base.to_excel(writer, sheet_name="基本数据", index=False)
            df_comparison.to_excel(writer, sheet_name="对比数据", index=False)
        print(f"数据已保存到 {filename}")
    else:
        print("未能获取数据")