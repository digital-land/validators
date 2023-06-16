import json
from esridump.dumper import EsriDumper


def arcgis_get(url, plugin="arcgis"):
    dumper = EsriDumper(url, fields=None)

    content = '{"type":"FeatureCollection","features":['
    sep = "\n"

    for feature in dumper:
        content += sep + json.dumps(feature)
        sep = ",\n"

    content += "]}"

    content = str.encode(content)
    return content
