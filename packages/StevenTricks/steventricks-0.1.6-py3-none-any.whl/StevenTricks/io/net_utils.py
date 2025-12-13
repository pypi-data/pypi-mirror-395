
#這裡是使用在爬蟲裡面request的header
headers = {
    'mac': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15',
    'safari14.0': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'iphone13': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1',
    'ipod13': 'Mozilla/5.0 (iPod; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1',
    'ipadmini13': 'Mozilla/5.0 (iPad; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1',
    'ipad': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Safari/605.1.15',
    'winedge': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
    'chromewin': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    'firefoxmac': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0',
    'firefoxwin': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
}
import requests as re
from traceback import format_exc
from StevenTricks.core.convert_utils import randomitem



def randomheader():
    # 隨機產生header，是一個iter
    while True:
        yield {"User-Agent": randomitem(headers)[1]}

import requests as re
from traceback import format_exc
from StevenTricks.core.convert_utils import randomitem

# ……上面原本的 headers 跟 randomheader() 保持不動……

def safereturn(res, packet, jsoncheck: bool = False):
    """
    安全處理 requests.Response，統一在 packet 裡紀錄狀態與錯誤訊息。

    參數
    ----
    res : requests.Response
        requests 回傳的 response 物件。
    packet : dict
        外部傳進來的紀錄用 dict，函式內會直接修改這個物件。
        - 新增 / 覆寫欄位：
            - 'restatuscode': HTTP 狀態碼
            - 'errormessage': 錯誤說明（只有失敗時才會出現）
    jsoncheck : bool, 預設 False
        若為 True，成功時會嘗試回傳 JSON 內容。

    回傳
    ----
    list
        - 若 status_code != 200 → 回傳 [None]
        - 若 jsoncheck=True 且 JSON 解析成功 → [json_obj]
        - 其他情況 → [None]
    """
    # 記錄狀態碼
    packet["restatuscode"] = res.status_code

    # 先檢查 HTTP 是否成功
    if res.status_code != re.codes.ok:
        packet["errormessage"] = f"{res.status_code} != {re.codes.ok}"
        return [None]

    # 不要求 JSON，就到此為止
    if not jsoncheck:
        return [None]

    # 需要 JSON → 嘗試解析
    try:
        jsontext = res.json()
    except Exception:
        packet["errormessage"] = format_exc()
        return [None]

    return [jsontext]


