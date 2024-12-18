from flask import Blueprint, render_template, jsonify
from services.file_service import get_tree_data, get_file_data, highlight_code
import os

file_blueprint = Blueprint('file', __name__, template_folder=os.path.join('..', 'views', 'templates'))

@file_blueprint.route('/')
def index():
    # 메인 페이지에서 폴더 및 파일 트리 표시
    # 모두 펼친 상태로 렌더링 (토글 없음)
    tree = get_tree_data()
    return render_template('index.html', tree=tree)

@file_blueprint.route('/file-data/<path:filename>')
def file_data(filename):
    data = get_file_data(filename)
    if data:
        code = data["code"]
        report = data["report"]
        return jsonify({
            "success": True,
            "code": code,
            "report": report,
        })
    else:
        return jsonify({
            "success": False,
            "code": "",
            "report": "해당 파일 정보가 없습니다.",
        })
