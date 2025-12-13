from cubexpress.conversion import lonlat2rt, geo2utm
from cubexpress.geotyping import RasterTransform, Request, RequestSet
from cubexpress.cloud_utils import s2_table
from cubexpress.cube import get_cube
from cubexpress.request import table_to_requestset
import importlib.metadata


__all__ = [
    "lonlat2rt",
    "RasterTransform",
    "Request",
    "RequestSet",
    "geo2utm",
    "get_cube",
    "s2_table",
    "table_to_requestset"
]

from cubexpress.conversion import lonlat2rt, geo2utm
from cubexpress.geotyping import RasterTransform, Request, RequestSet
from cubexpress.cloud_utils import s2_table
from cubexpress.cube import get_cube
from cubexpress.request import table_to_requestset

__all__ = [
    "lonlat2rt",
    "RasterTransform",
    "Request",
    "RequestSet",
    "geo2utm",
    "get_cube",
    "s2_table",
    "table_to_requestset"
]


try:
    from importlib.metadata import version
    __version__ = version("cubexpress")
except Exception:
    __version__ = "0.1.X-dev"