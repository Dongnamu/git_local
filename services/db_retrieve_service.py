from models.db_connect import DBConnect

def get_repository_names(config):
    db_connect = DBConnect(config['MYSQL_USER'], config['MYSQL_PW'], config['MYSQL_DB'])
    available_repositories = db_connect.get_repository_names()
    db_connect.close()
    return available_repositories

def get_files_from_db(config, user, repository):
    db_connect = DBConnect(config['MYSQL_USER'], config['MYSQL_PW'], config['MYSQL_DB'])
    repo_name = '{}/{}'.format(user, repository)
    repo_id = db_connect.get_repository_id(repo_name)
    files = db_connect.get_files(repo_id)
    db_connect.close()
    return files