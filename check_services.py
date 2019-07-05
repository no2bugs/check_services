#!/usr/bin/env python3

import requests
import sys


def http_get(url, time_out=60):
    try:
        resp = requests.get(url, timeout=time_out)
        if (100 <= resp.status_code < 600) and (resp.status_code != 200):
            raise ConnectionError('Error: Bad response code')
        print("Connected to", url)
    except ConnectionError as e:
        print('{0}\n{1} returned: {2} {3}'.format(e, url, resp.status_code, resp.reason))
        sys.exit(1)
    except Exception as e:
        print('Error: Something went wrong when connecting to {0}\n{1}'.format(url, e))
        sys.exit(1)

    return resp


def check_services_health(services):
    services_down = {}  # keep record of all downed services

    for service in services:
        if len(service) > 0:
            service_name = service.split(':')[0].strip()
            service_status = service.split(':')[1].strip()
            if service_status != 'OK':
                services_down[service_name] = service_status

    if services_down:
        # show all downed services before exit non 0
        for service, status in services_down.items():
            print('The service {0} is {1}'.format(service, status))
        sys.exit(1)
    else:
        print("All services are healthy")
        sys.exit(0)


if __name__ == "__main__":
    try:
        URL = sys.argv[1]
    except IndexError as e:
        print('Endpoint is missing. Must pass it as first argument (i.e. ./service_check.py <url>)')
        sys.exit(1)

    response = http_get(URL)
    services = response.content.decode('UTF-8').split("<br />")

    # sanity check in case content is empty or invalid formatting
    if not services:
        print('no services found')
        sys.exit(1)

    check_services_health(services)
