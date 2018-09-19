import requests


url = "http://52.36.93.215:3000/createMetric"


def post(payload):
    return requests.post(url, json=payload)
