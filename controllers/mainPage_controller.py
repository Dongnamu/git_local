from flask import Blueprint, render_template, jsonify, current_app
import os

mainPage_blueprint = Blueprint('mainPage', __name__, template_folder=os.path.join('..','views','templates'))

@mainPage_blueprint.route('/')
def mainPage():
    return render_template('startPage.html')