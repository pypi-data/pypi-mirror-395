import logging
from typing import Optional, Dict, Any, Literal
from datetime import datetime, timedelta
import requests
import pandas as pd
from requests.exceptions import RequestException
from mysharelib.tools import get_quarters, get_annual

# Configure logging
logger = logging.getLogger(__name__)

# Constants
BASE_URL = 'https://datacenter.eastmoney.com/securities/api/data/v1/get'
API_COLUMNS = ('SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,ORG_CODE,REPORT_DATE,'
              'DATE_TYPE_CODE,FISCAL_YEAR,STD_ITEM_CODE,STD_ITEM_NAME,AMOUNT,STD_REPORT_DATE')

DEFAULT_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6',
    'Connection': 'keep-alive',
    'Origin': 'https://emweb.securities.eastmoney.com',
    'Referer': 'https://emweb.securities.eastmoney.com/',
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0'),
}

def _build_request_params(symbol: str, 
                          limit: int,
                          period: Literal["annual", "quarter"] = "quarter"
                          ) -> Dict[str, str]:
    """Build request parameters for the API call.
    
    Args:
        symbol (str): Stock symbol like "01088.HK"
        
    Returns:
        Dict[str, str]: API request parameters
    """
    if period == "annual":
        quarters = get_annual(limit)
    else:
        quarters = get_quarters(limit)
    return {
        'reportName': 'RPT_HKF10_FN_BALANCE_PC',
        'columns': API_COLUMNS,
        'filter': f'(SECUCODE="{symbol}")(REPORT_DATE in ({quarters}))',
        'pageNumber': '1',
        'pageSize': '',
        'sortTypes': '-1,1',
        'sortColumns': 'REPORT_DATE,STD_ITEM_CODE',
        'source': 'F10',
        'client': 'PC',
        'v': '025466691284924325'
    }

def _process_response_data(data: Dict[str, Any]) -> pd.DataFrame:
    """Process API response data into a DataFrame.
    
    Args:
        data (Dict[str, Any]): Raw API response data
        
    Returns:
        pd.DataFrame: Processed balance sheet data
    """
    if not (data.get('result') and data['result'].get('data')):
        logger.warning("No valid data received from the API")
        return pd.DataFrame()
    
    df = pd.DataFrame(data['result']['data'])
    
    # Convert date columns
    for date_col in ['REPORT_DATE', 'STD_REPORT_DATE']:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col]).dt.date
            
    return df

def stock_balance_sheet(symbol: str, 
                        limit: int = 10,
                        period: Literal["annual", "quarter"] = "quarter"
                        ) -> pd.DataFrame:
    """
    Fetch balance sheet data for Hong Kong stocks using EastMoney API.
    
    Args:
        symbol (str): Hong Kong stock symbol (e.g., "01088.HK")
    
    Returns:
        pd.DataFrame: Balance sheet data with columns:
            - SECUCODE: Stock code
            - SECURITY_CODE: Security code
            - SECURITY_NAME_ABBR: Company name abbreviation
            - ORG_CODE: Organization code
            - REPORT_DATE: Report date
            - DATE_TYPE_CODE: Date type code
            - FISCAL_YEAR: Fiscal year
            - STD_ITEM_CODE: Standard item code
            - STD_ITEM_NAME: Item name
            - AMOUNT: Amount value
            - STD_REPORT_DATE: Standard report date
            
    Raises:
        RequestException: If there's an error with the API request
    """
    try:
        response = requests.get(
            BASE_URL,
            params=_build_request_params(symbol, limit, period),
            headers=DEFAULT_HEADERS,
            timeout=10
        )
        response.raise_for_status()
        return _process_response_data(response.json())
        
    except RequestException as e:
        logger.error(f"Failed to fetch balance sheet data: {str(e)}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Unexpected error while fetching balance sheet data: {str(e)}")
        return pd.DataFrame()