import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Store():
    def __init__(self):
        self.__users = None
        self.__filesData = None
        
    def set_users(self, users):
        self.__users = users
        
    def get_user_list(self):
        return list(self.__users.keys())
    
    def get_repositores(self, user):
        return self.__users[user]
    
    def set_filesData(self, filesData):
        self.__filesData = filesData
        
    def get_fileData(self, filename):
        return self.__filesData[filename]