import urllib.parse
import math

class PolylineToImg:

    _bboxZoomLevels = [
        { "level": 0, "maxLong": 360.0, "maxLat": 170.0 },
        { "level": 1, "maxLong": 360.0, "maxLat": 170.0 },
        { "level": 2, "maxLong": 360.0, "maxLat": 170.0 },
        { "level": 3, "maxLong": 360.0, "maxLat": 170.0 },
        { "level": 4, "maxLong": 360.0, "maxLat": 170.0 },
        { "level": 5, "maxLong": 180.0, "maxLat": 85.0 },
        { "level": 6, "maxLong": 90.0, "maxLat": 42.5 },
        { "level": 7, "maxLong": 45.0, "maxLat": 21.25 },
        { "level": 8, "maxLong": 22.5, "maxLat": 10.625 },
        { "level": 9, "maxLong": 11.25, "maxLat": 5.3125 },
        { "level": 10, "maxLong": 5.625, "maxLat": 2.2625 },
        { "level": 11, "maxLong": 2.8125, "maxLat": 1.328125 },
        { "level": 12, "maxLong": 1.40625, "maxLat": 0.6640625 },
        { "level": 13, "maxLong": 0.703125, "maxLat": 0.33203125 },
        { "level": 14, "maxLong": 0.3515625, "maxLat": 0.166015625 },
        { "level": 15, "maxLong": 0.17578125, "maxLat": 0.0830078125 },
        { "level": 16, "maxLong": 0.087890625, "maxLat": 0.0415039063 },
        { "level": 17, "maxLong": 0.0439453125, "maxLat": 0.0207519531 },
        { "level": 18, "maxLong": 0.0219726563, "maxLat": 0.0103759766 },
        { "level": 19, "maxLong": 0.0109863281, "maxLat": 0.0051879883 },
        { "level": 20, "maxLong": 0.0054931641, "maxLat": 0.0025939941 }
    ]

    _tileZoomLevels = [
        { "level": 0, "metersPerPixel": 156543, "metersPerTileSide": 40075017 },
        { "level": 1, "metersPerPixel": 78271.5, "metersPerTileSide": 20037508 },
        { "level": 2, "metersPerPixel": 39135.8, "metersPerTileSide": 10018754 },
        { "level": 3, "metersPerPixel": 19567.88, "metersPerTileSide": 5009377.1 },
        { "level": 4, "metersPerPixel": 9783.94, "metersPerTileSide": 2504688.5 },
        { "level": 5, "metersPerPixel": 4891.97, "metersPerTileSide": 1252344.3 },
        { "level": 6, "metersPerPixel": 2445.98, "metersPerTileSide": 626172.1 },
        { "level": 7, "metersPerPixel": 1222.99, "metersPerTileSide": 313086.1 },
        { "level": 8, "metersPerPixel": 611.5, "metersPerTileSide": 156543 },
        { "level": 9, "metersPerPixel": 305.75, "metersPerTileSide": 78271.5 },
        { "level": 10, "metersPerPixel": 152.87, "metersPerTileSide": 39135.8 },
        { "level": 11, "metersPerPixel": 76.44, "metersPerTileSide": 19567.9 },
        { "level": 12, "metersPerPixel": 38.219, "metersPerTileSide": 9783.94 },
        { "level": 13, "metersPerPixel": 19.109, "metersPerTileSide": 4891.97 },
        { "level": 14, "metersPerPixel": 9.555, "metersPerTileSide": 2445.98 },
        { "level": 15, "metersPerPixel": 4.777, "metersPerTileSide": 1222.99 },
        { "level": 16, "metersPerPixel": 2.3887, "metersPerTileSide": 611.496 },
        { "level": 17, "metersPerPixel": 1.1943, "metersPerTileSide": 305.748 },
        { "level": 18, "metersPerPixel": 0.5972, "metersPerTileSide": 152.874 },
        { "level": 19, "metersPerPixel": 0.14929, "metersPerTileSide": 76.437 },
        { "level": 20, "metersPerPixel": 0.14929, "metersPerTileSide": 38.2185 },
        { "level": 21, "metersPerPixel": 0.074646, "metersPerTileSide": 19.10926 },
        { "level": 22, "metersPerPixel": 0.037323, "metersPerTileSide": 9.55463 },
        { "level": 23, "metersPerPixel": 0.0186615, "metersPerTileSide": 4.777315 },
        { "level": 24, "metersPerPixel": 0.00933075, "metersPerTileSide": 2.3886575 }
    ]

    def __init__(self, azure_subscription_key):
        self.azure_subscription_key = azure_subscription_key


    def _decode_polyline(self, polyline_str):
        index, lat, lng = 0, 0, 0
        coordinates = []
        changes = {'latitude': 0, 'longitude': 0}

        # Coordinates have variable length when encoded, so just keep
        # track of whether we've hit the end of the string. In each
        # while loop iteration, a single coordinate is decoded.
        while index < len(polyline_str):
            # Gather lat/lon changes, store them in a dictionary to apply them later
            for unit in ['latitude', 'longitude']:
                shift, result = 0, 0

                while True:
                    byte = ord(polyline_str[index]) - 63
                    index+=1
                    result |= (byte & 0x1f) << shift
                    shift += 5
                    if not byte >= 0x20:
                        break

                if (result & 1):
                    changes[unit] = ~(result >> 1)
                else:
                    changes[unit] = (result >> 1)

            lat += changes['latitude']
            lng += changes['longitude']

            coordinates.append([lng / 100000.0, lat / 100000.0])

        if len(coordinates) > 100:
            skipRecords = round(len(coordinates) / 100) + 1
            coordinates = coordinates[0::skipRecords]

        return coordinates


    def _get_coord_string(self, coordinates):
        coordStr = "|"
        for coord in coordinates:
            coordStr = coordStr + "|{0} {1}".format(coord[0], coord[1])

        return coordStr


    def _get_center_coord(self, coordinates):
        X = 0.0
        Y = 0.0
        Z = 0.0

        for coord in coordinates:
            lng = coord[0] * math.pi / 180
            lat = coord[1] * math.pi / 180

            X = X + (math.cos(lat) * math.cos(lng))
            Y = Y + (math.cos(lat) * math.sin(lng))
            Z = Z + math.sin(lat)

        X = X / len(coordinates)
        Y = Y / len(coordinates)
        Z = Z / len(coordinates)

        retLng = math.atan2(Y, X)
        hyp = math.sqrt(X * X + Y * Y)
        retLat = math.atan2(Z, hyp)

        return [retLng * 180 / math.pi, retLat * 180 / math.pi]

    def _get_zoom_level(self, coordinates):

        minLong = min(x[0] for x in coordinates)
        maxLong = max(x[0] for x in coordinates)
        minLat = min(x[1] for x in coordinates)
        maxLat = max(x[1] for x in coordinates)

        R = 6378.137 # Radius of earth in KM
        dLat = maxLat * math.pi / 180 - minLat * math.pi / 180
        dLon = maxLong * math.pi / 180 - minLong * math.pi / 180
        a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(minLat * math.pi / 180) * math.cos(maxLat * math.pi / 180) * math.sin(dLon / 2) * math.sin(dLon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c
        distanceInMeters = d * 1000

        zoomLevel = -1
        for level in self._tileZoomLevels:
            if level["metersPerTileSide"] > distanceInMeters:
                zoomLevel = level["level"]
            else:
                break

        return zoomLevel

    def get_image_url(self, polyline_string):
        try:
            coords = self._decode_polyline(polyline_string)
            coord_path = "lcEC5913|lw3" + self._get_coord_string(coords)
            url_encoded_coords = urllib.parse.quote(coord_path)
            center = self._get_center_coord(coords)
            zoom_level = self._get_zoom_level(coords)

            return "https://atlas.microsoft.com/map/static/png?subscription-key={0}&api-version=1.0&width=800&height=800&layer=basic&style=main&zoom={1}&center={2},{3}&path={4}".format(self.azure_subscription_key, zoom_level, center[0], center[1], url_encoded_coords)
        except:
            return ""
