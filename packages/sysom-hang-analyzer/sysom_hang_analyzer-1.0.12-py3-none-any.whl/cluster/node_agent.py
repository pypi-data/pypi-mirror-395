# node_agent.py
import argparse
import json
import os
import sys
import time
import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import urllib.request
import urllib.parse
import subprocess

class NodeAgentServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.agent = kwargs.pop('agent', None)
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        if self.path == '/collect':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            collection_id = data.get('collection_id')
            if collection_id:
                # 异步执行采集
                threading.Thread(target=self.agent.collect_stacks, args=(collection_id,)).start()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'status': 'collecting', 'collection_id': collection_id}
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(400)
                self.end_headers()

class NodeAgent:
    def __init__(self, coordinator_host, coordinator_port, node_id=None, dump_path='/tmp/stack_data'):
        self.coordinator_host = coordinator_host
        self.coordinator_port = coordinator_port
        self.node_id = node_id or socket.gethostname()
        self.dump_path = Path(dump_path)
        self.dump_path.mkdir(parents=True, exist_ok=True)
        self.agent_port = None
        self.server = None
        
    def register_with_coordinator(self, agent_port):
        """向协调器注册"""
        try:
            url = f"http://{self.coordinator_host}:{self.coordinator_port}/register"
            data = json.dumps({
                'node_id': self.node_id,
                'port': agent_port
            }).encode()
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            response = urllib.request.urlopen(req, timeout=10)
            result = json.loads(response.read().decode())
            print(f"注册结果: {result}")
            return True
        except Exception as e:
            print(f"注册失败: {e}")
            return False
            
    def collect_stacks(self, collection_id):
        """采集堆栈数据"""
        print(f"开始采集堆栈数据，ID: {collection_id}")
        
        # 创建临时目录
        collect_dir = self.dump_path / f"collect_{collection_id}"
        collect_dir.mkdir(exist_ok=True)
        
        try:
            # 调用原有的采集脚本
            cmd = [
                "python3", "-m", "cluster.auto_stack_collector",
                "--dump-path", str(collect_dir),
                "--auto"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("堆栈采集完成")
                # 读取采集的数据并上传到协调器
                self.upload_stacks(collect_dir, collection_id)
            else:
                print(f"堆栈采集失败: {result.stderr}")
                
        except Exception as e:
            print(f"采集过程中出错: {e}")
        # finally:
        #     # 清理临时目录
        #     import shutil
        #     try:
        #         shutil.rmtree(collect_dir)
        #     except:
        #         pass
                
    # node_agent.py
    def upload_stacks(self, collect_dir, collection_id):
        """上传堆栈数据到协调器"""
        try:
            # 收集所有.stackdata文件
            stack_files = list(collect_dir.glob("*.stackdata"))
            
            # 逐个上传每个.stackdata文件
            for file_path in stack_files:
                try:
                    # 读取单个.stackdata文件
                    with open(file_path, 'r') as f:
                        stack_data = json.load(f)
                    
                    # 为每个文件创建独立的上传请求
                    url = f"http://{self.coordinator_host}:{self.coordinator_port}/upload"
                    upload_data = {
                        'node_id': self.node_id,
                        'collection_id': collection_id,
                        'file_name': file_path.name,  # 保留原始文件名
                        'stack_data': stack_data
                    }
                    
                    data = json.dumps(upload_data).encode()
                    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
                    response = urllib.request.urlopen(req, timeout=30)
                    result = json.loads(response.read().decode())
                    print(f"上传文件 {file_path.name} 结果: {result}")
                    
                except Exception as file_error:
                    print(f"上传文件 {file_path.name} 失败: {file_error}")
                    
        except Exception as e:
            print(f"上传数据失败: {e}")
            
    def start_server(self, port=0):
        """启动节点代理服务"""
        def handler_factory(*args, **kwargs):
            return NodeAgentServer(*args, agent=self, **kwargs)
            
        self.server = HTTPServer(('0.0.0.0', port), handler_factory)
        self.agent_port = self.server.server_port
        
        # 注册到协调器
        if self.register_with_coordinator(self.agent_port):
            print(f"节点代理服务启动在端口 {self.agent_port}")
            self.server.serve_forever()
        else:
            print("无法注册到协调器，服务启动失败")
            return False
            
        return True
        
    def stop_server(self):
        """停止节点代理服务"""
        if self.server:
            self.server.shutdown()

def main():
    parser = argparse.ArgumentParser(description="节点堆栈采集代理")
    parser.add_argument("--coordinator-host", 
                       default=os.environ.get("MASTER_ADDR"),
                       required=False,
                       help="协调器主机地址（默认使用 MASTER_ADDR 环境变量）")
    parser.add_argument("--coordinator-port", type=int, default=8080, help="协调器端口")
    parser.add_argument("--node-id", help="节点ID（默认使用主机名）")
    parser.add_argument("--dump-path", default="/tmp/stack_data", help="数据保存路径")
    parser.add_argument("--port", type=int, default=0, help="代理服务端口（0表示自动分配）")
    
    args = parser.parse_args()
    
    agent = NodeAgent(
        args.coordinator_host, 
        args.coordinator_port, 
        args.node_id, 
        args.dump_path
    )
    
    try:
        if agent.start_server(args.port):
            print("节点代理已启动")
        else:
            print("节点代理启动失败")
            sys.exit(1)  # 添加这行来返回错误码
    except KeyboardInterrupt:
        print("节点代理已停止")
        agent.stop_server()
    except Exception as e:
        print(f"节点代理启动异常: {e}")
        sys.exit(1)  # 添加异常处理时的错误码返回

if __name__ == "__main__":
    main()