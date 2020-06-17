import requests
from time import time, sleep

requests.packages.urllib3.disable_warnings()


def http_check(
    url='',
    http_verb='get',
    headers='',
    params='',
    payload='',
    auth='',
    timeout=1,
    scan_timeout=480,
    retry=1,
    message_to_display=10
):
    ''''

    '''
    end_time = time() + scan_timeout
    counter = 1
    while end_time > time():
        try:
            response = requests.request(
                http_verb,
                url=url,
                headers=headers,
                params=params,
                json=payload,
                auth=auth,
                timeout=timeout,
                verify=False)
            response.raise_for_status()
            return response
        except Exception as e:
            scan_timeout = scan_timeout - retry
            if counter == message_to_display:
                print(f"{url} reports {str(e)}..sleeping for {retry} "
                      f"seconds ({scan_timeout} seconds left)")
                counter = 1
            else:
                counter += 1
            sleep(retry)
    return None


def main():
    url = 'http://127.0.0.1:9000'
    response = http_check(url=url, scan_timeout=100)
    if response is None:
        print(f"{url} is unavailable")
    else:
        print(f"{url} is responsive with {response.status_code}")


if __name__ == "__main__":
    main()
