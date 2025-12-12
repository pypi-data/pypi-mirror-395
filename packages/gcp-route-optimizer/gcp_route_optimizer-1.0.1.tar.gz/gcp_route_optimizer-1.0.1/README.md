# gcp_route_optimizer

`gcp_route_optimizer` is a lightweight Python library that simplifies using the **Google Fleet Routing / OptimizeTours API**.

It automatically:

- Extracts the `project_id` from your Google Service Account JSON
- Generates OAuth tokens using the service account credentials
- Builds shipments and vehicle structures
- Sends requests to the OptimizeTours API
- Returns the optimized polyline + visit sequence

This library contains **no AWS, SSM, DynamoDB, SQS, or Flask logic**, making it reusable across any backend environment (Flask, FastAPI, Django, AWS Lambda, GCP Functions, EBS, etc.).

---

## 🚀 Features

- Pure Google Route Optimization logic
- Simple Python API
- Auto token generation from service-account JSON
- Clean structure and production-ready code
- Works with any application layer (Flask, EB, Lambda)
- Python 3.9+ compatible

---

## 📦 Installation

Install from PyPI:

```bash
pip install gcp-route-optimizer
