import requests

class GitRetrieve:
    def __init__(self, owner, repo, branch, data, token):
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.data = data
        self.__headers = {
            "Authorization" : "Bearer {}".format(token)
        }
        
    def get_hierachy(self):
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/git/trees/{self.branch}?recursive=1"
        response = requests.get(url, headers=self.__headers)
        
        files = []
        
        if response.status_code == 200:
            tree = response.json()["tree"]
        else:
            return None
        
        for item in tree:
            name = item['path']
            if item['mode'] == "100644" or item["mode"] == "100755":
                file_info = requests.get(item['url'], headers=self.__headers).json()
                file_content = file_info['content']
                files.append((name, file_content))
                
        return files
    
    def get_diff(self):
        hash = self.data['after']
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/commits/{hash}"
        response = requests.get(url, headers=self.__headers)
        
        if response.status_code == 200:
            # print(response.json())
            diff = response.json()['files']
        else:
            diff = None
            
        return diff