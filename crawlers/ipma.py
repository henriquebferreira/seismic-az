import requests
import json
import pandas as pd

from crawlers.base import SeismicCrawler


class IpmaCrawler(SeismicCrawler):
    IPMA_BASE_URL = "http://api.ipma.pt/open-data"
    IPMA_SEISMIC_ENDPOINT = "/observation/seismic/$AREA_ID$.json"

    AREA_ID_MAPPER = {"mainland": 7,
                      "madeira": 7,
                      "azores": 3}

    def __init__(self, area_name):
        self.set_area_name(area_name)
        super().__init__("IPMA")

    def set_area_name(self, area_name):
        if not isinstance(area_name, str):
            raise TypeError("'area_name' must be a string")

        valid_values = list(self.AREA_ID_MAPPER.keys())
        if area_name not in valid_values:
            raise ValueError(f"'area_name' should be one of: {valid_values}")

        self.area_name = area_name

    def crawl(self):
        area_id = self.AREA_ID_MAPPER.get(self.area_name)
        url = f'{self.IPMA_BASE_URL}{self.IPMA_SEISMIC_ENDPOINT}'
        url = url.replace("$AREA_ID$", str(area_id))

        data = {}
        try:
            response = requests.get(url)
            response.raise_for_status()

            data = json.loads(response.text)
        except Exception as err:
            print(err)
        finally:
            self.data = data
            return data

    def pandify_data(self):
        df = pd.DataFrame(self.data["data"])
        df["source"] = "IPMA"

        df["date"] = pd.to_datetime(df["time"])
        df["lat"] = df["lat"].astype(float)
        df["lon"] = df["lon"].astype(float)
        df["magnitude"] = df["magnitud"].astype(float)
        df["magnitude_type"] = df["magType"].astype("string[pyarrow]")
        df["depth"] = df["depth"].astype(int)
        df["degree"] = df["degree"].astype("string[pyarrow]")
        df["local"] = df["local"].astype("string[pyarrow]")
        df["obs_region"] = df["obsRegion"].astype("string[pyarrow]")
        df["updated_at"] = pd.to_datetime(df["dataUpdate"])

        drop_columns = ["time",
                        "sismoId",
                        "dataUpdate",
                        "magType",
                        "obsRegion",
                        "sensed",
                        "googlemapref",
                        "tensorRef",
                        "shakemapid",
                        "shakemapref",
                        "magnitud"]
        df = df.drop(columns=drop_columns)

        df = df.replace('', None)
        df = df.sort_values(by="date", ascending=False)

        # Column selection and reordering
        df = df[["date", "lat", "lon", "magnitude", "magnitude_type",
                 "depth", "degree", "local", "obs_region", "source",
                 "updated_at"]]
        return df
