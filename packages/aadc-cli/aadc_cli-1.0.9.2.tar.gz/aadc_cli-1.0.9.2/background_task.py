import time
import sys

print("Starting 10 minute background task...")
sys.stdout.flush()

for i in range(10):
    time.sleep(60)
    print(f"Task running: {i+1} minutes elapsed")
    sys.stdout.flush()

print("Task complete!")
