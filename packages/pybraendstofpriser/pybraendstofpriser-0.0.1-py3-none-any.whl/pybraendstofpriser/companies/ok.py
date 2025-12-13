"""OK fetcher for pybraendstofpriser."""

from __future__ import annotations
import logging

from ..exceptions import ErrorFetchingProduct
from ..const import DIESEL, OCTANE_100, OCTANE_95
from ..tools import clean_product_name, clean_value, get_html_soup, get_website

baseurl = (
    "https://www.ok.dk/offentlig/produkter/braendstof/priser/vejledende-standerpriser"
)

PRODUCTS = {
    DIESEL: {"name": "Diesel"},
    OCTANE_95: {"name": "Blyfri 95"},
    OCTANE_100: {"name": "Oktan 100"},
}

COMPANY_NAME = "OK"

_LOGGER = logging.getLogger(__name__)


class FuelCompany:
    """OK fuel company class."""

    def __init__(self):
        """Initialize the OKCompany class."""
        pass

    async def fetch_price(self, product: str) -> float | None:
        """Fetch fuel prices from OK."""
        return await self._parser(product)

    async def list_products(self) -> list[str]:
        """List available fuel products from OK."""
        retlist = []
        for _, productDict in PRODUCTS.items():
            retlist.append(productDict["name"])
        return retlist

    async def _parser(self, product) -> float | None:
        """Parse the fetched data."""
        r = await get_website(baseurl, timeout=5)
        html = get_html_soup(r)
        rows = html.find_all("div", {"role": "row"})

        for row in rows:
            cells = row.find_all("div", {"role": "gridcell"})
            if cells:
                found = PRODUCTS[product]["name"] == clean_product_name(cells[0].text)
                if found:
                    return clean_value(cells[1].text)

        raise ErrorFetchingProduct(f"Product '{PRODUCTS[product]['name']}' not found")
