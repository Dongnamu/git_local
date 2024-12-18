from flask import Flask, request, abort, render_template
import hmac
import hashlib
import sys
import os
from datetime import datetime
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library.git_retrieve import GitRetrieve
from library.db_connection import DBConnect
import configparser

config = configparser.ConfigParser()

config.read('/home/ubuntu/th/git_local/config.ini', encoding='utf-8')
print(config['CONFIG'])
app = Flask(__name__)

# GitHub Webhook Secret (GitHub 웹훅 설정 시 사용한 비밀 키)
GITHUB_SECRET = "0911"

@app.route("/test")
def test():
    return render_template('test.html')

@app.route("/webhook", methods=["POST"])
def github_webhook():
    # GitHub 웹훅 서명 헤더
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        abort(400, "Signature missing")
    # 요청 본문 검증
    payload = request.data
    calculated_signature = "sha256=" + hmac.new(
        GITHUB_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(calculated_signature, signature):
        abort(400, "Invalid signature")

    # 이벤트 타입 확인
    event = request.headers.get("X-GitHub-Event", "ping")
    if event == "ping":
        return {"msg": "pong"}
    elif event == "push" or event == "pull_request":
        data = request.json
        if event == "push":
            user = data['repository']['owner']['login']
            name = data['repository']['name']
            branch = data['ref']
            db_connect = DBConnect(config['CONFIG']['MYSQL_USER'], config['CONFIG']['MYSQL_PW'], config['CONFIG']['MYSQL_DB'])
            git = GitRetrieve(user, name, branch, data, config['CONFIG']['GIT_TOKEN'])
            
            diff = git.get_diff()
            files = git.get_hierachy()
            
            git_id = None
            
            if diff is None:
                print("Error occured while retrieving file difference from github")
            else:
                before_hash = data['before']
                after_hash = data['after']
                
                commit_time = data['repository']['updated_at']
                
                dt = datetime.strptime(commit_time, "%Y-%m-%dT%H:%M:%SZ")
                
                diff_json = json.dumps(diff)
                # print(user, name, after_hash, before_hash, dt.strftime("%Y-%m-%d %H:%M:%S"))
                git_id = db_connect.insert_repository(user, name, after_hash, before_hash, dt.strftime("%Y-%m-%d %H:%M:%S"), diff_json)
            
            if files is None:
                print("Error occured while retrieving file hierachy from github")
            else:
                db_connect.insert_files(files, git_id)
            
            db_connect.close()
                
        elif data['pull_request']['state'] == 'open':
            git_head = GitRetrieve(data['repository']['owner']['login'], data['repository']['name'], data['pull_request']['head']['ref'], data, config['CONFIG']['GIT_TOKEN'])
            git_base = GitRetrieve(data['repository']['owner']['login'], data['repository']['name'], data['pull_request']['base']['ref'], data, config['CONFIG']['GIT_TOKEN'])
        
        
        
        
        # print(data)
            
        
    else:
        print(f"Unhandled event: {event}")

    return {"msg": "Event received"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)