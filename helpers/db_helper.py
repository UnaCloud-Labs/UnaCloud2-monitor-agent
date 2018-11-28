import requests


base_url = "http://157.253.205.40:3000/{}"

metric = "createMetric"
initial_info = "hardwareInfo"
processes = "processes"
offline = "recoveredData"
print_payload = False

error_response = requests.Response()
error_response.status_code = 0

def post(url, payload):
    if print_payload:
        print(payload)
    try:
        return requests.post(base_url.format(url), json=payload, timeout=0.5)
    except OSError:
        print(OSError)
        return error_response
