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


def check_services_health(services, status_delimiter):
    services_down = {}  # keep record of all downed services

    for service in services:
        service_name = service.split(status_delimiter)[0]
        service_status = service.split(status_delimiter)[1]
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


def input_formatter(input, services_delimiter, status_delimiter):
    # remove blank results and extra spaces
    formatted_input = [x.replace(status_delimiter + ' ', status_delimiter).strip() for x in
                       list(filter(None, input.split(services_delimiter)))]

    # perform input validation
    for item in formatted_input:
        if len(item.split(status_delimiter)) != 2:
            print('invalid format detected in {}'.format(item))
            print('services are expected to be separated by "{0}" and status by "{1}"'.format(services_delimiter,
                                                                                              status_delimiter))
            sys.exit(1)

    return formatted_input


if __name__ == "__main__":
    try:
        URL = sys.argv[1]
    except IndexError:
        print('Error: endpoint is missing\nMust pass it as first argument (i.e. ./check_services.py <url>)')
        sys.exit(1)

    response = http_get(URL).content.decode('UTF-8')

    # set delimiters according to content format
    services_delimiter = '<br />'
    service_status_delimiter = ':'

    # parse response into services list
    services = input_formatter(response, services_delimiter=services_delimiter, status_delimiter=service_status_delimiter)

    # sanity check in case content is empty
    if not services:
        print('Error: no services found in', URL)
        sys.exit(1)

    check_services_health(services, status_delimiter=service_status_delimiter)
