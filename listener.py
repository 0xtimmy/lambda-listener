import sys
import time
import argparse
import requests
import datetime
from pydub import AudioSegment
from pydub.playback import play


parser = argparse.ArgumentParser()
parser.add_argument("--sleep", default=5, type=float)
parser.add_argument("--keyfile", required=True)



# Select Types and regions below

VALID_TYPES = ['gpu_1x_h100_pcie', 'gpu_8x_a100_80gb_sxm4', 'gpu_1x_a10', 'gpu_1x_rtx6000', 'gpu_1x_a100', 'gpu_1x_a100_sxm4', 'gpu_2x_a100', 'gpu_4x_a100', 'gpu_8x_a100', 'gpu_1x_a6000', 'gpu_2x_a6000', 'gpu_4x_a6000', 'gpu_8x_v100']
types = ["gpu_1x_a100", "gpu_1x_a6000"]
VALID_REGIONS = ['us-south-1', 'us-west-1', 'us-west-2', 'us-west-3', 'us-midwest-1', 'us-east-1', 'europe-central-1', 'asia-south-1', 'me-west-1', 'asia-northeast-1', 'asia-northeast-2']
regions = ["us-south-1"]

if len(types) == 0: types = VALID_TYPES
if len(regions) == 0: regions = VALID_TYPES


def log(x):
    print(x)
    sys.stdout.flush()

def main():
    args = parser.parse_args()
    
    try:
        with open(args.keyfile, "r") as f:
            KEY = f.read()
            f.close()
    except FileNotFoundError:
        log(f"Keyfile not found at path: {args.keyfile}")
        return
    
    headers = { "Authorization": f"Bearer {KEY}" }
    
    try:
        while True:
            res = requests.get(
                "https://cloud.lambdalabs.com/api/v1/instance-types",
                headers=headers
            )
            result = res.json()["data"]
            
            availability = []
            
            for type in types:
                for region in regions:
                    if region in [x["name"] for x in result[type]['regions_with_capacity_available']]:
                        availability.append(f"{type} currently availibable in {region}")
            if len(availability) == 0:
                log(f"--- No Instances Available @ {datetime.datetime.now().isoformat()} ---")
            else:
                log(f"--- Instances Available @ {datetime.datetime.now().isoformat()} ---")
                for msg in availability:
                    log(msg)
                log("---")
                
                alarm_time = time.time()
                
                while alarm_time - time.time() < 20:
                    alarm = AudioSegment.from_wav("alarm.wav")
                    play(alarm)
                    time.sleep(.25)
                
            
            log("done")
                            
            time.sleep(args.sleep * 60)
    except KeyboardInterrupt:
        log("Terminating...")
        return

if __name__ == "__main__":
    main()
    