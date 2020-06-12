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
    scan_timeout=480,
    retry=1
):
    ''''

    '''
    end_time = time() + scan_timeout
    while end_time > time():
        try:
            response = requests.request(
                http_verb,
                url=url,
                headers=headers,
                params=params,
                json=payload,
                auth=auth,
                verify=False)
            response.raise_for_status()
            return response
        except Exception as e:
            scan_timeout = scan_timeout - retry
            print(f"{url} reports {str(e)}..sleeping for {retry} "
                  f"seconds ({scan_timeout} seconds left)")
            sleep(retry)
    return None


def main():
    url = 'https://10.1.1.111'
    response = http_check(url=url, scan_timeout=10)
    if response is None:
        print(f"{url} is unavailable")
    else:
        print(f"{url} is responsive with {response.status_code}")


if __name__ == "__main__":
    main()
