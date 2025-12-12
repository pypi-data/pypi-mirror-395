# trigger_distributed_collection.py
import argparse
import urllib.request
import json
import os

def trigger_collection(coordinator_host, coordinator_port):
    """触发分布式采集"""
    try:
        url = f"http://{coordinator_host}:{coordinator_port}/trigger"
        req = urllib.request.Request(url, method='GET')
        response = urllib.request.urlopen(req, timeout=10)
        result = json.loads(response.read().decode())
        print(f"触发结果: {result}")
        return True
    except Exception as e:
        print(f"触发采集失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="触发分布式堆栈采集")
    parser.add_argument("--coordinator-host", 
                       default=os.environ.get("MASTER_ADDR"),
                       required=False,
                       help="协调器主机地址（默认使用 MASTER_ADDR 环境变量）")
    parser.add_argument("--coordinator-port", type=int, default=8080, help="协调器端口")
    
    args = parser.parse_args()
    
    if trigger_collection(args.coordinator_host, args.coordinator_port):
        print("分布式堆栈采集已触发")
    else:
        print("触发分布式堆栈采集失败")

if __name__ == "__main__":
    main()