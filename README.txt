# Service Availability Monitor

A lightweight Python script that checks a list of web endpoints on a fixed interval and logs uptime + latency to a CSV file.

## Features
- Reads endpoints from an external file (`urls.txt`)
- Measures latency and classifies endpoints as: UP / SLOW / UNHEALTHY / DOWN
- Logs results to `uptime_log.csv` with timestamps
- Exit with Ctrl+C

## Setup
```bash
pip install -r requirements.txt
