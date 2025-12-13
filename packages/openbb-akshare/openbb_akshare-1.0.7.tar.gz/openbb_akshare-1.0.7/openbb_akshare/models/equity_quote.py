"""AKShare Equity Quote Model."""

# pylint: disable=unused-argument

from typing import Any, Dict, List, Optional
from warnings import warn

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.equity_quote import (
    EquityQuoteData,
    EquityQuoteQueryParams,
)
from pydantic import Field
import logging
from mysharelib.tools import setup_logger, normalize_symbol
from openbb_akshare import project_name

setup_logger(project_name)
logger = logging.getLogger(__name__)

class AKShareEquityQuoteQueryParams(EquityQuoteQueryParams):
    """AKShare Equity Quote Query."""

    __json_schema_extra__ = {"symbol": {"multiple_items_allowed": True}}

    use_cache: bool = Field(
        default=True,
        description="Whether to use a cached request. The quote is cached for one hour.",
    )


class AKShareEquityQuoteData(EquityQuoteData):
    """AKShare Equity Quote Data."""

    __alias_dict__ = {
        "symbol": "代码",
        "name": "名称",
        "last_price": "最新价",
        "open": "今开",
        "high": "最高",
        "low": "最低",
        "prev_close": "昨收",
        "volume": "成交量",
        "change": "涨跌额",
        "change_percent": "涨跌幅",
    }


class AKShareEquityQuoteFetcher(
    Fetcher[AKShareEquityQuoteQueryParams, List[AKShareEquityQuoteData]]
):
    """AKShare Equity Quote Fetcher."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> AKShareEquityQuoteQueryParams:
        """Transform the query."""
        return AKShareEquityQuoteQueryParams(**params)

    @staticmethod
    def extract_data(
        query: AKShareEquityQuoteQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Extract the raw data from AKShare."""
        # pylint: disable=import-outside-toplevel
        import akshare as ak
        import pandas as pd

        symbols = query.symbol.split(",")
        all_data = []

        def get_one(symbol, use_cache) -> pd.DataFrame:
            """Get the data for one ticker symbol."""
            from openbb_akshare.utils.fetch_quote import load_cached_data
            quote = pd.DataFrame()
            symbol_b, symbol_f, market = normalize_symbol(symbol)
            stock_quotes = load_cached_data(market, use_cache)
            quote = stock_quotes[stock_quotes["代码"] == symbol]

            if quote.empty:
                return pd.DataFrame([{"symbol": symbol, "error": "Symbol not found"}])
            return quote

        for symbol in symbols:
            try:        
                data = get_one(symbol, query.use_cache)
                all_data.append(data.to_dict(orient="records")[0])
                
            except Exception as e:
                print(f"Error fetching data for symbol {symbol}: {e}")
                continue

        return all_data

    @staticmethod
    def transform_data(
        query: AKShareEquityQuoteQueryParams,
        data: List[Dict],
        **kwargs: Any,
    ) -> List[AKShareEquityQuoteData]:
        """Transform the data."""
        return [AKShareEquityQuoteData.model_validate(d) for d in data]
