from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado
import tornado.httpclient
import json

class AIProxyHandler(APIHandler):
    
    @tornado.web.authenticated
    async def post(self):
        """Handle POST requests to the AI proxy endpoint"""
        backend_url = "http://localhost:8888/v1/chat/completions"
        
        try:
            # 创建HTTP客户端
            http_client = tornado.httpclient.AsyncHTTPClient()
            
            # 获取原始请求体
            request_body = self.request.body
            
            # 转发请求到后端
            request = tornado.httpclient.HTTPRequest(
                url=backend_url,
                method='POST',
                headers={
                    'Content-Type': 'application/json',
                },
                body=request_body,
                request_timeout=300  # 5分钟超时
            )
            
            # 发送请求
            response = await http_client.fetch(request)
            
            # 返回响应
            self.set_status(response.code)
            self.set_header('Content-Type', 'application/json')
            self.write(response.body)
            
        except tornado.httpclient.HTTPError as e:
            self.set_status(e.code)
            self.write(e.response.body if e.response else str(e))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({"error": str(e)}))
        finally:
            if 'http_client' in locals():
                http_client.close()

def setup_handlers(web_app):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    
    # 添加代理路由 - 使用更标准的路径
    route_pattern = url_path_join(base_url, "jupyterlab-chat", "api", "chat")
    handlers = [(route_pattern, AIProxyHandler)]
    web_app.add_handlers(host_pattern, handlers)