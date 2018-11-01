import requests


url = "http://157.253.205.40:3000/{}"
createMetric = "createMetric"
readHardwareInfo = "readHardwareInfo" 


def post_metric(payload):
    return requests.post(url.format(createMetric), json=payload)

def post_hardware_info(payload):
    return requests.post(url.format(readHardwareInfo), json=payload)