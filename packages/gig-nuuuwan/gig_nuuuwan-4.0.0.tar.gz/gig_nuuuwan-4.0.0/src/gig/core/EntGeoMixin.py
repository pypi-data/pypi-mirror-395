import json
import os
import tempfile
import time
from functools import cached_property

import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon
from utils import WWW, JSONFile, Log, Parallel

from gig.core.EntType import EntType
from gig.core.GIGConstants import GIGConstants

log = Log("EntGeoMixin")


class EntGeoMixin:
    @property
    def raw_geo_file(self):
        raw_geo_path = os.path.join(
            tempfile.gettempdir(), f"ent.{self.id}.raw_geo.json"
        )
        return JSONFile(raw_geo_path)

    @property
    def url_remote_geo_data_path(self):
        ent_id = self.id
        ent_type = EntType.from_id(ent_id)

        if ent_id.startswith("LK-"):
            return (
                f"{GIGConstants.URL_BASE_NEW}"
                + "/data/geo/json/original"
                + f"/{ent_type.name}s.json/{ent_id}.json"
            )

        return f"{GIGConstants.URL_BASE}/geo/{ent_type.name}/{ent_id}.json"

    def get_raw_geo(self):
        raw_geo_file = self.raw_geo_file
        if raw_geo_file.exists:
            raw_geo = raw_geo_file.read()
        else:
            log.debug(f"Downloading geo data for {self.id}")
            content = WWW(self.url_remote_geo_data_path).read()
            raw_geo = json.loads(content)
            raw_geo_file.write(raw_geo)
        return raw_geo

    def geo(self):
        polygon_list = list(
            map(
                Polygon,
                self.get_raw_geo(),
            )
        )
        multipolygon = MultiPolygon(polygon_list)
        return gpd.GeoDataFrame(
            index=[0], crs="epsg:4326", geometry=[multipolygon]
        )

    def geo_safe(self, timeout=10):
        timeout_cur = 0.1
        while timeout_cur < timeout:
            try:
                return self.geo()
            except Exception as e:
                log.error(f"[{timeout_cur}s] {self.id} {e}")
                time.sleep(timeout_cur)
                timeout_cur *= 2
        return None

    def get_area_from_geo(self) -> float:
        geo = self.geo_safe()
        geo = geo.to_crs(epsg=3395)
        return geo.area.sum() / 1_000_000.0

    @cached_property
    def area(self):
        return self.get_area_from_geo()

    @classmethod
    def get_ent_id_to_geo(cls, ent_id_list, max_threads=4):
        workers = []

        for ent_id in ent_id_list:

            def worker(ent_id=ent_id):
                ent = cls.from_id(ent_id)
                return ent_id, ent.geo()

            workers.append(worker)

        tuples = Parallel.run(workers, max_threads=max_threads)
        return dict(tuples)
