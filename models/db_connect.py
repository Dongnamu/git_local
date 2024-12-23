import json
import pymysql
from services.utilities import decode_files, request_to_model
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound

class DBConnect:
    def __init__(self, user, passwd, db, host='localhost', port=3306):
        self.user = user
        self.passwd = passwd
        self.db = db
        self.host = host
        self.port = port
        self.__conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8mb4')
        self.__cursor = self.__conn.cursor(pymysql.cursors.DictCursor)
    
    def insert_repository(self, user, name, hash, parent_hash, commit_time, log):
        parent_id = None
        
        repository = f'{user}/{name}'
        
        # check if repository and hash already exists in database
        query = f"SELECT id as id, COUNT(*) as count FROM git_repository WHERE name = %s AND hash = %s"
        self.__cursor.execute(query, (repository, hash))
        result = self.__cursor.fetchone()
        if result['count'] > 0:
            print("Repository already exist in database. Skipping insert")
            return result['id']
        else:
            # if just created (either new repository or new branch)
            if parent_hash != "0000000000000000000000000000000000000000":
                parent_id = None
                query = "SELECT id FROM git_repository WHERE name = %s AND hash = %s;"
                self.__cursor.execute(query, (repository, parent_hash))
                result = self.__cursor.fetchone()
                
                if result is not None:
                    parent_id = result['id']
                
            query = "INSERT INTO git_repository(name, hash, parent_id, log, commit_time) VALUES(%s, %s, %s, %s, %s)"
            self.__cursor.execute(query, (repository, hash, parent_id, log, commit_time))
            id = self.__cursor.lastrowid
            self.__conn.commit()
            print("Repository Successfully inserted")
            return id
    
    def insert_files(self, files, git_id):
        for name, content in files:
            query = 'select id from content_cache where content = %s'
            self.__cursor.execute(query, (content))
            result = self.__cursor.fetchone()
            
            if result is not None:
                content_id = result['id']
                print("fetched file id from table")
            else:
                print(name)
                report, code_review = request_to_model('gpt', name, decode_files(content))
                query = 'insert into content_cache(content, report, code_review) values(%s, %s, %s)'
                self.__cursor.execute(query, (content, report, code_review))
                content_id = self.__cursor.lastrowid
                self.__conn.commit()
                print("file added to database")
            # check if file with same name, content and git_id exists
            query = 'select id from files where name = %s and content_id = %s and git_id = %s'
            self.__cursor.execute(query, (name, content_id, git_id))
            result = self.__cursor.fetchone()
            
            if result is not None:
                print("File information with corresponding git id is already saved. Skipping file information insertion")
            else:
                query = 'insert into files(name, content_id, git_id) values(%s, %s, %s)'
                self.__cursor.execute(query, (name, content_id, git_id))
                self.__conn.commit()
                
    def get_repository_names(self):
        query = 'select distinct name from git_repository'
        self.__cursor.execute(query)
        results = self.__cursor.fetchall()
        names = [result['name'] for result in results]            
        return names
    
    def get_repository_id(self, repo_name):
        query = 'select id from git_repository where name = %s order by id desc limit 1'
        self.__cursor.execute(query, (repo_name))
        result = self.__cursor.fetchone()
        return result['id']
    
    def get_files(self, repo_id):
        query = 'select name, content_id from files where git_id = %s'
        self.__cursor.execute(query, (repo_id))
        results = self.__cursor.fetchall()
        
        files = []
        filesData = {}
        
        for result in results:
            query = 'select content, report, code_review from content_cache where id=%s'
            self.__cursor.execute(query, result['content_id'])
            file_result = self.__cursor.fetchone()
            files.append(result['name'])
            code = decode_files(file_result['content'])
            
            try:
                lexer = guess_lexer_for_filename(result['name'], code)
                language = lexer.name
            except ClassNotFound:
                language = "plaintext"
                
            # filesData[result['name']] = {'code':code, "report":file_result['report'], "code_review":file_result['code_review']}
            filesData[result['name']] = {'code':code, "report":file_result['report'], "code_review":file_result['code_review'], "language":language}
            
        return files, filesData
            
                    
    def close(self):
        self.__cursor.close()
        self.__conn.close()