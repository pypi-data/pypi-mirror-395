import re
import uuid
import curl_cffi
import json_repair as json


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


def qwen(cookies, msg, model="tongyi-qwen3-max-thinking", sessionId="", parentMsgId=""):
    x_deviceid = str(uuid.uuid4())
    x_xsrf_token = str(uuid.uuid4())
    requestId = str(uuid.uuid4()).replace('-', '')
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
    response = curl_cffi.post('https://api.qianwen.com/dialog/conversation', cookies=cookies, headers=headers,
                              json=json_data, impersonate="chrome124")

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
