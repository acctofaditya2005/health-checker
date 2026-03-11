import requests
import json
import time
from datetime import datetime

URLS= [
    "https://google.com",
    "https://github.com",
    "https://this-fake-url-xyz123.com",
]

TIMEOUT = 5
LOG_FILE ="health_log.txt"
JSON_FILE = "health_results.json"

print("Health checker ready")
print(f"Checking {len(URLS)} URLs")


def check_url(url):
    start = time.time()    
    try:
        responses = requests.get(url, timeout = TIMEOUT)
        elapsed = round(time.time() - start, 2)
        return { 
              'url': url,
                'status_code': responses.status_code,
                'response_time': elapsed,
                'ok': True,
                'error': None}
    
    except requests.exceptions.Timeout:
            return {
                'url': url,
                'status_code': None,
                'response_time': None,
                'ok': False,
                'error':"TIMEOUT"
            }
    except requests.exceptions.ConnectionError:
            return {
                'url': url,
                'status_code': None,
                'response_time': None,
                'ok': False,
                'error':"CONNECTION"
            }
    
def print_summary(results):
    for result in results:
        if result['ok'] == True:
            print(f"✓ {result['url']} -> {result['status_code']} ({result['response_time']}s)")
        else:
            print(f"✗ {result['url']} -> {result['error']}")
    passed = len([r for r in results if r['ok'] == True])
    total = len(results)
    print(f"{passed}/{total} URLs healthy")

def save_log(results, filename):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a") as f:
        f.write(f"=== Health Check: {now} ===\n")
        for result in results:
            if result["ok"] == True:
                f.write(f"  OK     {result['url']} -> {result['status_code']} ({result['response_time']}s)\n")
            else:
                f.write(f"  FAILED {result['url']} -> {result['error']}\n")

def save_json(results, filename):
     with open(filename, 'w', encoding = "utf-8") as f:
        json.dump(results, f, indent = 2)


def main():
    results =[]
    for url in URLS:
        results.append(check_url(url))
   
    print_summary(results)
    save_log(results, LOG_FILE)
    save_json(results, JSON_FILE)
    print(f"Log saved to {LOG_FILE}")
    print(f"JSON saved to {JSON_FILE}")

if __name__ == "__main__":  
    main() 