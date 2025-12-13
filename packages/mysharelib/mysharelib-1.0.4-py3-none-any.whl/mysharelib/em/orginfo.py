import requests
import pandas as pd
from datetime import (
    date as dateType,
    datetime,
    timedelta
)

def get_a_orginfo_em(symbol: str) -> pd.DataFrame:
    """
    获取A股公司概况数据 (RPT_F10_BASIC_ORGINFO)

    Args:
        symbol (str): 股票代码，例如 '600028.SH'

    Returns:
        pd.DataFrame: 包含公司概况数据的DataFrame。
    """
    # 构建URL，注意reportName是 RPT_F10_BASIC_ORGINFO
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    params = {
        'reportName': 'RPT_F10_BASIC_ORGINFO',
        # 根据示例URL和返回数据，columns需要包含所有需要的字段
        # 这里列出一些关键字段，可根据需要增减
        'columns': 'SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,ORG_NAME,ORG_NAME_EN,FORMERNAME,LEGAL_PERSON,PRESIDENT,CHAIRMAN,SECRETARY,REG_CAPITAL,ADDRESS,REG_ADDRESS,PROVINCE,ORG_TEL,ORG_EMAIL,ORG_WEB,ORG_PROFILE,BUSINESS_SCOPE,MAIN_BUSINESS,TRADE_MARKET,INDUSTRYCSRC1,EMP_NUM,FOUND_DATE,LISTING_DATE',
        'quoteColumns': '',
        'filter': f'(SECUCODE="{symbol}")',
        'pageNumber': '1',
        'pageSize': '1', # 假设每家公司只有一条概况记录
        'source': 'HSF10',
        'client': 'PC'
        # 注意：示例curl中的v参数可能是动态生成的token或时间戳，
        # 在直接请求中可能不是必需的，或者需要动态获取。
        # 如果遇到问题，可以尝试添加 'v': '...' 或者省略。
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6',
        'Connection': 'keep-alive',
        'Origin': 'https://emweb.securities.eastmoney.com',
        'Referer': 'https://emweb.securities.eastmoney.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # 如果状态码不是200，会抛出异常

        data_json = response.json()

        if data_json.get('success') and 'result' in data_json and 'data' in data_json['result']:
            data_list = data_json['result']['data']
            if data_list:
                # 将列表数据转换为DataFrame
                df = pd.DataFrame(data_list)
                return df
            else:
                print(f"未找到股票代码为 {symbol} 的公司概况数据。")
                # 返回一个空的DataFrame，列名与请求的字段一致
                return pd.DataFrame(columns=[col.strip() for col in params['columns'].split(',')])
        else:
            print(f"API请求未成功或返回数据格式不符。消息: {data_json.get('message', 'N/A')}")
            return pd.DataFrame() # 返回空DataFrame

    except requests.exceptions.RequestException as e:
        print(f"请求过程中发生错误: {e}")
        return pd.DataFrame() # 返回空DataFrame
    except ValueError as e: # 捕获json解析错误
        print(f"解析JSON数据时发生错误: {e}")
        print(f"响应内容: {response.text}") # 打印响应内容以便调试
        return pd.DataFrame() # 返回空DataFrame

def get_hk_orginfo_em(symbol: str) -> pd.DataFrame:
    """
    获取港股公司概况数据，包括证券信息和组织概况，并合并为一个DataFrame。

    Args:
        symbol (str): 港股代码，例如 '01658.HK'。

    Returns:
        pd.DataFrame: 包含合并后公司概况数据的DataFrame。
                      如果请求失败或无数据，返回空的DataFrame。
    """
    # 移除可能存在的 .HK 后缀以构建 SECURITY_CODE
    secu_code = symbol.split('.')[0] if '.' in symbol else symbol

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
        'sec-ch-ua-platform': 'Windows',
    }

    # 获取证券信息 RPT_HKF10_INFO_SECURITYINFO
    url_sec_info = (
        f"https://datacenter.eastmoney.com/securities/api/data/v1/get"
        f"?reportName=RPT_HKF10_INFO_SECURITYINFO"
        f"&columns=SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,SECURITY_TYPE,"
        f"LISTING_DATE,ISIN_CODE,BOARD,TRADE_UNIT,TRADE_MARKET,"
        f"GANGGUTONGBIAODISHEN,GANGGUTONGBIAODIHU,PAR_VALUE,ISSUE_PRICE,"
        f"ISSUE_NUM,YEAR_SETTLE_DAY"
        f"&filter=(SECUCODE%3D%22{symbol}%22)"
        f"&pageNumber=1&pageSize=200&sortTypes=&sortColumns=&source=F10&client=PC"
    )

    try:
        response_sec_info = requests.get(url_sec_info, headers=headers)
        response_sec_info.raise_for_status()
        data_sec_info = response_sec_info.json()
    except requests.RequestException as e:
        print(f"请求证券信息失败: {e}")
        return pd.DataFrame() # 返回空DataFrame

    # 获取组织概况 RPT_HKF10_INFO_ORGPROFILE
    url_org_profile = (
        f"https://datacenter.eastmoney.com/securities/api/data/v1/get"
        f"?reportName=RPT_HKF10_INFO_ORGPROFILE"
        f"&columns=SECUCODE,SECURITY_CODE,ORG_NAME,ORG_EN_ABBR,BELONG_INDUSTRY,"
        f"FOUND_DATE,CHAIRMAN,SECRETARY,ACCOUNT_FIRM,REG_ADDRESS,ADDRESS,"
        f"YEAR_SETTLE_DAY,EMP_NUM,ORG_TEL,ORG_FAX,ORG_EMAIL,ORG_WEB,"
        f"ORG_PROFILE,REG_PLACE"
        f"&filter=(SECUCODE%3D%22{symbol}%22)"
        f"&pageNumber=1&pageSize=200&sortTypes=&sortColumns=&source=F10&client=PC"
    )

    try:
        response_org_profile = requests.get(url_org_profile, headers=headers)
        response_org_profile.raise_for_status()
        data_org_profile = response_org_profile.json()
    except requests.RequestException as e:
        print(f"请求组织概况失败: {e}")
        return pd.DataFrame() # 返回空DataFrame

    # 检查返回数据是否成功
    if not (data_sec_info.get('success') and data_org_profile.get('success')):
        print("API返回错误或无数据")
        return pd.DataFrame()

    # 提取数据列表
    sec_info_data_list = data_sec_info.get('result', {}).get('data', [])
    org_profile_data_list = data_org_profile.get('result', {}).get('data', [])

    # 确保都有数据且至少有一条记录
    if not sec_info_data_list or not org_profile_data_list:
        print("返回数据为空")
        return pd.DataFrame()

    # 取第一条记录进行合并 (通常应该只有一条)
    sec_info_dict = sec_info_data_list[0]
    org_profile_dict = org_profile_data_list[0]

    # 合并两个字典
    combined_dict = {**sec_info_dict, **org_profile_dict}

    # 转换为DataFrame
    df_result = pd.DataFrame([combined_dict]) # 使用列表包装字典以创建单行DataFrame

    return df_result


