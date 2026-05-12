"""Launch coordinate seeds for V1.

NPS publishes launch thresholds on the boating page, but the threshold list does
not include coordinates. V1 uses a lightweight coordinate lookup seeded from
public NPS structured data where available and public OpenStreetMap slipway
features / public map review for launch-only points.
"""


LAUNCH_COORDINATES = {
    "Hawk Creek": {"latitude": 47.8974, "longitude": -118.1744, "source": "OpenStreetMap slipway near Hawk Creek / NPS place page"},
    "Marcus Island": {"latitude": 48.6664, "longitude": -118.0652, "source": "OpenStreetMap named slipway / NPS place page"},
    "Evans": {"latitude": 48.6992, "longitude": -118.0197, "source": "OpenStreetMap named slipway / NPS place page"},
    "North Gorge": {"latitude": 48.7868, "longitude": -118.0014, "source": "OpenStreetMap named slipway / NPS structured data"},
    "Napoleon Bridge": {"latitude": 48.7346, "longitude": -118.1164, "source": "OpenStreetMap named slipway / NPS place page"},
    "Snag Cove": {"latitude": 48.7330, "longitude": -118.0590, "source": "OpenStreetMap named slipway / NPS structured data"},
    "China Bend": {"latitude": 48.8103, "longitude": -117.9511, "source": "OpenStreetMap named slipway / NPS place page"},
    "Jones Bay": {"latitude": 47.8762, "longitude": -118.4680, "source": "OpenStreetMap slipway / NPS structured data vicinity"},
    "Crescent Bay": {"latitude": 47.9375, "longitude": -118.9858, "source": "OpenStreetMap slipway / public map review"},
    "Daisy": {"latitude": 48.3755, "longitude": -118.1679, "source": "OpenStreetMap named slipway / NPS place page"},
    "French Rocks": {"latitude": 48.4947, "longitude": -118.1976, "source": "OpenStreetMap named slipway"},
    "Hanson Harbor": {"latitude": 47.8724, "longitude": -119.0984, "source": "OpenStreetMap slipway / public map review"},
    "Bradbury Beach": {"latitude": 47.9355, "longitude": -118.9350, "source": "OpenStreetMap slipway / public map review"},
    "Gifford": {"latitude": 48.2885, "longitude": -118.1453, "source": "OpenStreetMap named slipway / NPS place page"},
    "Fort Spokane": {"latitude": 47.9096, "longitude": -118.3110, "source": "OpenStreetMap named slipway / NPS structured data vicinity"},
    "Lincoln Mill": {"latitude": 47.9206, "longitude": -118.5823, "source": "OpenStreetMap slipway / public map review"},
    "Porcupine Bay": {"latitude": 47.8300, "longitude": -118.4062, "source": "OpenStreetMap slipway / NPS structured data vicinity"},
    "Kettle Falls": {"latitude": 48.6106, "longitude": -118.1204, "source": "OpenStreetMap slipway / NPS structured data vicinity"},
    "Hunters Camp": {"latitude": 48.1296, "longitude": -118.2254, "source": "OpenStreetMap named slipway / NPS place page"},
    "Keller Ferry": {"latitude": 47.9375, "longitude": -118.9858, "source": "OpenStreetMap slipway / concessionaire vicinity"},
    "Seven Bays": {"latitude": 47.9273, "longitude": -119.0567, "source": "OpenStreetMap slipway / public map review"},
    "Spring Canyon": {"latitude": 47.9355, "longitude": -119.0304, "source": "OpenStreetMap slipway / NPS structured data vicinity"},
}

