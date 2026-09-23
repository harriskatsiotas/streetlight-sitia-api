from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime, timezone

app = FastAPI(
    title="Luminaires API – Δήμος Σητείας",
    description="Real-time status and geolocation for 133 street luminaires in Sitia.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Luminaire registry – all 133 LCU devices from Assets_list_for_Sitia
# ---------------------------------------------------------------------------
LUMINAIRES: list[dict] = [
    {"sl_id": "SI001", "mac": "00124B001CE32574", "latitude": 35.07416, "longitude": 26.1385384, "wattage": 40},
    {"sl_id": "SI002", "mac": "00124B001CE3265A", "latitude": 35.0742035, "longitude": 26.138113, "wattage": 40},
    {"sl_id": "SI003", "mac": "SI_PLACEHOLDER_003", "latitude": 35.0742378, "longitude": 26.13751, "wattage": 40},
    {"sl_id": "SI004", "mac": "00124B001CE32641", "latitude": 35.0742149, "longitude": 26.137064, "wattage": 40},
    {"sl_id": "SI005", "mac": "00124B001CE3268A", "latitude": 35.0741844, "longitude": 26.1366463, "wattage": 40},
    {"sl_id": "SI006", "mac": "00124B001CE32515", "latitude": 35.0746059, "longitude": 26.1374645, "wattage": 40},
    {"sl_id": "SI007", "mac": "00124B001CE32555", "latitude": 35.0750275, "longitude": 26.1382828, "wattage": 40},
    {"sl_id": "SI008", "mac": "00124B001CE324E7", "latitude": 35.07481, "longitude": 26.1381721, "wattage": 40},
    {"sl_id": "SI009", "mac": "00124B001CDE95D1", "latitude": 35.07481, "longitude": 26.1381721, "wattage": 40},
    {"sl_id": "SI010", "mac": "SI_PLACEHOLDER_010", "latitude": 35.074398, "longitude": 26.1381, "wattage": 40},
    {"sl_id": "SI011", "mac": "00124B001CDE95C9", "latitude": 35.0744324, "longitude": 26.1384678, "wattage": 40},
    {"sl_id": "SI012", "mac": "SI_PLACEHOLDER_012", "latitude": 35.0702934, "longitude": 26.1359138, "wattage": 40},
    {"sl_id": "SI013", "mac": "00124B001CDE9664", "latitude": 35.07489, "longitude": 26.1390247, "wattage": 40},
    {"sl_id": "SI014", "mac": "00124B001CDE9641", "latitude": 35.0747681, "longitude": 26.13882, "wattage": 40},
    {"sl_id": "SI015", "mac": "SI_PLACEHOLDER_015", "latitude": 35.0740776, "longitude": 26.1389084, "wattage": 40},
    {"sl_id": "SI016", "mac": "00124B001CDE961F", "latitude": 35.07399, "longitude": 26.1392879, "wattage": 40},
    {"sl_id": "SI017", "mac": "00124B001CE32519", "latitude": 35.0740128, "longitude": 26.1393948, "wattage": 40},
    {"sl_id": "SI018", "mac": "00124B001CE32516", "latitude": 35.073864, "longitude": 26.13953, "wattage": 40},
    {"sl_id": "SI019", "mac": "00124B001CDE9648", "latitude": 35.07382, "longitude": 26.1394272, "wattage": 40},
    {"sl_id": "SI020", "mac": "SI_PLACEHOLDER_020", "latitude": 35.0736237, "longitude": 26.13946, "wattage": 40},
    {"sl_id": "SI021", "mac": "00124B00193F3FAD", "latitude": 35.07048, "longitude": 26.135828, "wattage": 40},
    {"sl_id": "SI022", "mac": "00124B001CE32506", "latitude": 35.0740738, "longitude": 26.1397076, "wattage": 40},
    {"sl_id": "SI023", "mac": "SI_PLACEHOLDER_023", "latitude": 35.07439, "longitude": 26.139658, "wattage": 40},
    {"sl_id": "SI024", "mac": "00124B001CDE962E", "latitude": 35.07464, "longitude": 26.1396027, "wattage": 40},
    {"sl_id": "SI025", "mac": "00124B001CE327CE", "latitude": 35.0741539, "longitude": 26.14, "wattage": 40},
    {"sl_id": "SI026", "mac": "SI_PLACEHOLDER_026", "latitude": 35.074173, "longitude": 26.14022, "wattage": 40},
    {"sl_id": "SI027", "mac": "SI_PLACEHOLDER_027", "latitude": 35.0742531, "longitude": 26.1406441, "wattage": 40},
    {"sl_id": "SI028", "mac": "00124B001CDE967D", "latitude": 35.07441, "longitude": 26.1405869, "wattage": 40},
    {"sl_id": "SI029", "mac": "SI_PLACEHOLDER_029", "latitude": 35.07443, "longitude": 26.1399479, "wattage": 40},
    {"sl_id": "SI030", "mac": "00124B001CE32661", "latitude": 35.0747261, "longitude": 26.1399632, "wattage": 40},
    {"sl_id": "SI031", "mac": "00124B001CE32550", "latitude": 35.0749474, "longitude": 26.1399956, "wattage": 40},
    {"sl_id": "SI032", "mac": "00124B001CE3265E", "latitude": 35.07502, "longitude": 26.1397057, "wattage": 40},
    {"sl_id": "SI033", "mac": "SI_PLACEHOLDER_033", "latitude": 35.0751343, "longitude": 26.1397476, "wattage": 40},
    {"sl_id": "SI034", "mac": "SI_PLACEHOLDER_034", "latitude": 35.07491, "longitude": 26.1394424, "wattage": 40},
    {"sl_id": "SI035", "mac": "00124B001CDE9623", "latitude": 35.07501, "longitude": 26.139082, "wattage": 40},
    {"sl_id": "SI036", "mac": "SI_PLACEHOLDER_036", "latitude": 35.0751381, "longitude": 26.1391983, "wattage": 40},
    {"sl_id": "SI037", "mac": "00124B001CE325D3", "latitude": 35.0752373, "longitude": 26.13899, "wattage": 40},
    {"sl_id": "SI038", "mac": "SI_PLACEHOLDER_038", "latitude": 35.07505, "longitude": 26.1388721, "wattage": 40},
    {"sl_id": "SI039", "mac": "SI_PLACEHOLDER_039", "latitude": 35.0753555, "longitude": 26.1389542, "wattage": 40},
    {"sl_id": "SI040", "mac": "00124B001CE32663", "latitude": 35.0753174, "longitude": 26.1385326, "wattage": 40},
    {"sl_id": "SI041", "mac": "SI_PLACEHOLDER_041", "latitude": 35.07539, "longitude": 26.13847, "wattage": 40},
    {"sl_id": "SI042", "mac": "00124B001CE325F2", "latitude": 35.07514, "longitude": 26.1386013, "wattage": 40},
    {"sl_id": "SI043", "mac": "SI_PLACEHOLDER_043", "latitude": 35.07523, "longitude": 26.13807, "wattage": 40},
    {"sl_id": "SI044", "mac": "00124B001CE32658", "latitude": 35.0753174, "longitude": 26.1375771, "wattage": 40},
    {"sl_id": "SI045", "mac": "SI_PLACEHOLDER_045", "latitude": 35.0755, "longitude": 26.1377354, "wattage": 40},
    {"sl_id": "SI046", "mac": "00124B001CE325B4", "latitude": 35.07552, "longitude": 26.13772, "wattage": 40},
    {"sl_id": "SI047", "mac": "SI_PLACEHOLDER_047", "latitude": 35.07569, "longitude": 26.13784, "wattage": 40},
    {"sl_id": "SI048", "mac": "SI_PLACEHOLDER_048", "latitude": 35.0756569, "longitude": 26.1378288, "wattage": 40},
    {"sl_id": "SI049", "mac": "SI_PLACEHOLDER_049", "latitude": 35.07555, "longitude": 26.138073, "wattage": 40},
    {"sl_id": "SI050", "mac": "00124B001CE32646", "latitude": 35.07559, "longitude": 26.138464, "wattage": 40},
    {"sl_id": "SI051", "mac": "00124B001CE32800", "latitude": 35.0755844, "longitude": 26.13898, "wattage": 40},
    {"sl_id": "SI052", "mac": "00124B001CE32610", "latitude": 35.0759239, "longitude": 26.1392479, "wattage": 40},
    {"sl_id": "SI053", "mac": "00124B001CE325E9", "latitude": 35.07579, "longitude": 26.1396332, "wattage": 40},
    {"sl_id": "SI054", "mac": "SI_PLACEHOLDER_054", "latitude": 35.07569, "longitude": 26.140089, "wattage": 40},
    {"sl_id": "SI055", "mac": "00124B001CE326D4", "latitude": 35.0756149, "longitude": 26.14032, "wattage": 40},
    {"sl_id": "SI056", "mac": "00124B001CE325C9", "latitude": 35.0757141, "longitude": 26.1408215, "wattage": 40},
    {"sl_id": "SI057", "mac": "00124B001CE325CE", "latitude": 35.0757866, "longitude": 26.1411686, "wattage": 40},
    {"sl_id": "SI058", "mac": "SI_PLACEHOLDER_058", "latitude": 35.07425, "longitude": 26.1401939, "wattage": 40},
    {"sl_id": "SI059", "mac": "00124B001CE3270D", "latitude": 35.0746, "longitude": 26.140089, "wattage": 40},
    {"sl_id": "SI060", "mac": "00124B001CE32625", "latitude": 35.0744133, "longitude": 26.14006, "wattage": 40},
    {"sl_id": "SI061", "mac": "00124B001CE325FC", "latitude": 35.07434, "longitude": 26.1403313, "wattage": 40},
    {"sl_id": "SI062", "mac": "00124B001CE325DD", "latitude": 35.0751839, "longitude": 26.140213, "wattage": 40},
    {"sl_id": "SI063", "mac": "00124B001CE3252D", "latitude": 35.0753822, "longitude": 26.1403351, "wattage": 40},
    {"sl_id": "SI064", "mac": "00124B001CE325E4", "latitude": 35.0754662, "longitude": 26.1402016, "wattage": 40},
    {"sl_id": "SI065", "mac": "00124B001CE326E8", "latitude": 35.0753136, "longitude": 26.13967, "wattage": 40},
    {"sl_id": "SI066", "mac": "00124B001CE3262E", "latitude": 35.07534, "longitude": 26.13951, "wattage": 40},
    {"sl_id": "SI067", "mac": "00124B001CE32665", "latitude": 35.07531, "longitude": 26.1403351, "wattage": 40},
    {"sl_id": "SI068", "mac": "00124B001CE325CF", "latitude": 35.0755, "longitude": 26.1410065, "wattage": 40},
    {"sl_id": "SI069", "mac": "00124B001CE32667", "latitude": 35.0751, "longitude": 26.1408, "wattage": 40},
    {"sl_id": "SI070", "mac": "00124B001CE32649", "latitude": 35.0752525, "longitude": 26.1408749, "wattage": 40},
    {"sl_id": "SI071", "mac": "SI_PLACEHOLDER_071", "latitude": 35.07522, "longitude": 26.1407089, "wattage": 40},
    {"sl_id": "SI072", "mac": "00124B001CE325B0", "latitude": 35.0751381, "longitude": 26.140398, "wattage": 40},
    {"sl_id": "SI073", "mac": "SI_PLACEHOLDER_073", "latitude": 35.07509, "longitude": 26.1401, "wattage": 40},
    {"sl_id": "SI074", "mac": "00124B001CE325DA", "latitude": 35.074276, "longitude": 26.1410637, "wattage": 40},
    {"sl_id": "SI075", "mac": "00124B00193F3FC1", "latitude": 35.0743065, "longitude": 26.1414547, "wattage": 40},
    {"sl_id": "SI076", "mac": "SI_PLACEHOLDER_076", "latitude": 35.0745, "longitude": 26.1411171, "wattage": 40},
    {"sl_id": "SI077", "mac": "SI_PLACEHOLDER_077", "latitude": 35.074604, "longitude": 26.1418037, "wattage": 40},
    {"sl_id": "SI078", "mac": "SI_PLACEHOLDER_078", "latitude": 35.0746155, "longitude": 26.14215, "wattage": 40},
    {"sl_id": "SI079", "mac": "00124B001CE32695", "latitude": 35.0749359, "longitude": 26.1414165, "wattage": 40},
    {"sl_id": "SI080", "mac": "00124B001CE325C0", "latitude": 35.0752144, "longitude": 26.141407, "wattage": 40},
    {"sl_id": "SI081", "mac": "00124B001CE3271F", "latitude": 35.07527, "longitude": 26.14123, "wattage": 40},
    {"sl_id": "SI082", "mac": "SI_PLACEHOLDER_082", "latitude": 35.07523, "longitude": 26.1410522, "wattage": 40},
    {"sl_id": "SI083", "mac": "SI_PLACEHOLDER_083", "latitude": 35.0751266, "longitude": 26.140976, "wattage": 40},
    {"sl_id": "SI084", "mac": "00124B001CE3272E", "latitude": 35.0749321, "longitude": 26.1407757, "wattage": 40},
    {"sl_id": "SI085", "mac": "SI_PLACEHOLDER_085", "latitude": 35.0749321, "longitude": 26.140379, "wattage": 40},
    {"sl_id": "SI086", "mac": "00124B001CE3258C", "latitude": 35.0749664, "longitude": 26.1404171, "wattage": 40},
    {"sl_id": "SI087", "mac": "SI_PLACEHOLDER_087", "latitude": 35.07551, "longitude": 26.1414185, "wattage": 40},
    {"sl_id": "SI088", "mac": "00124B001CE325C1", "latitude": 35.07563, "longitude": 26.1417313, "wattage": 40},
    {"sl_id": "SI089", "mac": "00124B001CE32685", "latitude": 35.0757637, "longitude": 26.1419659, "wattage": 40},
    {"sl_id": "SI090", "mac": "00124B001CE32682", "latitude": 35.07568, "longitude": 26.1410236, "wattage": 40},
    {"sl_id": "SI091", "mac": "SI_PLACEHOLDER_091", "latitude": 35.0759354, "longitude": 26.1416321, "wattage": 40},
    {"sl_id": "SI092", "mac": "SI_PLACEHOLDER_092", "latitude": 35.0756035, "longitude": 26.14256, "wattage": 40},
    {"sl_id": "SI093", "mac": "00124B001CDE965A", "latitude": 35.075573, "longitude": 26.1429157, "wattage": 40},
    {"sl_id": "SI094", "mac": "SI_PLACEHOLDER_094", "latitude": 35.0751228, "longitude": 26.1417446, "wattage": 40},
    {"sl_id": "SI095", "mac": "00124B001CE32540", "latitude": 35.0753365, "longitude": 26.14183, "wattage": 40},
    {"sl_id": "SI096", "mac": "00124B001CDE95BE", "latitude": 35.07511, "longitude": 26.14212, "wattage": 40},
    {"sl_id": "SI097", "mac": "00124B001CE32604", "latitude": 35.0751, "longitude": 26.14247, "wattage": 40},
    {"sl_id": "SI098", "mac": "SI_PLACEHOLDER_098", "latitude": 35.0743828, "longitude": 26.1429062, "wattage": 40},
    {"sl_id": "SI099", "mac": "00124B001CE32877", "latitude": 35.0744171, "longitude": 26.1433449, "wattage": 40},
    {"sl_id": "SI100", "mac": "00124B001CE3284F", "latitude": 35.07441, "longitude": 26.1438351, "wattage": 40},
    {"sl_id": "SI101", "mac": "SI_PLACEHOLDER_101", "latitude": 35.07505, "longitude": 26.1435413, "wattage": 40},
    {"sl_id": "SI102", "mac": "00124B001CE324CC", "latitude": 35.0748978, "longitude": 26.1441917, "wattage": 40},
    {"sl_id": "SI103", "mac": "SI_PLACEHOLDER_103", "latitude": 35.07499, "longitude": 26.1433544, "wattage": 40},
    {"sl_id": "SI104", "mac": "00124B001CDE95CE", "latitude": 35.0749855, "longitude": 26.14301, "wattage": 40},
    {"sl_id": "SI105", "mac": "00124B001CE325ED", "latitude": 35.0751648, "longitude": 26.1428547, "wattage": 40},
    {"sl_id": "SI106", "mac": "00124B001CE327D8", "latitude": 35.07526, "longitude": 26.1424446, "wattage": 40},
    {"sl_id": "SI107", "mac": "00124B001CDE966D", "latitude": 35.0753, "longitude": 26.1420879, "wattage": 40},
    {"sl_id": "SI108", "mac": "SI_PLACEHOLDER_108", "latitude": 35.07386, "longitude": 26.1406174, "wattage": 40},
    {"sl_id": "SI109", "mac": "SI_PLACEHOLDER_109", "latitude": 35.0739174, "longitude": 26.141098, "wattage": 40},
    {"sl_id": "SI110", "mac": "00124B001CDE9660", "latitude": 35.0735779, "longitude": 26.1408043, "wattage": 40},
    {"sl_id": "SI111", "mac": "00124B001CE325BB", "latitude": 35.07386, "longitude": 26.14064, "wattage": 40},
    {"sl_id": "SI112", "mac": "SI_PLACEHOLDER_112", "latitude": 35.07335, "longitude": 26.1409988, "wattage": 40},
    {"sl_id": "SI113", "mac": "00124B001CE32676", "latitude": 35.0736923, "longitude": 26.1389351, "wattage": 40},
    {"sl_id": "SI114", "mac": "SI_PLACEHOLDER_114", "latitude": 35.0733147, "longitude": 26.138752, "wattage": 40},
    {"sl_id": "SI115", "mac": "00124B001CE32615", "latitude": 35.0734367, "longitude": 26.1395111, "wattage": 40},
    {"sl_id": "SI116", "mac": "00124B001CE32684", "latitude": 35.0736961, "longitude": 26.1398449, "wattage": 40},
    {"sl_id": "SI117", "mac": "SI_PLACEHOLDER_117", "latitude": 35.0740128, "longitude": 26.1374187, "wattage": 40},
    {"sl_id": "SI118", "mac": "00124B001CE3263B", "latitude": 35.0736923, "longitude": 26.1372814, "wattage": 40},
    {"sl_id": "SI119", "mac": "00124B001CE325C8", "latitude": 35.0733681, "longitude": 26.1374817, "wattage": 40},
    {"sl_id": "SI120", "mac": "00124B001CE32609", "latitude": 35.0744324, "longitude": 26.13667, "wattage": 40},
    {"sl_id": "SI121", "mac": "SI_PLACEHOLDER_121", "latitude": 35.07444, "longitude": 26.13666, "wattage": 40},
    {"sl_id": "SI122", "mac": "SI_PLACEHOLDER_122", "latitude": 35.0745773, "longitude": 26.1361351, "wattage": 40},
    {"sl_id": "SI123", "mac": "00124B001CE3267E", "latitude": 35.0747566, "longitude": 26.13562, "wattage": 40},
    {"sl_id": "SI124", "mac": "00124B001CE32657", "latitude": 35.075386, "longitude": 26.1431828, "wattage": 40},
    {"sl_id": "SI125", "mac": "00124B001CE3274B", "latitude": 35.07533, "longitude": 26.1431236, "wattage": 40},
    {"sl_id": "SI126", "mac": "00124B001CE32597", "latitude": 35.0754852, "longitude": 26.1425266, "wattage": 40},
    {"sl_id": "SI127", "mac": "SI_PLACEHOLDER_127", "latitude": 35.0759544, "longitude": 26.139883, "wattage": 40},
    {"sl_id": "SI128", "mac": "00124B001CE3266C", "latitude": 35.07569, "longitude": 26.1394253, "wattage": 40},
    {"sl_id": "SI129", "mac": "SI_PLACEHOLDER_129", "latitude": 35.0741043, "longitude": 26.1401443, "wattage": 40},
    {"sl_id": "SI130", "mac": "00124B001CE32790", "latitude": 35.07572, "longitude": 26.13877, "wattage": 40},
    {"sl_id": "SI131", "mac": "00124B001CDE95A1", "latitude": 35.07563, "longitude": 26.13848, "wattage": 40},
    {"sl_id": "SI132", "mac": "00124B001CE32545", "latitude": 35.0749245, "longitude": 26.13848, "wattage": 40},
    {"sl_id": "SI133", "mac": "00124B001CE327CA", "latitude": 35.0732536, "longitude": 26.13895, "wattage": 40},
]

LUMINAIRE_MAP: dict[str, dict] = {l["mac"]: l for l in LUMINAIRES}
LUMINAIRE_MAP_BY_SL: dict[str, dict] = {l["sl_id"]: l for l in LUMINAIRES}


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
        "sl_id": lum["sl_id"],
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
                "sl_id": l["sl_id"],
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
