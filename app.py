from flask import Flask, request, abort, current_app
from controllers.webhook_controller import webhook_blueprint
from controllers.test_controller import test_blueprint
from controllers.file_controller import file_blueprint

import configparser
import os
import sys

# 프로젝트 경로 설정
# /home/ubuntu/th/git_local
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)

# config.ini 로드
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"), encoding='utf-8')

app.config['GIT_TOKEN'] = config['CONFIG']['GIT_TOKEN']
app.config['MYSQL_USER'] = config['CONFIG']['MYSQL_USER']
app.config['MYSQL_PW']   = config['CONFIG']['MYSQL_PW']
app.config['MYSQL_DB']   = config['CONFIG']['MYSQL_DB']
app.config['GITHUB_SECRET'] = "0911" 

# # 블루프린트 등록
app.register_blueprint(webhook_blueprint, url_prefix="/")
app.register_blueprint(test_blueprint, url_prefix="/")
app.register_blueprint(file_blueprint, url_prefix="/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
