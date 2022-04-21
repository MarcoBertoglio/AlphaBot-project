import requests

r = requests.get(f"http://192.168.0.138:5000//api/v1/motors/both?pwml={0}&pwmr={0}&tempo={0.3}")