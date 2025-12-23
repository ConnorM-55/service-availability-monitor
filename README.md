# Service Availability Monitor

Small Python tool that checks a list of URLs on a fixed interval and logs the results to a CSV.
## What it does
- Reads endpoints from "urls.txt" (one per line)
- Sends an HTTP GET request to each endpoint
- Measures response time and records the following:
    - **UP** (Connected in <2s and HTTP status <400)
    - **SLOW** (HTTPS status is under 400, but latency is over the threshold)
    - **UNHEALTHY** (HTTP status is 4xx or 5xx)
    - **DOWN** (Timeout, DNS error, or a connection error)
- Saves results to "uptime_log.csv" with timestamps

## Setup
```bash
pip install -r requirements.txt
