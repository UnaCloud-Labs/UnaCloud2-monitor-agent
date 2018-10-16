import requests


url = "http://157.253.205.40:3000/createMetric"


def post(payload):
    return requests.post(url, json=payload)
