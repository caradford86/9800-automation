import requests
from time import time, sleep


def http_check(
    url='',
    http_verb='get',
    headers='',
    params='',
    payload='',
    scan_timeout=120,
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
                json=payload)
            response.raise_for_status()
            return response
        except Exception as e:
            scan_timeout = scan_timeout - retry
            print(f"{url} reports {str(e)}..sleeping for {retry} "
                  f"seconds ({scan_timeout} seconds left)")
            sleep(retry)
    return None


def main():
    url = 'http://127.0.0.1:9000'
    response = http_check(url=url, scan_timeout=10)
    if response is None:
        print(f"{url} is unavailable")
    else:
        print(response.status_code)


if __name__ == "__main__":
    main()
