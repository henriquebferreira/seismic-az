import pandas as pd
import requests
import xmltodict

from crawlers.base import SeismicCrawler


class IvarCrawler(SeismicCrawler):
    IVAR_BASE_URL = "http://www.ivar.azores.gov.pt"
    IVAR_SEISMIC_ENDPOINT = "/seismic/eventgroup.xml"

    def __init__(self):
        super().__init__("IVAR")

    def crawl(self):
        url = f'{self.IVAR_BASE_URL}{self.IVAR_SEISMIC_ENDPOINT}'

        data = {}
        try:
            response = requests.get(url)
            response.raise_for_status()

            data = xmltodict.parse(response.text)

        except Exception as err:
            print(err)
        finally:
            self.data = data
            return data

    def format_data(self):
        processed_data = []

        for e in self.data["EventGroup"]["Event"]:
            event_id = e["@EventID"].strip()
            origin = e["Origin"]
            if isinstance(origin, list):
                origin = origin[0]
            origin_agency = origin["@Agency"]
            origin_id = origin["@OriginID"]
            origin_time = origin["originTime"]
            location_length = origin["location"]["@length"]
            location = origin["location"]["#text"]
            magnitude_agency = e["Magnitude"]["@Agency"]
            magnitude_id = e["Magnitude"]["@MagnitudeID"]
            magnitude_value = e["Magnitude"]["value"]
            magnitude_type = e["Magnitude"]["type"]
            prime_origin_resource_id = e["primeOrigin"]["@ResourceID"]
            prime_magnitude_resource_id = e["primeMagnitude"]["@ResourceID"]
            comment_commands = []
            for command in e["CommentCommand"]:
                comment_commands.append({
                    "parameter": command["@Parameter"],
                    "value": command["value"]})

            processed_data.append(dict(
                event_id=event_id,
                origin_agency=origin_agency,
                origin_id=origin_id,
                time=origin_time,
                location_length=location_length,
                location=location,
                magnitude_agency=magnitude_agency,
                magnitude_id=magnitude_id,
                magnitude=magnitude_value,
                magnitude_type=magnitude_type,
                prime_origin_resource_id=prime_origin_resource_id,
                prime_magnitude_resource_id=prime_magnitude_resource_id,
                comment_commands=comment_commands
            ))
        return processed_data

    def _extract_lat_and_lon(self, data):
        locations = data["location"]

        lats, lons = [], []
        for l in locations:
            lat, lon, _ = l.split(", ")
            lats.append(float(lat))
            lons.append(float(lon))

        data["lat"] = lats
        data["lon"] = lons

        return data

    def _unpack_comment_commands(self, data):
        sentidos = [[] for i in range(len(data))]
        regioes = [[] for i in range(len(data))]

        for idx, row_commands in enumerate(data["comment_commands"]):
            for command in row_commands:
                if command["parameter"] == "SENTIDO:":
                    sentidos[idx].append(command["value"])
                elif command["parameter"] == "REGIAO:":
                    regioes[idx].append(command["value"])

        data["sentidos"] = sentidos
        data["regioes"] = regioes
        return data

    def pandify_data(self):
        formatted_data = self.format_data()
        df = pd.DataFrame(formatted_data)

        df["date"] = pd.to_datetime(df["time"]).dt.tz_localize(None)
        df = self._extract_lat_and_lon(df)
        df["magnitude"] = df["magnitude"].astype(float)
        df = self._unpack_comment_commands(df)

        drop_columns = ["origin_id",
                        "time",
                        "location_length",
                        "location",
                        "magnitude_agency",
                        "magnitude_id",
                        "magnitude_type",
                        "prime_origin_resource_id",
                        "prime_magnitude_resource_id",
                        "comment_commands"]

        df = df.drop(columns=drop_columns)
        df = df.sort_values(by="date", ascending=False)
        return df
