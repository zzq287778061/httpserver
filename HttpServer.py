#coding=utf-8

'''
name : Levi
time : 2018-8-28
功能 ：httpserver部分
'''
from socket import  *
import sys 
from threading import Thread
import re
from setting import * 

#处理http请求类
class HTTPServer(object):
    def __init__(self,application):
        self.sockfd = socket()
        self.sockfd.setsockopt\
        (SOL_SOCKET,SO_REUSEADDR,1)
        #获取模块接口
        self.application = application

    def bind(self,host,port):
        self.host = host
        self.port = port 
        self.sockfd.bind((self.host,self.port))
    #启动服务器
    def serve_forever(self):
        self.sockfd.listen(10)
        print("Listen the port %d..."%self.port)
        while True:
            connfd,addr = self.sockfd.accept()
            print("Connect from",addr)
            handle_client = Thread\
            (target = self.client_handler,\
                args = (connfd,))
            handle_client.setDaemon(True)
            handle_client.start()

    def client_handler(self,connfd):
        #接收浏览器request
        request = connfd.recv(4096)
        #可以分析请求头和请求体
        request_lines = request.splitlines()
        #获取请求行
        request_line = request_lines[0].decode('utf-8')
        
        #获取请求方法和请求内容
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH_INFO>/\S*)'
        try:
            env = re.match(pattern,request_line).groupdict()
        except:
            response_headlers =  "HTTP/1.1 500 SERVER ERROR\r\n"
            response_headlers += "\r\n"
            response_body = "server error"
            response = response_headlers + response_body
            connfd.send(response.encode())

        # method,filename = \
        # re.findall(r'^([A-Z]+)\s+(/\S*)',\
        #     request_line)[0]
        #将解析内容合成字典给web frame使用
        # env = {'METHOD':method,'PATH_INFO':filename}
        # print(env)

        #将env给Frame处理,得到返回内容
        response = self.application(env)

        #发送给客户端
        if response:
            connfd.send(response.encode())
            connfd.close()


if __name__ == "__main__":
    #将要使用的模块导入进来
    sys.path.insert(1,MODULE_PATH)
    m = __import__(MODULE)
    application = getattr(m,APP)

    httpd = HTTPServer(application)
    httpd.bind(HOST,PORT)
    httpd.serve_forever()
