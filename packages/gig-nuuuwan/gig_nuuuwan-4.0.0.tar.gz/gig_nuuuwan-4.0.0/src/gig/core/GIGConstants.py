import os
import tempfile


class GIGConstants:
    URL_BASE = "/".join(
        [
            "https://raw.githubusercontent.com",
            "nuuuwan/gig-data/master",
        ]
    )
    URL_BASE_NEW = "/".join(
        [
            "https://raw.githubusercontent.com",
            "nuuuwan/lk_admin_regions/master",
        ]
    )

    TEMP_GIG_DIR = os.path.join(tempfile.gettempdir(), "gig")
