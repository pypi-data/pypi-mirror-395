import os
from dataclasses import dataclass
from functools import cached_property

from utils import WWW, File, Log, TSVFile

from gig.core.GIGConstants import GIGConstants
from gig.core.GIGTableRow import GIGTableRow

ID_FIELD = "entity_id"


log = Log("GIGTable")


@dataclass
class GIGTable:
    measurement: str
    ent_type_group: str
    time_group: str

    @property
    def table_id(self):
        return ".".join(
            [
                self.measurement,
                self.ent_type_group,
                self.time_group,
            ]
        )

    @property
    def url_remote_data_path(self):
        return f"{GIGConstants.URL_BASE}/gig2/{self.table_id}.tsv"

    @property
    def temp_data_path(self):
        temp_gig_dir_tables = os.path.join(
            GIGConstants.TEMP_GIG_DIR, "tables"
        )
        os.makedirs(temp_gig_dir_tables, exist_ok=True)
        return os.path.join(temp_gig_dir_tables, f"{self.table_id}.tsv")

    @cached_property
    def remote_data_list(self) -> list:
        if not os.path.exists(self.temp_data_path):
            content = WWW(self.url_remote_data_path).read()
            File(self.temp_data_path).write(content)
            log.debug(
                f"Downloaded {self.url_remote_data_path}"
                + f" to {self.temp_data_path}"
            )
        d_list = TSVFile(self.temp_data_path).read()
        n = len(d_list)
        log.debug(f"Loaded {n} records from {self.temp_data_path}")
        return d_list

    @cached_property
    def remote_data_idx(self) -> dict:
        return {d[ID_FIELD]: d for d in self.remote_data_list}

    def get(self, id):
        return GIGTableRow(self.remote_data_idx[id])
