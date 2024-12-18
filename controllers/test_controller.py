from flask import Blueprint, render_template
import os

# template 폴더 경로 설정    //  /views/templates 안에껄 보게됨 
test_blueprint = Blueprint('test', __name__, template_folder=os.path.join('..', 'views', 'templates'))

@test_blueprint.route("/test")
def test():
    return render_template('test.html')
