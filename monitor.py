import requests
import csv
import time
from datetime import datetime

URL_FILE = "urls.txt"
CSV_FILE = "uptime_log.csv"
TIMEOUT_SEC = 5 # give up after ~5s
LATENCY_THRESHOLD = 2.0 #If >2s to respond, it is flagged as SLOW
SLEEP_SEC = 10

def load_urls(filename):

    try: 
        with open(filename, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: Could not find {filename}.")
    return []

def check_endpoint(url):
    start_time = time.perf_counter()

    #Add a basic User-Agent to reduce request blocking by some sites
    try: 
        headers = {"User-Agent": "Mozilla/5.0"}

        #Send the HTTP request
        response = requests.get(url, headers=headers, timeout=TIMEOUT_SEC)

        #Calculates how many seconds the request took
        latency = time.perf_counter() - start_time
        code = response.status_code

        if code >= 400:
            state = "UNHEALTHY"
        elif latency > LATENCY_THRESHOLD:
            state = "SLOW"
        else:
            state = "UP"

        return code, round(latency, 4), state
        
    except requests.exceptions.RequestException:
        return "ERR", 0.0, "DOWN"
    
# Main loop that keeps the script running
def run_monitor():
    
    urls = load_urls(URL_FILE)
    if not urls:
        return
    
    print(f"--- Service Monitor Started ---")
    print(f"Targets: {len(urls)} | Threshold: {LATENCY_THRESHOLD}s")
    print(f"Logging to {CSV_FILE}. Press ctrl + C to stop.\n")

    try:
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Endpoint", "Status Code", "Latency (s)", "State"])
    except PermissionError:
        print(f"Error: Close {CSV_FILE} first!")
        return
    
    try:
        while True:
            with open(CSV_FILE, "a", newline="") as f:
                writer = csv.writer(f)

                for url in urls:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    code, latency, state = check_endpoint(url)

                    writer.writerow([timestamp, url, code, latency, state])

                    print(f"[{timestamp}] {url} | {state} | {latency}s | Code: {code}")
            print("-" * 40)
            time.sleep(SLEEP_SEC)
    except KeyboardInterrupt:
        print("\nMonitor stopped by user. Exiting.")

if __name__ == "__main__":
    run_monitor()