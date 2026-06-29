from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from datetime import datetime, timezone

app = FastAPI(
    title="Luminaires API – Δήμος Σητείας",
    description="Real-time status and geolocation for 133 street luminaires in Sitia.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Luminaire registry – all 133 LCU devices from Assets_list_for_Sitia
# ---------------------------------------------------------------------------
LUMINAIRES: list[dict] = [
    {"mac": "00124B001CE32574", "latitude": 35.07416, "longitude": 26.1385384, "wattage": 40},
    {"mac": "00124B001CE3265A", "latitude": 35.0742035, "longitude": 26.138113, "wattage": 40},
    {"mac": "00124B001CDE9597", "latitude": 35.0742378, "longitude": 26.13751, "wattage": 42},
    {"mac": "00124B001CE32641", "latitude": 35.0742149, "longitude": 26.137064, "wattage": 40},
    {"mac": "00124B001CE3268A", "latitude": 35.0741844, "longitude": 26.1366463, "wattage": 40},
    {"mac": "00124B001CE32515", "latitude": 35.2059975, "longitude": 26.1073151, "wattage": 0},
    {"mac": "00124B001CE32555", "latitude": 35.0750275, "longitude": 26.1382828, "wattage": 40},
    {"mac": "00124B001CE324E7", "latitude": 35.07481, "longitude": 26.1381721, "wattage": 40},
    {"mac": "00124B001CDE95D1", "latitude": 35.07481, "longitude": 26.1381721, "wattage": 39},
    {"mac": "00124B001CE32531", "latitude": 35.074398, "longitude": 26.1381, "wattage": 6542},
    {"mac": "00124B001CDE95C9", "latitude": 35.0744324, "longitude": 26.1384678, "wattage": 40},
    {"mac": "00124B001CDE95B8", "latitude": 35.0702934, "longitude": 26.1359138, "wattage": 0},
    {"mac": "00124B001CDE9664", "latitude": 35.07489, "longitude": 26.1390247, "wattage": 40},
    {"mac": "00124B001CDE9641", "latitude": 35.0747681, "longitude": 26.13882, "wattage": 40},
    {"mac": "00124B00193F3FBD", "latitude": 35.0740776, "longitude": 26.1389084, "wattage": 40},
    {"mac": "00124B001CDE961F", "latitude": 35.07399, "longitude": 26.1392879, "wattage": 40},
    {"mac": "00124B001CE32519", "latitude": 35.0740128, "longitude": 26.1393948, "wattage": 40},
    {"mac": "00124B001CE32516", "latitude": 35.073864, "longitude": 26.13953, "wattage": 40},
    {"mac": "00124B001CDE9648", "latitude": 35.07382, "longitude": 26.1394272, "wattage": 40},
    {"mac": "00124B001CE32535", "latitude": 35.0736237, "longitude": 26.13946, "wattage": 40},
    {"mac": "00124B00193F3FAD", "latitude": 35.07048, "longitude": 26.135828, "wattage": 0},
    {"mac": "00124B001CE32506", "latitude": 35.0740738, "longitude": 26.1397076, "wattage": 40},
    {"mac": "00124B001CDE9595", "latitude": 35.07439, "longitude": 26.139658, "wattage": 40},
    {"mac": "00124B001CDE962E", "latitude": 35.07464, "longitude": 26.1396027, "wattage": 40},
    {"mac": "00124B001CE327CE", "latitude": 35.0741539, "longitude": 26.14, "wattage": 41},
    {"mac": "00124B001CE3277C", "latitude": 35.074173, "longitude": 26.14022, "wattage": 40},
    {"mac": "00124B001CE32566", "latitude": 35.0742531, "longitude": 26.1406441, "wattage": 39},
    {"mac": "00124B001CDE967D", "latitude": 35.07441, "longitude": 26.1405869, "wattage": 41},
    {"mac": "00124B001CDE967C", "latitude": 35.07443, "longitude": 26.1399479, "wattage": 41},
    {"mac": "00124B001CE32661", "latitude": 35.0747261, "longitude": 26.1399632, "wattage": 40},
    {"mac": "00124B001CE32550", "latitude": 35.0749474, "longitude": 26.1399956, "wattage": 40},
    {"mac": "00124B001CE3265E", "latitude": 35.07502, "longitude": 26.1397057, "wattage": 40},
    {"mac": "00124B001CE325D5", "latitude": 35.0751343, "longitude": 26.1397476, "wattage": 40},
    {"mac": "00124B001CE32622", "latitude": 35.07491, "longitude": 26.1394424, "wattage": 40},
    {"mac": "00124B001CDE9623", "latitude": 35.07501, "longitude": 26.139082, "wattage": 40},
    {"mac": "00124B001CE3263E", "latitude": 35.0751381, "longitude": 26.1391983, "wattage": 40},
    {"mac": "00124B001CE325D3", "latitude": 35.0752373, "longitude": 26.13899, "wattage": 40},
    {"mac": "00124B001CE324F7", "latitude": 35.07505, "longitude": 26.1388721, "wattage": 41},
    {"mac": "00124B001CE3263D", "latitude": 35.0753555, "longitude": 26.1389542, "wattage": 40},
    {"mac": "00124B001CE32663", "latitude": 35.0753174, "longitude": 26.1385326, "wattage": 41},
    {"mac": "00124B001CE3286B", "latitude": 35.07539, "longitude": 26.13847, "wattage": 41},
    {"mac": "00124B001CE325F2", "latitude": 35.07514, "longitude": 26.1386013, "wattage": 40},
    {"mac": "00124B001CE3264B", "latitude": 35.07523, "longitude": 26.13807, "wattage": 40},
    {"mac": "00124B001CE32658", "latitude": 35.0753174, "longitude": 26.1375771, "wattage": 40},
    {"mac": "00124B001CE32674", "latitude": 35.0755, "longitude": 26.1377354, "wattage": 39},
    {"mac": "00124B001CE325B4", "latitude": 35.07552, "longitude": 26.13772, "wattage": 41},
    {"mac": "00124B001CE3262C", "latitude": 35.07569, "longitude": 26.13784, "wattage": 40},
    {"mac": "00124B001CE32554", "latitude": 35.0756569, "longitude": 26.1378288, "wattage": 41},
    {"mac": "00124B00193F3FA0", "latitude": 35.07555, "longitude": 26.138073, "wattage": 40},
    {"mac": "00124B001CE32646", "latitude": 35.07559, "longitude": 26.138464, "wattage": 40},
    {"mac": "00124B001CE32800", "latitude": 35.0755844, "longitude": 26.13898, "wattage": 41},
    {"mac": "00124B001CE32610", "latitude": 35.0759239, "longitude": 26.1392479, "wattage": 40},
    {"mac": "00124B001CE325E9", "latitude": 35.07579, "longitude": 26.1396332, "wattage": 41},
    {"mac": "00124B001CE325D2", "latitude": 35.07569, "longitude": 26.140089, "wattage": 40},
    {"mac": "00124B001CE326D4", "latitude": 35.0756149, "longitude": 26.14032, "wattage": 40},
    {"mac": "00124B001CE325C9", "latitude": 35.0757141, "longitude": 26.1408215, "wattage": 40},
    {"mac": "00124B001CE325CE", "latitude": 35.0757866, "longitude": 26.1411686, "wattage": 40},
    {"mac": "00124B001CE32633", "latitude": 35.07425, "longitude": 26.1401939, "wattage": 40},
    {"mac": "00124B001CE3270D", "latitude": 35.0746, "longitude": 26.140089, "wattage": 41},
    {"mac": "00124B001CE32625", "latitude": 35.0744133, "longitude": 26.14006, "wattage": 40},
    {"mac": "00124B001CE325FC", "latitude": 35.07434, "longitude": 26.1403313, "wattage": 40},
    {"mac": "00124B001CE325DD", "latitude": 35.0751839, "longitude": 26.140213, "wattage": 40},
    {"mac": "00124B001CE3252D", "latitude": 35.0753822, "longitude": 26.1403351, "wattage": 40},
    {"mac": "00124B001CE325E4", "latitude": 35.0754662, "longitude": 26.1402016, "wattage": 40},
    {"mac": "00124B001CE326E8", "latitude": 35.0753136, "longitude": 26.13967, "wattage": 40},
    {"mac": "00124B001CE3262E", "latitude": 35.07534, "longitude": 26.13951, "wattage": 40},
    {"mac": "00124B001CE32665", "latitude": 35.07531, "longitude": 26.1403351, "wattage": 40},
    {"mac": "00124B001CE325CF", "latitude": 35.0755, "longitude": 26.1410065, "wattage": 40},
    {"mac": "00124B001CE32667", "latitude": 35.0751, "longitude": 26.1408, "wattage": 40},
    {"mac": "00124B001CE32649", "latitude": 35.0752525, "longitude": 26.1408749, "wattage": 41},
    {"mac": "00124B001CE325E6", "latitude": 35.07522, "longitude": 26.1407089, "wattage": 41},
    {"mac": "00124B001CE325B0", "latitude": 35.0751381, "longitude": 26.140398, "wattage": 40},
    {"mac": "00124B001CE32585", "latitude": 35.07509, "longitude": 26.1401, "wattage": 40},
    {"mac": "00124B001CE325DA", "latitude": 35.074276, "longitude": 26.1410637, "wattage": 40},
    {"mac": "00124B00193F3FC1", "latitude": 35.0743065, "longitude": 26.1414547, "wattage": 39},
    {"mac": "00124B001CE326D6", "latitude": 35.0745, "longitude": 26.1411171, "wattage": 40},
    {"mac": "00124B001CE32686", "latitude": 35.074604, "longitude": 26.1418037, "wattage": 40},
    {"mac": "00124B001CE32652", "latitude": 35.0746155, "longitude": 26.14215, "wattage": 40},
    {"mac": "00124B001CE32695", "latitude": 35.0749359, "longitude": 26.1414165, "wattage": 40},
    {"mac": "00124B001CE325C0", "latitude": 35.0752144, "longitude": 26.141407, "wattage": 41},
    {"mac": "00124B001CE3271F", "latitude": 35.07527, "longitude": 26.14123, "wattage": 40},
    {"mac": "00124B001CE32586", "latitude": 35.07523, "longitude": 26.1410522, "wattage": 39},
    {"mac": "00124B001CE325DB", "latitude": 35.0751266, "longitude": 26.140976, "wattage": 41},
    {"mac": "00124B001CE3272E", "latitude": 35.0749321, "longitude": 26.1407757, "wattage": 40},
    {"mac": "00124B001CE32660", "latitude": 35.0749321, "longitude": 26.140379, "wattage": 40},
    {"mac": "00124B001CE3258C", "latitude": 35.0749664, "longitude": 26.1404171, "wattage": 39},
    {"mac": "00124B001CE32616", "latitude": 35.07551, "longitude": 26.1414185, "wattage": 40},
    {"mac": "00124B001CE325C1", "latitude": 35.07563, "longitude": 26.1417313, "wattage": 40},
    {"mac": "00124B001CE32685", "latitude": 35.0757637, "longitude": 26.1419659, "wattage": 41},
    {"mac": "00124B001CE32682", "latitude": 35.07568, "longitude": 26.1410236, "wattage": 40},
    {"mac": "00124B001CDE960A", "latitude": 35.0759354, "longitude": 26.1416321, "wattage": 40},
    {"mac": "00124B001CE327A8", "latitude": 35.0756035, "longitude": 26.14256, "wattage": 41},
    {"mac": "00124B001CDE965A", "latitude": 35.075573, "longitude": 26.1429157, "wattage": 40},
    {"mac": "00124B001CE32560", "latitude": 35.0751228, "longitude": 26.1417446, "wattage": 40},
    {"mac": "00124B001CE32540", "latitude": 35.0753365, "longitude": 26.14183, "wattage": 41},
    {"mac": "00124B001CDE95BE", "latitude": 35.07511, "longitude": 26.14212, "wattage": 40},
    {"mac": "00124B001CE32604", "latitude": 35.0751, "longitude": 26.14247, "wattage": 40},
    {"mac": "00124B001CE324C5", "latitude": 35.0743828, "longitude": 26.1429062, "wattage": 40},
    {"mac": "00124B001CE32877", "latitude": 35.0744171, "longitude": 26.1433449, "wattage": 40},
    {"mac": "00124B001CE3284F", "latitude": 35.07441, "longitude": 26.1438351, "wattage": 41},
    {"mac": "00124B00193F3FB0", "latitude": 35.07505, "longitude": 26.1435413, "wattage": 40},
    {"mac": "00124B001CE324CC", "latitude": 35.0748978, "longitude": 26.1441917, "wattage": 41},
    {"mac": "00124B001CE32799", "latitude": 35.07499, "longitude": 26.1433544, "wattage": 41},
    {"mac": "00124B001CDE95CE", "latitude": 35.0749855, "longitude": 26.14301, "wattage": 40},
    {"mac": "00124B001CE325ED", "latitude": 35.0751648, "longitude": 26.1428547, "wattage": 40},
    {"mac": "00124B001CE327D8", "latitude": 35.07526, "longitude": 26.1424446, "wattage": 41},
    {"mac": "00124B001CDE966D", "latitude": 35.0753, "longitude": 26.1420879, "wattage": 41},
    {"mac": "00124B00193F3FB7", "latitude": 35.07386, "longitude": 26.1406174, "wattage": 0},
    {"mac": "00124B00193F3F88", "latitude": 35.0739174, "longitude": 26.141098, "wattage": 0},
    {"mac": "00124B001CDE9660", "latitude": 35.0735779, "longitude": 26.1408043, "wattage": 0},
    {"mac": "00124B001CE325BB", "latitude": 35.07386, "longitude": 26.14064, "wattage": 0},
    {"mac": "00124B001CE326B4", "latitude": 35.07335, "longitude": 26.1409988, "wattage": 0},
    {"mac": "00124B001CE32676", "latitude": 35.0736923, "longitude": 26.1389351, "wattage": 40},
    {"mac": "00124B001CE32778", "latitude": 35.0733147, "longitude": 26.138752, "wattage": 40},
    {"mac": "00124B001CE32615", "latitude": 35.0734367, "longitude": 26.1395111, "wattage": 40},
    {"mac": "00124B001CE32684", "latitude": 35.0736961, "longitude": 26.1398449, "wattage": 40},
    {"mac": "00124B001CE32659", "latitude": 35.0740128, "longitude": 26.1374187, "wattage": 40},
    {"mac": "00124B001CE3263B", "latitude": 35.0736923, "longitude": 26.1372814, "wattage": 39},
    {"mac": "00124B001CE325C8", "latitude": 35.0733681, "longitude": 26.1374817, "wattage": 40},
    {"mac": "00124B001CE32609", "latitude": 35.0744324, "longitude": 26.13667, "wattage": 40},
    {"mac": "00124B001CE326B8", "latitude": 35.07444, "longitude": 26.13666, "wattage": 41},
    {"mac": "00124B001CE32738", "latitude": 35.0745773, "longitude": 26.1361351, "wattage": 40},
    {"mac": "00124B001CE3267E", "latitude": 35.0747566, "longitude": 26.13562, "wattage": 40},
    {"mac": "00124B001CE32657", "latitude": 35.075386, "longitude": 26.1431828, "wattage": 40},
    {"mac": "00124B001CE3274B", "latitude": 35.07533, "longitude": 26.1431236, "wattage": 40},
    {"mac": "00124B001CE32597", "latitude": 35.0754852, "longitude": 26.1425266, "wattage": 40},
    {"mac": "00124B001CE32772", "latitude": 35.0759544, "longitude": 26.139883, "wattage": 10},
    {"mac": "00124B001CE3266C", "latitude": 35.07569, "longitude": 26.1394253, "wattage": 40},
    {"mac": "00124B001CE3261E", "latitude": 35.0741043, "longitude": 26.1401443, "wattage": 40},
    {"mac": "00124B001CE32790", "latitude": 35.07572, "longitude": 26.13877, "wattage": 40},
    {"mac": "00124B001CDE95A1", "latitude": 35.07563, "longitude": 26.13848, "wattage": 39},
    {"mac": "00124B001CE32545", "latitude": 35.0749245, "longitude": 26.13848, "wattage": 40},
    {"mac": "00124B001CE327CA", "latitude": 35.0732536, "longitude": 26.13895, "wattage": 0},
]

LUMINAIRE_MAP: dict[str, dict] = {l["mac"]: l for l in LUMINAIRES}


# ---------------------------------------------------------------------------
# Status logic: active 20:00–06:00 UTC, inactive otherwise
# ---------------------------------------------------------------------------
def is_active_now() -> bool:
    hour = datetime.now(timezone.utc).hour
    return hour >= 20 or hour < 6


def luminaire_status(active: bool) -> str:
    return "active" if active else "inactive"


def enrich(lum: dict, active: bool) -> dict:
    return {
        "mac": lum["mac"],
        "latitude": lum["latitude"],
        "longitude": lum["longitude"],
        "wattage": lum["wattage"],
        "status": luminaire_status(active),
        "schedule": "20:00–06:00 UTC",
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
def health():
    active = is_active_now()
    return {
        "status": "ok",
        "service": "Luminaires API – Δήμος Σητείας",
        "utc_time": datetime.now(timezone.utc).isoformat(),
        "luminaires_active": active,
        "total_luminaires": len(LUMINAIRES),
    }


@app.get("/status", tags=["Status"])
def get_current_status():
    """Current global status of the luminaire network."""
    active = is_active_now()
    return {
        "utc_time": datetime.now(timezone.utc).isoformat(),
        "status": luminaire_status(active),
        "schedule": "Active: 20:00–06:00 UTC | Inactive: 06:00–20:00 UTC",
        "total_luminaires": len(LUMINAIRES),
    }


@app.get("/luminaires", tags=["Luminaires"])
def get_all_luminaires(
    status: Optional[str] = Query(None, description="Filter by 'active' or 'inactive'"),
):
    """All luminaires with geolocation and current status."""
    active = is_active_now()
    result = [enrich(l, active) for l in LUMINAIRES]
    if status in ("active", "inactive"):
        result = [r for r in result if r["status"] == status]
    return {
        "utc_time": datetime.now(timezone.utc).isoformat(),
        "current_status": luminaire_status(active),
        "count": len(result),
        "luminaires": result,
    }


@app.get("/luminaires/geojson/all", tags=["GeoJSON"])
def get_geojson():
    """GeoJSON FeatureCollection – ready for Leaflet, QGIS, Google Maps, etc."""
    active = is_active_now()
    features = [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [l["longitude"], l["latitude"]]},
            "properties": {
                "mac": l["mac"],
                "wattage": l["wattage"],
                "status": luminaire_status(active),
                "schedule": "20:00–06:00 UTC",
            },
        }
        for l in LUMINAIRES
    ]
    return {
        "type": "FeatureCollection",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "feature_count": len(features),
        "features": features,
    }


@app.get("/luminaires/{mac}", tags=["Luminaires"])
def get_luminaire(mac: str):
    """Single luminaire by MAC address."""
    lum = LUMINAIRE_MAP.get(mac.upper())
    if not lum:
        raise HTTPException(status_code=404, detail=f"Luminaire '{mac}' not found.")
    return enrich(lum, is_active_now())
