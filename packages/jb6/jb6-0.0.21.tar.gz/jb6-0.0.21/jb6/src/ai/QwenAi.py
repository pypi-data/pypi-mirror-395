import os
import re
import uuid
import magic
import requests
import curl_cffi
import json_repair as json

model_map = {
    "Qwen3-Max": "tongyi-qwen3-max-model",
    "Qwen3-Max-Thinking-Preview": "tongyi-qwen3-max-thinking",
    "Qwen3-Plus": "tongyi-qwen-plus-latest",
    "Qwen3-Coder": "tongyi-qwen3-coder",
    "Qwen3-VL-32B": "tongyi-qwen3-vl-32b",
    "Qwen3-VL-30B-A3B": "tongyi-qwen3-vl-30b-a3b-instruct",
    "Qwen3-Omni-Flash": "tongyi-qwen3-omni-flash",
    "Qwen3-Next-80B-A3B": "tongyi-qwen3-next-80b-a3b",
    "Qwen3-235B-A22B-2507": "tongyi-qwen3-235b-a22b-instruct-2507",
    "Qwen3-VL-235B-A22B": "tongyi-qwen3-vl-235b-a22b",
    "Qwen3-30B-A3B-2507": "tongyi-qwen3-30b-a3b-instruct-2507",
    "Qwen3-Coder-Flash": "tongyi-qwen3-coder-flash",
}


def parse_sse_data(sse_data):
    """
    解析SSE格式数据，提取JSON内容
    """
    messages = []
    sse = sse_data.strip().split('\n')
    for line in sse:
        line = re.findall("\{.*\}", line)
        if line:
            line = line[0]
        else:
            continue
        messages.append(json.loads(line))
    return messages


def extract_final_response(messages):
    """
    从解析后的消息中提取最终回复和相关信息
    """
    sessionId = ""
    parentMsgId = ""
    text = ""
    think = ""

    for msg in messages:
        # 提取最终文本回复
        if 'contents' in msg:
            msgList = msg.get("contents")
            for i in msgList:
                if i and type(i) is dict:
                    if i.get("contentType") == "think":
                        content = i.get("content", dict())
                        think += json.loads(content).get("content", "")
                    elif i.get("contentType") == "text":
                        text += i.get("content", "")
        if 'sessionId' in msg:
            sessionId = msg.get("sessionId")
        if 'parentMsgId' in msg:
            parentMsgId = msg.get("parentMsgId")

    return {
        'text': text,
        'think': think,
        'sessionId': sessionId,
        'parentMsgId': parentMsgId
    }


def qwen(cookies, msg, model="tongyi-qwen3-max-thinking", sessionId="", parentMsgId="", imgPath=""):
    x_deviceid = str(uuid.uuid4().hex)
    x_xsrf_token = str(uuid.uuid4())
    requestId = str(uuid.uuid4()).replace('-', '')

    json_data = {
        'sessionId': sessionId,
        'sessionType': 'text_chat',
        'parentMsgId': parentMsgId,
        'model': '',
        'mode': 'chat',
        'userAction': 'new_top',
        'actionSource': '',
        'contents': [
            {
                'content': msg,
                'contentType': 'text',
                'role': 'user',
                'ext': {
                    'deepThink': True,
                },
            },
        ],
        'action': 'next',
        'requestId': requestId,
        'params': {
            'deepThink': True,
            'specifiedModel': model,
            'lastUseModelList': [
                model,
            ],
            'recordModelName': model,
            'bizSceneInfo': {},
        },
    }
    if imgPath:
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://www.qianwen.com',
            'priority': 'u=1, i',
            'referer': 'https://www.qianwen.com/chat',
            'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'x-deviceid': x_deviceid,
            'x-platform': 'pc_tongyi',
            'x-xsrf-token': x_xsrf_token,
        }
        filename = os.path.basename(imgPath)
        response = curl_cffi.post('https://api.qianwen.com/dialog/uploadToken', cookies=cookies, headers=headers,
                                  json={'source': 'dialogue'}, impersonate="chrome124")
        Data = response.json()
        data = Data.get('data')
        OSSAccessKeyId = data.get('accessId')
        policy = data.get('policy')
        signature = data.get('signature')
        dir = data.get('dir')
        key = f"{dir}{filename}"
        files = {
            'OSSAccessKeyId': (None, OSSAccessKeyId),
            'policy': (None, policy),
            'signature': (None, signature),
            'key': (None, key),
            'dir': (None, dir),
            'success_action_status': (None, '200'),
            'file': (filename, open(imgPath, "rb"), magic.from_file(imgPath, mime=True)),
        }
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'Connection': 'keep-alive',
            'Origin': 'https://www.qianwen.com',
            'Referer': 'https://www.qianwen.com/chat',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        requests.post('https://tongyi-main.oss-accelerate.aliyuncs.com/', headers=headers, files=files)

        imgData = {
            'fileKey': filename,
            'fileType': 'image',
            'dir': dir,
            'source': 'dialogue',
        }
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://www.qianwen.com',
            'priority': 'u=1, i',
            'referer': 'https://www.qianwen.com/chat/1dd5c793985941c48d974152c1a02937',
            'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'x-deviceid': x_deviceid,
            'x-platform': 'pc_tongyi',
            'x-xsrf-token': x_xsrf_token,

        }
        response = curl_cffi.post('https://api.qianwen.com/dialog/downloadLink', cookies=cookies, headers=headers,
                                  json=imgData, impersonate="chrome124")
        urlLink = response.json().get('data').get('url')
        json_data.get('contents').append({
            'role': 'user',
            'contentType': 'image',
            'content': urlLink,
        })

    headers = {
        'accept': 'text/event-stream',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://www.qianwen.com',
        'priority': 'u=1, i',
        'referer': 'https://www.qianwen.com/chat',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'x-deviceid': x_deviceid,
        'x-platform': 'pc_tongyi',
        'x-xsrf-token': x_xsrf_token,
    }

    response = curl_cffi.post('https://api.qianwen.com/dialog/conversation', cookies=cookies, headers=headers,
                              json=json_data, impersonate="chrome124", timeout=120)

    data = parse_sse_data(response.text)
    result = extract_final_response(data)
    return result


if __name__ == '__main__':
    cookies = {
        # https://www.qianwen.com/ 网站下F12获取 https://api.qianwen.com/dialog/conversation 下的cookies
    }

    data = qwen(cookies, "我叫JB6")
    print(data)

    data = qwen(cookies, "我叫什么?", sessionId=data["sessionId"], parentMsgId=data["parentMsgId"])
    print(data)

    data = qwen(cookies, "提取文字", imgPath="abc.jpg")
    print(data)
