#!/usr/bin/env python3
import base64, json, os, ssl, urllib.request

ES_URL = "https://elastic.cluen.com:9200/metricbeat-*/_search"
ES_USER = "elastic"
ES_PASS = "dm*9tygOEp7rm+mT-oCm"
SLACK_WEBHOOK = "https://hooks.slack.com/services/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"
STATE_FILE = "/tmp/k8s_alert_state.json"

def query_es(body):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(ES_URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    auth = base64.b64encode(f"{ES_USER}:{ES_PASS}".encode()).decode()
    req.add_header("Authorization", f"Basic {auth}")
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        return json.loads(resp.read().decode()).get("hits", {}).get("hits", [])

state = {}
if os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE) as f:
            state = json.load(f)
    except Exception:
        state = {}

alerts = []
new_state = {}

# 1. Check Pod Crashes & New Restarts in 'dev'
pod_hits = query_es({
    "size": 50,
    "sort": [{"@timestamp": "desc"}],
    "query": {"bool": {"filter": [
        {"range": {"@timestamp": {"gte": "now-24h"}}},
        {"term": {"kubernetes.namespace": "dev"}},
        {"exists": {"field": "kubernetes.container.name"}}
    ]}},
    "_source": ["kubernetes.pod.name", "kubernetes.container.status.reason", "kubernetes.container.status.restarts"]
})

latest_pods = {}
for h in pod_hits:
    k = h.get("_source", {}).get("kubernetes", {})
    pod = k.get("pod", {}).get("name")
    if pod and pod not in latest_pods:
        st = k.get("container", {}).get("status", {})
        latest_pods[pod] = (st.get("reason", "OK"), st.get("restarts", 0))

for pod, (reason, restarts) in latest_pods.items():
    prev = state.get(f"pod:{pod}", {"reason": "OK", "restarts": 0})
    is_bad = reason in ("CrashLoopBackOff", "OOMKilled", "ImagePullBackOff", "ErrImagePull")
    if is_bad or restarts > 0:
        new_state[f"pod:{pod}"] = {"reason": reason, "restarts": restarts}
        if restarts > prev.get("restarts", 0) or (is_bad and reason != prev.get("reason")):
            alerts.append(f"• *Pod Alert (`dev`):* `{pod}` — Status: `{reason}` | Restarts: `{restarts}`")

# 2. Check Node Disk / Memory / Ready Pressure
node_hits = query_es({
    "size": 10,
    "sort": [{"@timestamp": "desc"}],
    "query": {"bool": {"filter": [
        {"range": {"@timestamp": {"gte": "now-24h"}}},
        {"exists": {"field": "kubernetes.node.name"}}
    ]}},
    "_source": ["kubernetes.node.name", "kubernetes.node.status.ready", "kubernetes.node.status.disk_pressure", "kubernetes.node.status.memory_pressure"]
})

for h in node_hits:
    k = h.get("_source", {}).get("kubernetes", {})
    node = k.get("node", {}).get("name")
    st = k.get("node", {}).get("status", {})
    if node and (st.get("disk_pressure") or st.get("memory_pressure") or st.get("ready") is False):
        key = f"node:{node}"
        new_state[key] = True
        if not state.get(key):
            alerts.append(f"• *Node Pressure:* `{node}` (Ready={st.get('ready')}, DiskPressure={st.get('disk_pressure')}, MemPressure={st.get('memory_pressure')})")

with open(STATE_FILE, "w") as f:
    json.dump(new_state, f)

if alerts:
    payload = json.dumps({"text": "*Kubernetes Health Alert*\n" + "\n".join(alerts)}).encode()
    urllib.request.urlopen(urllib.request.Request(SLACK_WEBHOOK, data=payload, headers={"Content-Type": "application/json"}), timeout=10)
    print("Sent Slack alert:", alerts)
else:
    print("Healthy — no new state changes.")
