"""Defines the pybraendstofpriser package."""

from __future__ import annotations
from asyncio import get_running_loop
from collections import namedtuple
from genericpath import isfile
import importlib
import logging
from os import listdir
from posixpath import dirname
import sys

if sys.version_info < (3, 11, 0):
    sys.exit("The pybraendstofpriser module requires Python 3.11.0 or later")

_LOGGER = logging.getLogger(__name__)
Company = namedtuple("Company", "module namespace products name")


class Braendstofpriser:
    """Main class for pybraendstofpriser module."""

    def __init__(self):
        """Initialize the Braendstofpriser class."""
        # self.companies = []
        self.companies = {}
        _LOGGER.debug("Braendstofpriser initialized")

    async def list_companies(self):
        """List fuel companies."""
        _LOGGER.debug("Listing companies")
        loop = get_running_loop()
        companies = await loop.run_in_executor(
            None, listdir, f"{dirname(__file__)}/companies"
        )
        for company in sorted(companies):
            company_path = f"{dirname(__file__)}/companies/{company}"
            if (
                isfile(company_path)
                and not company.endswith("__pycache__")
                and not company == "__init__.py"
            ):
                company_name = company.replace(".py", "")
                _LOGGER.debug("Found company: %s", company_name)

                ns = f".companies.{company.replace('.py', '')}"
                mod = await self._load_module(ns)

                # company_list_obj = Company(
                #     module=mod,
                #     namespace=ns,
                #     products=mod.PRODUCTS,
                #     name=mod.COMPANY_NAME,
                # )

                # self.companies.append(company_list_obj)

                self.companies.update(
                    {
                        mod.COMPANY_NAME: {
                            "products": mod.PRODUCTS,
                            "namespace": ns,
                        }
                    }
                )

        return self.companies

    async def get_price(self, company: str, product: str):
        """Get fuel price for a specific company and product."""
        _LOGGER.debug("Getting price for %s - %s", company, product)
        c = await self._load_module(self.companies[company]["namespace"])
        co = c.FuelCompany()
        return await co.fetch_price(product)

    @staticmethod
    async def _load_module(namespace: str):
        """Dynamically load a module."""
        loop = get_running_loop()
        return await loop.run_in_executor(
            None, importlib.import_module, namespace, __name__
        )
