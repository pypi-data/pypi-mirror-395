"""
The `rcloud` module builds on the `thread` module by adding URL-based data acquisition capabilities.

Classes:
    RCloud: An extension of the RThread class for handling URL-based data acquisition.
    RCloudThread: An extension of the RThread class to support URL data fetching.

It is up to the subclasses of RCloudThread  to implement the specific URL for data acquisition, such 
as weather forecasts, and the `process_data()` method to handle the acquired data. 
The `process_data()` method might, for instance, publish the data to an appropriate automation MQTT topic.

This module simplifies the process of integrating and processing data from web-based resources, 
such as weather forecast websites, leveraging the asynchronous processing capabilities provided by the `thread` module.
"""

from typing import Any, Optional
import requests
from masterpiece.mqtt import Mqtt
from .juham_thread import JuhamThread, MasterPieceThread


class JuhamCloudThread(MasterPieceThread):
    """Data acuisition base class. Responsible for fetching data from clouds and other web
    resources via url. It is up to the sub classes to implement get_url() and process_data()
    methods.

    Can be configured how often the query is being run.
    """

    timeout: float = 60

    def __init__(self, client: Optional[Mqtt]) -> None:
        """Construct automation object with the given MQTT client.

        Args:
            client (Mqtt, optional): Mqtt. Defaults to None.
        """
        super().__init__(client)

    def make_weburl(self) -> str:
        """Build http url for acquiring data from the web resource. Up to the
        sub classes to implement.

        This method is periodically called by update method.

        Returns: Url to be used as parameter to requests.get().
        """
        return ""

    def update(self) -> bool:
        """Acquire and process.

        This method is periodically called to acquire data from a the configured web url
        and publish it to respective MQTT topic in the process_data() method.

        Returns: True if the update succeeded. Returning False implies an error and
        in which case the method should be called shortly again to retry. It is up
        to the caller to decide the number of failed attempts before giving up.
        """

        headers: dict[Any, Any] = {}
        params: dict[Any, Any] = {}
        url = self.make_weburl()

        try:

            response = requests.get(
                url, headers=headers, params=params, timeout=self.timeout
            )

            if response.status_code == 200:
                self.process_data(response)
                return True
            else:
                self.error(f"Reading {url}  failed: {str(response)}")
        except Exception as e:
            self.error(f"Requesting data from {url} failed", str(e))
        return False

    def process_data(self, data: Any) -> None:
        """Process the acquired data.

        This method is called from the update method, to process the
        data from the acquired data source. It is up to the sub classes
        to implement this.
        """
