def to_geojson(place):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [place.longitude, place.latitude]
        },
        "properties": {
            "geonameid": place.geonameid,
            "name": place.name,
            "asciiname": place.asciiname,
            "alternatenames": place.alternatenames,
            "country": place.country,
            "population": place.population,
            "timezone": place.timezone,
        }
    }
