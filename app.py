import logging
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from config import SERVICE_CONFIG
from handlers import TextServiceHandler, MultimodalServiceHandler, HealthCheckHandler

# 定义命令行参数
define("port", default=SERVICE_CONFIG['port'], help="run on the given port", type=int)
define("host", default=SERVICE_CONFIG['host'], help="run on the given host")
define("debug", default=SERVICE_CONFIG['debug'], help="run in debug mode", type=bool)

class Application(tornado.web.Application):
    """主应用类"""
    
    def __init__(self):
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # 定义路由
        handlers = [
            (r"/api/text", TextServiceHandler),
            (r"/api/multimodal", MultimodalServiceHandler),
            (r"/health", HealthCheckHandler),
        ]
        
        # 应用设置
        settings = {
            "debug": options.debug,
            "max_buffer_size": SERVICE_CONFIG['max_buffer_size'],
            "max_body_size": SERVICE_CONFIG['max_body_size'],
        }
        
        super().__init__(handlers, **settings)

def main():
    """主函数"""
    # 解析命令行参数
    tornado.options.parse_command_line()
    
    # 创建应用
    app = Application()
    
    # 启动服务器
    app.listen(options.port, options.host)
    
    logging.info(f"Server started on {options.host}:{options.port}")
    logging.info("Available endpoints:")
    logging.info("  POST /api/text - Text processing services")
    logging.info("  POST /api/multimodal - Multimodal processing services")
    logging.info("  GET /health - Health check")
    
    # 启动事件循环
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main() 