def get_listing_date(symbol: str) -> dateType:
    """
    获取指定股票的上市日期。

    Args:
        symbol (str): 股票代码，如 '600028.SH'。

    Returns:
        dateType: 股票上市日期，格式为 'YYYY-MM-DD'。
    """
    from mysharelib.tools import normalize_symbol

    _, symbol_f, market = normalize_symbol(symbol)
    if market == "HK":
        listing_date = pd.to_datetime(get_hk_orginfo_em(symbol_f)['LISTING_DATE'].values[0])
    else:
        listing_date = pd.to_datetime(get_a_orginfo_em(symbol_f)['LISTING_DATE'].values[0])

    if listing_date is not None:
        return listing_date
    else:
        return (datetime.now() - timedelta(days=365)).date()

# --- 示例用法 ---
if __name__ == "__main__":
    # 获取中国石化的公司概况
    stock_code = "600028.SH"
    df_orginfo = get_a_orginfo_em(stock_code)

    # 定义列名与中文名的映射关系
    column_mapping_a = {
        "SECUCODE": "证券代码",
        "SECURITY_CODE": "股票代码",
        "SECURITY_NAME_ABBR": "股票简称",
        "ORG_NAME": "公司名称",
        "ORG_NAME_EN": "公司英文名称",
        "FORMERNAME": "曾用名",
        "LEGAL_PERSON": "法定代表人",
        "PRESIDENT": "总经理",
        "CHAIRMAN": "董事长",
        "SECRETARY": "董事会秘书",
        "REG_CAPITAL": "注册资本(万元)",
        "ADDRESS": "办公地址",
        "REG_ADDRESS": "注册地址",
        "PROVINCE": "所在省份",
        "ORG_TEL": "联系电话",
        "ORG_EMAIL": "电子邮箱",
        "ORG_WEB": "公司网址",
        "ORG_PROFILE": "公司简介",
        "BUSINESS_SCOPE": "经营范围",
        "MAIN_BUSINESS": "主营业务",
        "TRADE_MARKET": "上市市场",
        "INDUSTRYCSRC1": "证监会行业分类",
        "EMP_NUM": "员工总数",
        "FOUND_DATE": "成立日期",
        "LISTING_DATE": "上市日期"
        # 可根据需要添加更多字段...
    }

    # 定义中英列名对照关系
    column_mapping_hk = {
        # RPT_HKF10_INFO_SECURITYINFO 部分
        'SECUCODE': '证券代码 (Security Code)',
        'SECURITY_CODE': '证券简称代码 (Security Short Code)',
        'SECURITY_NAME_ABBR': '证券简称 (Security Abbreviation)',
        'SECURITY_TYPE': '证券类型 (Security Type)',
        'LISTING_DATE': '上市日期 (Listing Date)',
        'ISIN_CODE': 'ISIN代码 (ISIN Code)',
        'BOARD': '上市板 (Listing Board)',
        'TRADE_UNIT': '每手股数 (Trading Unit)',
        'TRADE_MARKET': '交易市场 (Trading Market)',
        'GANGGUTONGBIAODISHEN': '沪港通标的 (Shanghai-HK Connect Stock)',
        'GANGGUTONGBIAODIHU': '深港通标的 (Shenzhen-HK Connect Stock)',
        'PAR_VALUE': '面值 (Par Value)',
        'ISSUE_PRICE': '发行价格 (Issue Price)',
        'ISSUE_NUM': '发行数量 (Issue Number)',
        'YEAR_SETTLE_DAY': '年度结算日 (Year-End Settlement Day)',

        # RPT_HKF10_INFO_ORGPROFILE 部分
        'ORG_NAME': '公司名称 (Organization Name)',
        'ORG_EN_ABBR': '公司英文简称 (Organization English Abbreviation)',
        'BELONG_INDUSTRY': '所属行业 (Industry)',
        'FOUND_DATE': '成立日期 (Founding Date)',
        'CHAIRMAN': '董事长 (Chairman)',
        'SECRETARY': '公司秘书 (Company Secretary)',
        'ACCOUNT_FIRM': '会计师事务所 (Accounting Firm)',
        'REG_ADDRESS': '注册地址 (Registered Address)',
        'ADDRESS': '办公地址 (Office Address)',
        'EMP_NUM': '员工人数 (Number of Employees)',
        'ORG_TEL': '公司电话 (Company Tel)',
        'ORG_FAX': '公司传真 (Company Fax)',
        'ORG_EMAIL': '公司邮箱 (Company Email)',
        'ORG_WEB': '公司网站 (Company Website)',
        'ORG_PROFILE': '公司简介 (Company Profile)',
        'REG_PLACE': '注册地 (Place of Registration)'
    }

    if not df_orginfo.empty:
        print(f"获取A股 {stock_code} 的公司概况数据:")
        print(df_orginfo.head()) # 打印前几行
        # 显示所有列名
        print("\n列名:")
        print(df_orginfo.columns.tolist())
        # 显示特定字段示例
        print(f"\n公司名称: {df_orginfo.iloc[0]['ORG_NAME']}")
        print(f"法定代表人: {df_orginfo.iloc[0]['LEGAL_PERSON']}")
        print(f"注册地址: {df_orginfo.iloc[0]['REG_ADDRESS']}")
        print(f"主营业务: {df_orginfo.iloc[0]['MAIN_BUSINESS']}")
    else:
        print(f"未能获取到 {stock_code} 的数据。")

    symbol_hk = "01658.HK"
    df = get_hk_orginfo_em(symbol_hk)

    if not df.empty:
        print(f"获取港股 {symbol_hk} 公司概况成功:")
        # 打印所有列名以检查
        # print(df.columns.tolist())
        # 打印前几列作为示例
        print(df[['SECUCODE', 'SECURITY_NAME_ABBR', 'SECURITY_TYPE', 'LISTING_DATE',
                  'ORG_NAME', 'BELONG_INDUSTRY', 'CHAIRMAN']])
        # print(df.head()) # 或者打印所有列的前几行
    else:
        print(f"获取 {symbol_hk} 公司概况失败或无数据。")
