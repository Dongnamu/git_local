import base64
import json
import requests

def decode_files(blob):
    return base64.b64decode(blob).decode("utf-8")
def request_to_coder_model(prompt):
    URL = "http://125.7.137.190:8003/v2/models/coder-qwen-model/infer"
    
    messages = [
    {"role": "system", "content": "당신은 코드를 리뷰하는 리뷰어 역할입니다. 코드에 주석이 없을 경우, 몇번째 줄에 어떤 주석을 달아야 하는지 추천해야 하고, 코드 자체의 난이도와 완성도가 어떤지 리뷰하며, 필요한 경우 몇번째 줄의 코드를 수정해야하는지 추천해야 합니다. 주어지는 코드에 대해 주석을 달고, 리뷰하여, 필요한 경우 어떤 코드를 수정해야 하는지 한국말로 작성하세요."},
    {"role": "user", "content": prompt}
    ]
    
    # 요청 데이터 구성
    data = {
        "name": "summarization-model",
        "inputs": [
            {
                "name": "prompt",
                "shape": [len(messages)],
                "datatype": "BYTES",
                "data": [json.dumps(item) for item in messages]
            }
        ]
    }
    # JSON 데이터 직렬화 및 요청 전송
    json_str = json.dumps(data, ensure_ascii=False).encode('utf-8')
    res = requests.post(URL, data=json_str)
    
    return res.json()['outputs'][0]['data'][0]