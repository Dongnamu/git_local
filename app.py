from flask import Flask, redirect, url_for
from controllers.webhook_controller import webhook_blueprint
from controllers.test_controller import test_blueprint
from controllers.report_controller import report_blueprint
from controllers.mainPage_controller import mainPage_blueprint
from controllers.admin_controller import admin_blueprint

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
app.register_blueprint(report_blueprint, url_prefix="/")
app.register_blueprint(mainPage_blueprint, url_prefix="/")
app.register_blueprint(admin_blueprint, url_prefix="/")

# 기본 경로에서 /test로 리디렉션
@app.route('/')
def home():
    return redirect(url_for('mainPage.mainPage')) 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
