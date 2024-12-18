from datetime import datetime
import json
from models.db_connect import DBConnect
from models.git_retrieve import GitRetrieve

def handle_github_event(data, event, config) :
    if event == "push" :
        user = data['repository']['owner']['login']
        name = data['repository']['name']
        branch = data['ref']
        
        db_connect = DBConnect(config['MYSQL_USER'], config['MYSQL_PW'], config['MYSQL_DB'])
        git = GitRetrieve(user, name, branch, data, config['GIT_TOKEN'])
    
        diff = git.get_diff()
        files = git.get_hierachy()
        
        git_id = None

        if diff is None:
            print("Error occurred while retrieving file difference from GitHub")
        else:
            before_hash = data['before']
            after_hash = data['after']
            commit_time = data['repository']['updated_at']
            dt = datetime.strptime(commit_time, "%Y-%m-%dT%H:%M:%SZ")

            diff_json = json.dumps(diff)
            git_id = db_connect.insert_repository(user, name, after_hash, before_hash, dt.strftime("%Y-%m-%d %H:%M:%S"), diff_json)

        if files is None:
            print("Error occurred while retrieving file hierarchy from GitHub")
        else:
            db_connect.insert_files(files, git_id)

        db_connect.close()
        return "Push event processed"
    elif event == "pull_request":
        git_head = GitRetrieve(data['repository']['owner']['login'], data['repository']['name'], data['pull_request']['head']['ref'], data, config['CONFIG']['GIT_TOKEN'])
        git_base = GitRetrieve(data['repository']['owner']['login'], data['repository']['name'], data['pull_request']['base']['ref'], data, config['CONFIG']['GIT_TOKEN'])
        # 필요하면 diff나 파일 처리를 추가
        return "Pull Request event processed (open)"
        
        
