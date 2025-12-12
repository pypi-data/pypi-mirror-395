from .exceptions import HttpException, SymbolNotFound, DataException
from .base import BaseAPI
import requests
from .base import HtmlTableParser
import re


class StockAnalysis(BaseAPI):
    def get_basic_info(self):
        """
        Downloads basic info about symbol. Data are:

        - company_name
        - market
        - description
        - has_dividends
        - year_low
        - year_hign
        - pe_ratio
        - eps
        - market_cap
        - similar_stocks (only for shares)
            - name
            - market_cap
        """

        def download(url):
            try:
                response = self._get(url)
                response.raise_for_status()
            except requests.HTTPError as e:
                if 404 == e.response.status_code:
                    raise SymbolNotFound
                raise HttpException from e

            return response

        def download_financials_and_others():
            def download_financials(response):
                """
                Contributes with:
                - market_cap
                - eps
                - has_dividends
                - pe_ratio
                """
                # Find all tables.
                finds = re.findall(
                    r"<table[^>]*>(.*?)</table>", response.text, re.DOTALL
                )

                if not finds:
                    raise DataException(
                        f"No basic data found for symbol {self.symbol}."
                    )

                # Parse 1st table.
                finds = re.findall(r"<tbody>(.*?)</tbody>", finds[0], re.DOTALL)
                rows = []

                try:
                    parser = HtmlTableParser(2)
                    parser.feed(finds[0])

                    rows = parser.get_data()
                except Exception as e:
                    raise DataException(
                        f"Invalid data in table for symbol {self.symbol}."
                    ) from e

                return {
                    "market_cap": rows[0][1],
                    "eps": rows[3][1],
                    "has_dividends": rows[2][1] != "n/a",
                    "pe_ratio": rows[7][1],
                }

            def download_company_name(response):
                """
                Contributes with:
                - company_name
                """
                try:
                    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", response.text, re.DOTALL)
                    company_name = re.sub(r"\(.*?\)", "", h1[0]).strip()
                except Exception as e:
                    raise DataException(
                        f"Invalid data for company name for symobl {self.symbol}."
                    ) from e

                return {"company_name": company_name}

            def download_description(response):
                """
                Contributes with:
                - description
                """
                # For share
                try:
                    description = re.findall(
                        f"About {self.symbol.upper()}</h2>[^<]?<p>(.*?)</p>",
                        response.text,
                        re.DOTALL,
                    )[0]
                except Exception:
                    # For ETF
                    try:
                        description = re.findall(
                            f"About {self.symbol.upper()}</h2>.*?</div>[^<]<p>(.*?)</p>",
                            response.text,
                            re.DOTALL,
                        )[0]
                    except Exception as e:
                        raise DataException(
                            f"Invalid data for description for symbol {self.symbol}."
                        ) from e

                return {"description": description}

            # Try stocks data.
            try:
                response = download(
                    f"https://stockanalysis.com/stocks/{self.symbol.lower()}/"
                )
            # Try ETF data.
            except SymbolNotFound:
                response = download(
                    f"https://stockanalysis.com/etf/{self.symbol.lower()}/"
                )

            # Compile output.
            data = download_financials(response)
            data |= download_company_name(response)
            data |= download_description(response)

            return data

        def download_basics():
            # Try stocks data.
            try:
                response = download(
                    f"https://stockanalysis.com/api/quotes/s/{self.symbol.lower()}"
                )
            # Try ETF data.
            except SymbolNotFound:
                response = download(
                    f"https://stockanalysis.com/api/quotes/e/{self.symbol.lower()}"
                )

            try:
                data = response.json()
                data = data["data"]
            except Exception:
                raise DataException(f"Invalid JSON data for symbol {self.symbol}.")

            return {
                "market": data["ex"],
                "year_low": data["l52"],
                "year_high": data["h52"],
            }

        def similar_items():
            try:
                response = self._get(
                    f"https://stockanalysis.com/stocks/{self.symbol.lower()}/market-cap/"
                )
            except Exception:
                return {"similar_items": []}

            # Find all tables.
            finds = re.findall(r"<table[^>]*>(.*?)</table>", response.text, re.DOTALL)

            if not finds:
                raise DataException(f"No market cap found for symbol {self.symbol}.")

            # Parse 2nd table.
            finds = re.findall(r"<tbody>(.*?)</tbody>", finds[1], re.DOTALL)
            rows = []

            try:
                parser = HtmlTableParser(2)
                parser.feed(finds[0])

                rows = parser.get_data()
            except Exception as e:
                raise DataException(
                    f"Invalid data in table for symbol {self.symbol}."
                ) from e

            # Compile output.
            return {
                "similar_items": [
                    {"company_name": name, "market_cap": market_cap}
                    for name, market_cap in rows
                ]
            }

        data = download_basics()
        data |= download_financials_and_others()
        data |= similar_items()

        return data
