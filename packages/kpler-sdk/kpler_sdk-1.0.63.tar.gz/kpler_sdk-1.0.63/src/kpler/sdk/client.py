from importlib.metadata import version
import json
import logging
from typing import Any, Dict, List, Optional

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import Timeout

from kpler.sdk.configuration import Configuration
from kpler.sdk.exceptions import (
    AuthenticationClassError,
    AuthenticationError,
    HttpError,
    RequestTimeoutError,
    RestrictedPlatformException,
)
from kpler.sdk.helpers import bytes_to_pandas_data_frame, filter_nones_from_dict


VERSION = version("kpler_sdk")


class KplerClient:
    """
    Base class for resources.

    Attributes:
        platform(Platform): An enum of type Platform to indicate the Platform to connect to
        email(str): The email to be used for login
        password(str): The password associated to the email

    """

    def __init__(
        self,
        configuration: Configuration,
        available_platforms: List,
        column_ids: bool = True,
        log_level=None,
    ):
        """
        Initiate the connection to Kpler servers.

        We do the login once and we keep the token.
        But we need to make sure we renew it before it expires.

        Args:
            configuration (Configuration): Configuration instance object which contains all the details (platform, login, password)
        """

        if configuration.platform not in available_platforms:
            raise RestrictedPlatformException(available_platforms)

        self.available_platforms = available_platforms

        logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s")
        self.configuration = configuration
        self.column_ids = column_ids
        self.logger = self.configuration.logger

        self._get_mapping()

    def _get_mapping(self):
        """
        Get the type mapping for this endpoint. It will be used to map type in Pandas.
        """
        if not self.configuration.auth_validated:
            self.mapping = {}
            return

        try:
            cols = self.get_columns()
            self.mapping = cols.set_index("id")["type"].to_dict()
            self.mapping.update(cols.set_index("name")["type"].to_dict())
        except Exception:
            # the endpoint does not have it, or anything else
            self.mapping = {}

    def _get_raw(self, resource: str, params: Dict[str, Optional[Any]] = {}):
        """
        Internal use only!

        This is the centralized method to query the server.
        """
        if not self.configuration.auth_validated:
            raise AuthenticationClassError()

        url = f"{self.configuration.base_url}/{resource}"
        params = params or {}
        params = filter_nones_from_dict(params)
        url_pretty = url + "?" + "&".join([f"{k}={v}" for k, v in params.items()])
        self.logger.debug(f"Requesting {url_pretty}")

        headers = {"X-SDK-Version": f"python-{VERSION}"}
        if self.column_ids:
            headers["X-use-columns-ids-headers"] = ""

        response = requests.get(
            url,
            params=params,  # type: ignore
            auth=HTTPBasicAuth(self.configuration.email, self.configuration.password),
            stream=True,
            headers=headers,
            proxies=self.configuration.proxies,
            cert=self.configuration.certificates,
            verify=self.configuration.verify,
            timeout=(None, self.configuration.timeout),
        )
        if response.status_code == 200:
            return response
        elif response.status_code in (401, 403):
            raise AuthenticationError(response.content)
        else:
            raise HttpError(response.status_code, response.content)

    def _get_dataframe(
        self, resource: str, params: Dict[str, Optional[Any]], header_parameters=None
    ) -> pd.DataFrame:

        if header_parameters is None:
            header_parameters = []
        if self.configuration.platform not in self.available_platforms:
            raise RestrictedPlatformException(self.available_platforms)

        self.validate()
        try:
            response = self._get_raw(resource, params)
            content: bytes = response.content
        except Timeout:
            raise RequestTimeoutError(
                f"Request duration exceeded configured timeout duration of {self.configuration.timeout} seconds. Increase or remove the timeout or change your filters."
            )

        try:
            if len(header_parameters) == 0:
                return bytes_to_pandas_data_frame(content, self.mapping)
            else:
                df = bytes_to_pandas_data_frame(content, self.mapping)
                df._metadata = ["headers"]
                df.headers = {
                    header_param: response.headers[header_param]
                    for header_param in header_parameters
                }

                return df
        except AuthenticationClassError:
            self.logger.error("You are not authenticated. Please execute 'Configuration' first.")
        except AuthenticationError as e:
            self.logger.error(f"Authentication error on request: returned [{e}]")
        except Exception as e:
            self.logger.error(f"Error on request: returned [{e}]")

    def _get_columns_for_resource(
        self, resource: str, columns_path: str = "columns"
    ) -> pd.DataFrame:
        try:
            content: bytes = self._get_raw(f"{resource}/{columns_path}").content
            data: dict = json.loads(content)
            df = pd.DataFrame(data["selected"] + data["unselected"])
            if "shortId" in df.columns:
                df.drop("shortId", axis=1, inplace=True)
            if "columnName" in df.columns:
                df.rename(columns={"columnName": "name"}, inplace=True)
            df.columns = df.columns.str.strip()
            return df
        except AuthenticationClassError:
            self.logger.error("You are not authenticated. Please execute 'Configuration' first.")
        except AuthenticationError as e:
            self.logger.error(f"Authentication error on request: returned [{e}]")
        except Exception as e:
            self.logger.error(f"Error on request: returned [{e}]")
        return pd.DataFrame()

    def _search(self, query_parameters: Dict[str, str]) -> pd.DataFrame:
        if not self.configuration.auth_validated:
            self.logger.error("You are not authenticated. Please execute 'Configuration' first.")
            return pd.DataFrame()

        try:
            result = requests.get(
                f"{self.configuration.base_url}/search",
                params=query_parameters,  # type: ignore
                auth=HTTPBasicAuth(self.configuration.email, self.configuration.password),
                stream=True,
                headers={"X-SDK-Version": f"python-{VERSION}"},
                proxies=self.configuration.proxies,
                cert=self.configuration.certificates,
                verify=self.configuration.verify,
            )
            return pd.DataFrame.from_dict(result.json())
        except Exception as e:
            self.logger.error(f"Error on search request: returned [{e}]")
        return pd.DataFrame()

    def get_columns(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

    def search(self, q: str) -> Any:
        raise AttributeError(f"search function is not defined for {self.__class__.__name__}")

    def validate(self):
        return True
