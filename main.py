import os
import logging
from typing import Literal, Any
from dotenv import load_dotenv

import requests
import json

# import matplotlib.pyplot as plt
# import pandas as pd


class APIData:
    def __init__(self) -> None:
        self.data = {}
    def __repr__(self):
        return f"APIData(data={self.data})"
    def __str__(self):
        return json.dumps(self.data, indent=4)
    def authenticate(self, client_id: str, client_secret: str) -> dict | None:
        try:
            response = requests.post(
                url="https://id.twitch.tv/oauth2/token",
                params={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "grant_type": "client_credentials"
                }
            )
            auth_data = response.json()
            return auth_data
        except Exception as e:
            logging.error(f"An error occurd when trying to authenticate: {e}")
            return None
    def api_fetch(self, url: str, client_id: str, access_token: str, data_fields: list[str] | None = None, data_limit: int | None = None) -> None:
        try:
            data_query = "fields " + ",".join(data_fields) + ";" if data_fields else "fields name;"
            data_query += f" limit {data_limit};" if data_limit else " limit 10;"
            response = requests.post(url=url, **{"headers": {"Client-ID": client_id, "Authorization": f"Bearer {access_token}"}, "data": data_query})
            self.data = response.json()
        except Exception as e:
            logging.error(f"An error occurd when trying to fetch data: {e}")

class Graph:
    def __init__(
            self, 
            type: Literal["dot", "bar", "box", "hist"]) -> None:
        self.type = type

class DotGraph(Graph):
    def __init__(
            self, 
            x: list[int | float], 
            y: list[int | float]):
        """
        Creates an instanse of DotGraph.

        Parameters:
            x(list[int | float]): List containing the x value for each dot.
            y(list[int | float]): List containing the y value for each dot.

        Raises:
            ValueError: If the length of x and y are not equal.
        """
        super().__init__("dot")
        self.x = x
        self.y = y

class BarGraph(Graph):
    def __init__(self, vals: dict[Any, int]) -> None:
        super().__init__("bar")
        self.vals = vals

class BoxGraph(Graph):
    def __init__(self, vals: list[int | float]) -> None:
        super().__init__("box")
        self.vals = vals

class HistGraph(Graph):
    def __init__(self, vals: list[int | float], width: int | float = 10):
        super().__init__("hist")
        self.vals = vals
        self.width = width


def main() -> int:
    logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s")

    logger = logging.getLogger(__name__)
    logger.info("Hello from %s", __name__)

    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    my_data = APIData()
    auth = my_data.authenticate(client_id, client_secret)
    if auth:
        logger.info("Authentication successful")
        my_data.api_fetch("https://api.igdb.com/v4/games", client_id, auth["access_token"], ["name", "rating", "release_dates"], 5)
        if my_data.data:
            logger.info("Data fetch successful")
    print(my_data)

    return 0

if __name__ == "__main__":
    exit_code = main()
    if exit_code == 0:
        logging.info("Exited program with exit_code: 0")
    else:
        logging.info(f"Exited program with exit_code: {exit_code}")