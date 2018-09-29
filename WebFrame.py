#coding=utf-8 
from views import *

#设置静态文件夹路径
STATIC_DIR = "./static"

#应用
class Application(object):
    def __init__(self,urls):
        self.urls = urls

    def __call__(self,env):
        method = env.get("METHOD",'GET')
        path = env.get("PATH_INFO",'/') #请求内容

        if method == 'GET':
            if path == '/' or path[-5:] == '.html':
                response = self.get_html(path)
            else:
                response = self.get_data(path)
        elif method == 'POST':
            pass

        return response

    def get_html(self,path):
        if path == '/':
            get_file = STATIC_DIR + "/index.html"
        else:
            get_file = STATIC_DIR + path
        try:
            fd = open(get_file)
        except IOError :
            #没有找到请求网页
            responseHeaders = "HTTP/1.1 404 not found\r\n"
            responseHeaders += '\r\n'
            response_body = "Sorry,the page not found"
        else:
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += '\r\n'
            response_body = fd.read()
        finally:
            response = responseHeaders + response_body
            return response

    def get_data(self,path):
        for url,handler in self.urls:
            if path == url:
                response_headers = "HTTP/1.1 200 OK\r\n"
                response_headers += '\r\n'
                response_body = handler()
                return response_headers + response_body 

        response_headers = "HTTP/1.1 404 not found\r\n"
        response_headers += '\r\n'
        response_body = "Sorry ,not found the data" 
        return response_headers + response_body

urls = [
    ('/time',show_time),
    ('/hello',say_hello),
    ('/bye',say_bye),
]

app = Application(urls)