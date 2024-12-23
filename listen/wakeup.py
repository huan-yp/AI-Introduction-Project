from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/wake':
            self.send_response(200)  # 发送200状态码
            self.end_headers()
            print("Wake")
        else:
            self.send_response(404)  # 对于其他路径返回404状态码
            self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 3366)  # 监听所有来自本地网络接口的请求，端口为8000
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()