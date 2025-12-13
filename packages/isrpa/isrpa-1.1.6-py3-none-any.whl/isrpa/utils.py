import os

import redis
import requests
import tldextract
from dotenv import load_dotenv

load_dotenv("/isearch/aiAgent/.env", override=True)
address = os.getenv("ADDRESS")
vnc_address = os.getenv("VNC_ADDRESS")
browser_type= os.environ.get('BROWSER_TYPE')
client = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=os.getenv("REDIS_DB"),
                     password=os.getenv("REDIS_PASSWORD"))


class Util:
    def get_path(self, user_name):
        url = f"{address}/client/getPath"
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            'user_name': user_name
        }
        response = requests.post(url, headers=headers, json=data)
        return response

    def get_vnc_path(self, email, app_id):
        url = f"{address}/client/get_vncpath?email={email}&app_id={app_id}"
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        return response

    def get_webSocketDebuggerUrl(self, host, port):
        url = f"http://{host}:{port}/json/version"
        r = requests.get(url, headers={"Connection": "close"}, stream=True, timeout=5)
        if r.status_code != 200:
            return "failure"
        url = r.json().get('webSocketDebuggerUrl')
        r.close()
        return url

    def get_websocket_data(self, host, port):
        url = f"http://{host}:{port}/json"
        r = requests.get(url, headers={"Connection": "close"}, stream=True, timeout=5)
        if r.status_code != 200:
            return "failure"
        data = r.json()
        r.close()
        return data

    def get_ws_url(self, host, port):
        for _ in range(3):
            try:
                return self.get_webSocketDebuggerUrl(host, port)
            except Exception as e:
                pass

    def get_json(self, host, port):
        for _ in range(3):
            try:
                return self.get_websocket_data(host, port)
            except Exception as e:
                pass

def getPath(user_name):
    """
    获取cdp_url
    """
    response = Util().get_path(user_name)
    if response.status_code != 200:
        return "failure"
    data = response.json()
    return f"ws://{data.get('ip_address')}:{data.get('port')}"


def get_ssh_path(user_name):
    """
    获取cdp_url
    """
    response = Util().get_path(user_name)
    if response.status_code != 200:
        return "failure"
    port = response.json().get('port')
    ws_url = Util().get_ws_url("localhost", port)
    return ws_url


def get_vnc_path(email, app_id):
    """
    获取cdp_url
    """
    response = Util().get_vnc_path(email, app_id)
    if response.status_code != 200:
        return "failure"
    port = response.json().get('port')
    ws_url = Util().get_ws_url(vnc_address, port)
    return ws_url


def get_url(user_name):
    """
    获取当前激活page的url
    """
    response = Util().get_path(user_name)
    if response.status_code != 200:
        return "failure"
    port = response.json().get('port')
    pages = Util().get_json("localhost", port)
    if pages:
        for page in pages:
            if (
                    page.get("url").startswith("chrome-extension://") or
                    page.get("url").startswith("chrome-untrusted://") or
                    page.get("title") == "MagicalAutomator-sidePanel"
            ):
                continue
            else:
                if page.get("url") == "chrome://newtab/":
                    return "chrome://new-tab-page/"
                return page.get("url")
    return None


def get_active_url(user_name):
    """
    获取当前激活page的id
    """
    response = Util().get_path(user_name)
    if response.status_code != 200:
        return "failure"
    port = response.json().get('port')
    pages = Util().get_json("localhost", port)
    if pages:
        for page in pages:
            if (
                    page.get("url").startswith("chrome-extension://") or
                    page.get("url").startswith("chrome-untrusted://") or
                    page.get("title") == "MagicalAutomator-sidePanel"
            ):
                continue
            return page.get("id")
    return None


def get_vnc_active_url(email, app_id):
    """
    获取当前激活page的id
    """
    response = Util().get_vnc_path(email, app_id)
    if response.status_code != 200:
        return "failure"
    port = response.json().get('port')
    pages = Util().get_json(vnc_address, port)
    if pages:
        for page in pages:
            if (
                    page.get("url").startswith("chrome-extension://") or
                    page.get("url").startswith("chrome-untrusted://") or
                    page.get("title") == "MagicalAutomator-sidePanel"
            ):
                continue
            return page.get("id")
    return None


def get_active_page(browser, active_page_id):
    """
    获取当前激活page对象
    """
    context = browser.contexts[0]
    context.add_init_script('''localStorage.setItem('devtool', 'open');''')
    for page in context.pages:
        client = page.context.new_cdp_session(page)
        target_info = client.send("Target.getTargetInfo")
        if target_info.get('targetInfo').get('targetId') == active_page_id:
            page.bring_to_front()
            return page


def set_playwright_file_path(key, value):
    """
    redis存储下载文件的地址
    """
    client.set(key, value, ex=30)


def upload_file(file_path, dest_file, user_name):
    """
    通知客户端上传文件
    """

    url = f"{address}/client/noticeUpload"
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'file_path': file_path,
        'dest_file': dest_file,
        'user_name': user_name
    }
    requests.post(url, headers=headers, json=data)


def vCode(image: str, code_type, apiKey, secretKey):
    """
    ocr 识别图片验证码
    """
    url = "https://ai.i-search.com.cn/ocr/v2/vCode"
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'image': image,
        'code_type': code_type,
        'apiKey': apiKey,
        'secretKey': secretKey
    }
    response = requests.post(url, headers=headers, json=data)
    status_code = response.status_code
    if status_code != 200:
        return {"error_msg": "failure", "error_code": status_code}
    return response.json()


def save_file(url, cookies, file_path):
    """
    playwright保存文件
    """
    extracted = tldextract.extract(url)
    top_level_domain = f"{extracted.domain}.{extracted.suffix}"
    cookie = {}
    for item in cookies:
        if top_level_domain in item.get("domain"):
            cookie[item["name"]] = item["value"]
    response = requests.get(url, cookies=cookie)
    with open(file_path, 'wb') as file:
        file.write(response.content)


def get_com_active_url(user_name,app_id=None):
    if browser_type == 1:
        target_id = get_vnc_active_url(user_name, app_id)
    else:
        target_id = get_active_url(user_name)
    return target_id

def get_com_path(user_name,app_id=None):
    if browser_type == 1:
        path = get_vnc_path(user_name, app_id)
    else:
        path = get_ssh_path(user_name)
    return path