from flask import Blueprint, render_template, jsonify, current_app
import os

admin_blueprint = Blueprint('admin', __name__, template_folder=os.path.join('..','views','templates'))

@admin_blueprint.route('/admin')
def admin():
    users_data = [
    {
        "name": "Alice",
        "commit_count": 42,
        "repositories": [
            {"name": "ProjectA", "commit_count": 20},
            {"name": "ProjectB", "commit_count": 22}
        ]
    },
    {
        "name": "Bob",
        "commit_count": 35,
        "repositories": [
            {"name": "ProjectC", "commit_count": 15},
            {"name": "ProjectD", "commit_count": 20}
        ]
    },
    # 추가 사용자를 여기서 정의할 수 있습니다.
    ]
    
    return render_template('admin.html', users=users_data)
