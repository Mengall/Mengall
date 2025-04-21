import time
import requests

def wait_for_image(url, timeout=15, interval=3):
    """
    轮询检测图像是否可以访问。
    - timeout: 最长等待时间（秒）
    - interval: 每次轮询间隔时间（秒）
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            result_url = f"{url}?v={int(time.time())}"
            print(result_url)
            res = requests.get(result_url)
            print(result_url)
            if res.status_code == 200:
                return result_url
        except Exception as e:
            print(f"等待图像可访问时出错: {e}")
        time.sleep(interval)
    return None

url = "https://abcd.com/a.png"
wait_for_image(url)