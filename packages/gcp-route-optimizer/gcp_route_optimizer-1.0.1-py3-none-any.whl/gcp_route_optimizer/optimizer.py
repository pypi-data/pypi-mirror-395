from .builders import build_shipments, build_vehicle
from .google_api import call_google_optimize
from .google_token import generate_google_token


class RouteOptimizer:
    """
    Core route optimizer.
    Flask provides service_account_json; library auto-extracts project_id.
    """

    def __init__(self, service_account_json: dict, warehouse_location: dict):
        """
        service_account_json: decrypted Google SA JSON dict
        warehouse_location: Dict containing {lat, lng}
        """
        self.service_account_json = service_account_json
        self.warehouse = warehouse_location

    def optimize(self, orders: list):
        """
        Optimize delivery route using Google OptimizeTours API.
        Returns: (result_dict, success_bool)
        """
        if not orders:
            return {"error": "No orders"}, False

        # Auto-fetch project ID from JSON
        project_id = self.service_account_json.get("project_id")
        if not project_id:
            return {"error": "project_id missing in service account JSON"}, False

        # Generate token from JSON
        token = generate_google_token(self.service_account_json)
        if not token:
            return {"error": "Failed to generate Google token"}, False

        shipments = build_shipments(orders)
        vehicles = build_vehicle(self.warehouse)

        # Call Google API
        resp = call_google_optimize(
            token=token,
            project_id=project_id,
            shipments=shipments,
            vehicles=vehicles
        )

        if "routes" not in resp:
            return {"error": "Google optimization failed", "details": resp}, False

        route = resp["routes"][0]
        polyline = route["routePolyline"]["points"]
        visits = route.get("visits", [])

        return {
            "polyline": polyline,
            "visits": visits
        }, True
