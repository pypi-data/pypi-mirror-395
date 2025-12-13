"""
游戏服务器模块
启动本地HTTP服务器来运行贪吃蛇游戏
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path


def main():
    """命令行入口点"""
    start_game()


def start_game(port=8000, open_browser=True):
    """
    启动贪吃蛇游戏服务器
    
    Args:
        port (int): 服务器端口，默认8000
        open_browser (bool): 是否自动打开浏览器，默认True
    """
    # 获取静态文件目录
    static_dir = Path(__file__).parent / 'static'
    
    # 切换到静态文件目录
    os.chdir(static_dir)
    
    # 创建HTTP服务器
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            url = f"http://localhost:{port}"
            print(f"🐍 贪吃蛇游戏服务器已启动!")
            print(f"📍 访问地址: {url}")
            print(f"按 Ctrl+C 停止服务器\n")
            
            if open_browser:
                webbrowser.open(url)
            
            httpd.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ 端口 {port} 已被占用，请尝试其他端口")
            print(f"💡 提示: 可以指定其他端口，例如 start_game(port=8001)")
        else:
            raise
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")


if __name__ == "__main__":
    start_game()

