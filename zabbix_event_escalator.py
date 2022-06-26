import json, os, secrets, argparse, logging, http.client

class ApiRequest:
    jsonrpc: str
    method:  str
    params:  dict
    auth:    str
    id:      str

    def __init__(self) -> None:
        self.jsonrpc = "2.0"
        self.id = secrets.token_hex(8)
        self.auth = os.getenv("ESCALATOR_TOKEN")

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def check_response(r): 
    if r.code != 200:
        log.warning(f"Connection terminated with code {r.code}")
        exit(1)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Raise zabbix event severity by 1\r\nRequired environment variable ESCALATOR_TOKEN with valid zabbix api token",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-e", dest="event", type=int, help="zabbix event id (int)", required=True)
    args = parser.parse_args()
    event = str(args.event)

    logging.basicConfig(format='%(asctime)s: %(message)s')
    log = logging.getLogger(__name__)

    if os.getenv("ESCALATOR_TOKEN") is None:
        log.warning("Environment variable ESCALATOR_TOKEN not set")
        exit(1)

    problem = ApiRequest()
    problem.method = "problem.get"
    problem.params = {
        "output": ["eventid", "severity"],
        "eventids": event
    }

    headers = {'Content-Type': 'application/json-rpc'}
    conn = http.client.HTTPSConnection("monitoring.nexusprotocol.tech")
    conn.request("POST", "/api_jsonrpc.php", problem.to_json(), headers)

    getresponse = conn.getresponse()
    check_response(getresponse)

    data = json.loads(getresponse.read())
    data = data["result"][0]
    data["severity"] = int(data["severity"])
    
    if (data["severity"]) < 6:
        data["severity"] += 1
        data["severity"] = str(data["severity"])
    else: 
        exit(0)

    escalate = ApiRequest()
    escalate.method = "event.acknowledge"
    escalate.params = {
        "eventids": data["eventid"],
        "action": "14",
        "message": "Event severity escalation",
        "severity": data["severity"]
    }

    conn.request("POST", "/api_jsonrpc.php", escalate.to_json(), headers)
    getresponse = conn.getresponse()
    check_response(getresponse)
    
    log.info("Request successfully sent")
    exit(0)
    
