from flask import Blueprint, render_template, jsonify, current_app
from services.db_retrieve_service import get_repository_names, get_files_from_db
from models.user_repository_store import Store
import os

report_blueprint = Blueprint('report', __name__, template_folder=os.path.join('..', 'views', 'templates'))
__store = Store()

def build_tree(file_paths):
    # 초기 트리 구조
    tree = {"folders": {}, "files": []}

    for path in file_paths:
        parts = path.split('/')
        node = tree
        # 마지막 요소는 파일명, 그 전까지는 폴더
        for folder in parts[:-1]:
            # 해당 폴더가 없으면 생성
            if folder not in node["folders"]:
                node["folders"][folder] = {"folders": {}, "files": []}
            node = node["folders"][folder]
        # 마지막 요소(파일명)를 files 리스트에 추가
        file_name = parts[-1]
        node["files"].append(file_name)

    return tree


@report_blueprint.route('/report')
def report():
    # 메인 페이지에서 폴더 및 파일 트리 표시
    # 모두 펼친 상태로 렌더링 (토글 없음)
    repositories = get_repository_names(current_app.config)
    users = {}
    
    for repository in repositories:
        user, name = repository.split('/')
        if user not in users:
            users[user] = [name]
        else:
            users[user].append(name)
            
    __store.set_users(users)
    return render_template('report.html', users=list(users.keys()))

@report_blueprint.route('/get-suboptions/<user>')
def get_suboptions(user):
    repos = __store.get_repositores(user)
    return jsonify(repos)

@report_blueprint.route('/get-tree/<user>/<repo>')
def get_tree(user, repo):
    files, filesData = get_files_from_db(current_app.config, user, repo)
    __store.set_filesData(filesData)
    tree = build_tree(files)
    return jsonify(tree)

@report_blueprint.route('/file-data/<user>/<repo>/<path:filename>')
def get_file_data(user, repo, filename):
    code_report = __store.get_fileData(filename)
    if code_report:
        code_report['success'] = True
        return jsonify(code_report)
    else:
        return jsonify({
            "success": False,
            "code" : "",
            "report" : "해당 파일 정보가 없습니다."
        })