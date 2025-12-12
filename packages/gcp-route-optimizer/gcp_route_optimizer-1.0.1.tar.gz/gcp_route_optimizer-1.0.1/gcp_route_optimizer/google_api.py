import requests


def call_google_optimize(token: str, project_id: str, shipments: list, vehicles: list):
    """
    Calls the Google OptimizeTours API with dynamic project_id.
    """
    url = f"https://routeoptimization.googleapis.com/v1/projects/{project_id}:optimizeTours"

    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "model": {"shipments": shipments, "vehicles": vehicles},
            "populatePolylines": True
        }
    )
    return resp.json()
