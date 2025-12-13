import logging
import pandas as pd
import akshare as ak
from typing import Optional, Literal
from openbb_akshare import project_name
from mysharelib.tools import setup_logger, normalize_symbol

setup_logger(project_name)
logger = logging.getLogger(__name__)

def fetch_key_metrics(
        symbol: str, 
        period: Literal["annual", "quarter"] = "quarter",
        use_cache: bool = True,
        api_key : Optional[str] = ""
        ) -> pd.DataFrame:
    """
    Fetches key financial metrics for a specific equity symbol.

    Args:
        symbol (str): The stock symbol to fetch metrics for.
                      such as "601127.SH".

    Returns:
        pd.DataFrame: A DataFrame containing the key metrics.
    """
    from mysharelib.blob_cache import BlobCache

    if api_key is None or api_key == "":
        raise ValueError("API key must be provided.")

    symbol_b, _, market = normalize_symbol(symbol)
    if market not in ["SH", "SZ", "BJ", "HK"]:
        logger.warning("AKShare key metrics only support A shares.")
        return pd.DataFrame()
    cache = BlobCache(table_name="key_metrics", project=project_name)
    data = cache.load_cached_data(symbol_b, period, use_cache, _get_key_metrics, api_key=api_key)
    if data is None:
        return pd.DataFrame()
    else:
        return data
def _get_key_metrics(
    symbol: str,
    period: str = "quarter",
    api_key : Optional[str] = ""
) -> pd.DataFrame:
    import akshare as ak
    from mysharelib.em.get_a_info_em import get_a_info_em
    from mysharelib.em.get_hk_info_em import get_hk_info_em

    symbol_b, symbol_f, market = normalize_symbol(symbol)
    df_base = pd.DataFrame()
    if market == "HK":
        df_base, _ = get_hk_info_em(symbol_f)
    else:
        df_base, _ = get_a_info_em(symbol_f)

        ak.stock.cons.xq_a_token=api_key
        stock_individual_spot_xq_df = ak.stock_individual_spot_xq(symbol=f"{market}{symbol_b}")
        def get_metric(df, metric_name):
            return df.loc[df['item'] == metric_name, 'value'].iloc[0]

        df_base.loc['市盈率(动)'] = get_metric(stock_individual_spot_xq_df, '市盈率(动)')
        df_base.loc['市盈率(TTM)'] = get_metric(stock_individual_spot_xq_df, '市盈率(TTM)')
        df_base.loc['市盈率(静)'] = get_metric(stock_individual_spot_xq_df, '市盈率(静)')
        df_base.loc['市净率'] = get_metric(stock_individual_spot_xq_df, '市净率')
        df_base.loc['流通值'] = get_metric(stock_individual_spot_xq_df, '流通值')
        df_base.loc['52周最低'] = get_metric(stock_individual_spot_xq_df, '52周最低')
        df_base.loc['52周最高'] = get_metric(stock_individual_spot_xq_df, '52周最高')
        df_base.loc['股息(TTM)'] = get_metric(stock_individual_spot_xq_df, '股息(TTM)')
        df_base.loc['股息率(TTM)'] = get_metric(stock_individual_spot_xq_df, '股息率(TTM)')
        df_base.loc['发行日期'] = get_metric(stock_individual_spot_xq_df, '发行日期')
    return df_base
