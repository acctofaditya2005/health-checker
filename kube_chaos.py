import subprocess
import time
import json
from datetime import datetime

def get_pod_name():
    result = subprocess.run(['kubectl','get', 'pods', '--no-headers'], capture_output = True, text = True)
    return result.stdout.split("\n")[0].split()[0]

def kill_pod(pod_name):
    result = subprocess.run(['kubectl','delete','pod', pod_name], capture_output = True, text = True)
    print(f"Killed pod {pod_name}")
    time.sleep(2)

def wait_for_recovery():
    start = time.time()
    while True:
        result = subprocess.run(['kubectl', 'get', 'pods','--no-headers'], capture_output = True, text = True)
        if "Running" in result.stdout:
            RTO = round(time.time()-start, 2)
            print(f"Pod recovered in {RTO} seconds")
            return RTO
        else: 
            time.sleep(2)
            
def save_results(rto, pod_name):
    results = {'pod':pod_name, 'rto_seconds': rto, 'status': 'recovered', 'timestamp': str(datetime.now())}
    with open('results.json', 'w', encoding = 'utf-8') as f:
        json.dump(results, f, indent = 2)
    return results

def main():
    print("Starting KubeResilienceTester......")
    pod = get_pod_name()
    print(f"Pod name is {pod}")
    kill_pod(pod)
    rto = wait_for_recovery()
    print(f"RTO was: {rto} seconds")
    save_results(rto, pod)
    print("Result saved to results.json")

if __name__ == "__main__":
        main()