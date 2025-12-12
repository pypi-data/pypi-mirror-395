def build_shipments(orders: list):
    """
    Builds Google 'shipments' structure from order list.
    """
    shipments = []

    for i, o in enumerate(orders):
        shipments.append({
            "label": str(i),
            "penaltyCost": 1000,
            "deliveries": [{
                "arrivalWaypoint": {
                    "location": {
                        "latLng": {
                            "latitude": float(o["delivery_lat"]),
                            "longitude": float(o["delivery_lng"])
                        }
                    }
                }
            }]
        })

    return shipments


def build_vehicle(warehouse: dict):
    """
    Builds the Google vehicle config.
    """
    lat = float(warehouse["lat"])
    lng = float(warehouse["lng"])

    return [{
        "label": "v1",
        "costPerKilometer": 1.0,
        "startWaypoint": {"location": {"latLng": {"latitude": lat, "longitude": lng}}},
        "endWaypoint": {"location": {"latLng": {"latitude": lat, "longitude": lng}}}
    }]
