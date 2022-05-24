from time import sleep
from random import randint

import requests
from requests.exceptions import HTTPError

def main():
    while True:
        for url in ['https://s3.amazonaws.com/logicmonitor-marketing/sitemonitor_ips.json', 'https://api.github.com/invalid']:
            for x in range(randint(1,3)):
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                except HTTPError as http_err:
                    print(f'HTTP error occurred: {http_err}')  # Python 3.6
                except Exception as err:
                    print(f'Other error occurred: {err}')  # Python 3.6
                else:
                    print('Success!')
                sleep(randint(3,5))
            sleep(randint(25,45))

if __name__ == "__main__":
    main()