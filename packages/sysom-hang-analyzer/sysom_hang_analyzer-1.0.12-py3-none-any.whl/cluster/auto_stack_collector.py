# auto_stack_collector.py
import argparse
import json
import os
import subprocess
import sys
import time
import re
import shutil
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
from typing import Dict, Set, Tuple
from tqdm import tqdm


def parallel_job(fn, items, desc, concurrency=32):
    """并行执行任务"""
    SLEEP = 0.2
    futures: Set = set()
    items: Set = set(items)
    objs = []
    with ProcessPoolExecutor(max_workers=concurrency) as e:
        with tqdm(total=len(items), desc=desc) as bar:
            while futures or items:
                done = set()
                added = set()
                for item in items:
                    futures.add(e.submit(fn, item))
                    added.add(item)
                    if len(futures) > concurrency:
                        break
                for future in futures:
                    if future.done():
                        obj = future.result()
                        objs.append(obj)
                        done.add(future)
                        bar.update(1)
                futures -= done
                items -= added
                time.sleep(SLEEP)
    return objs


def parse_main_task_sched_file(proc_path: Path) -> Tuple[str, str]:
    """解析主任务调度文件，获取宿主机PID到容器PID的映射"""
    try:
        container_pid = proc_path.name
        main_task_path = proc_path / "task" / container_pid
        sched_file = main_task_path / "sched"
        
        if not sched_file.exists():
            return ("", "")
        
        # 读取sched文件查找PID信息
        with open(sched_file, 'r') as f:
            first_line = f.readline().strip()
            # 格式: python3.11 (2283091, #threads: 22)
            match = re.search(r'\((\d+),', first_line)
            if match:
                host_pid = match.group(1)
                return (host_pid, container_pid)
    except Exception:
        pass
    return ("", "")


def parse_main_task_status_file(proc_path: Path) -> Tuple[str, str]:
    """解析主任务状态文件，获取宿主机PID到容器PID的映射"""
    try:
        container_pid = proc_path.name
        main_task_path = proc_path / "task" / container_pid
        status_file = main_task_path / "status"
        
        if not status_file.exists():
            return ("", "")
        
        # 读取status文件查找Ngid行
        with open(status_file, 'r') as f:
            for line in f:
                if line.startswith('Ngid:'):
                    # Ngid: 2283091 (宿主机PID)
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        host_pid = parts[1]
                        return (host_pid, container_pid)
                elif line.startswith('NSpid:'):
                    # NSpid: 12345 678 (宿主机PID, 容器PID)
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        host_pid = parts[1]  # 第二个是宿主机PID
                        container_pid = parts[2]  # 第三个是容器PID
                        return (host_pid, container_pid)
    except Exception:
        pass
    return ("", "")


def parse_one_process_tasks(proc_path: Path) -> Dict[str, str]:
    """解析单个进程的主任务，获取PID映射"""
    try:
        # # 只关注主任务（task目录下与进程PID同名的目录）
        # host_pid, container_pid = parse_main_task_status_file(proc_path)
        
        # if not host_pid:
        # 如果status文件没有Ngid或NSpid，尝试sched文件
        host_pid, container_pid = parse_main_task_sched_file(proc_path)
        
        if host_pid and container_pid:
            return {host_pid: container_pid}
                
    except Exception:
        pass
    return {}


def build_pid_mapping() -> Dict[str, str]:
    """构建宿主机PID到容器PID的映射表"""
    proc_path = Path("/proc")
    pid_dir_pattern = re.compile(r"^\d+$")
    
    # 获取所有进程目录
    pid_dirs = [p for p in proc_path.iterdir() if p.is_dir() and pid_dir_pattern.match(p.name)]
    
    # 并行解析所有进程的主任务目录
    pid_mappings = parallel_job(parse_one_process_tasks, tuple(pid_dirs), "Parsing PID mappings", concurrency=16)
    
    # 构建映射字典
    pid_host_to_container = {}
    for mapping in pid_mappings:
        pid_host_to_container.update(mapping)
    
    return pid_host_to_container


def find_gpu_processes() -> list:
    """查找GPU进程的宿主机PID"""
    try:
        # 使用nvidia-smi获取GPU进程的宿主机PID
        nvidia_smi = ["nvidia-smi", "--query-compute-apps=pid", "--format=csv,noheader,nounits"]
        process = subprocess.Popen(nvidia_smi, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            gpu_pids = [pid.strip() for pid in stdout.splitlines() if pid.strip().isdigit()]
            return gpu_pids
    except Exception as e:
        print(f"执行nvidia-smi时出错: {e}", file=sys.stderr)
    return []


def convert_host_pids_to_container_pids(host_pids: list) -> list:
    """将宿主机PID转换为容器PID"""
    # 构建PID映射表
    print("正在构建PID映射表...")
    pid_mapping = build_pid_mapping()
    
    if not pid_mapping:
        print("未能构建PID映射表，将直接使用宿主机PID", file=sys.stderr)
        return [int(pid) for pid in host_pids]
    
    # 转换PID
    container_pids = []
    for host_pid in host_pids:
        if host_pid in pid_mapping:
            container_pids.append(int(pid_mapping[host_pid]))
        else:
            # 如果没有映射关系，可能是宿主机进程，直接使用
            print(f"警告: PID {host_pid} 没有找到容器映射，使用宿主机PID", file=sys.stderr)
            container_pids.append(int(host_pid))
    
    return container_pids


def get_process_env(pid):
    """获取进程环境变量"""
    try:
        with open(f"/proc/{pid}/environ", "r") as f:
            env_data = f.read()
            env_vars = {}
            for item in env_data.split('\0'):
                if '=' in item:
                    k, v = item.split('=', 1)
                    env_vars[k] = v
            return env_vars
    except Exception:
        return {}


def get_process_state(pid):
    """获取进程状态"""
    try:
        with open(f"/proc/{pid}/status", "r") as f:
            for line in f:
                if line.startswith("State:"):
                    return line.split(":", 1)[1].strip()
        return "Unknown"
    except Exception:
        return "Unknown"


def collect_python_stack(pid, dump_path, rank=None):
    """使用py-spy收集Python堆栈（包括native堆栈）"""
    try:
        # 使用 -n 参数同时收集native堆栈
        cmd = ["py-spy", "dump", "-j", "-n", "-p", str(pid)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            stack_data = json.loads(result.stdout)
            return stack_data
        else:
            print(f"收集进程 {pid} 的堆栈失败: {result.stderr}", file=sys.stderr)
            return []
    except subprocess.TimeoutExpired:
        print(f"收集进程 {pid} 的堆栈超时", file=sys.stderr)
        return None
    except Exception as e:
        print(f"收集进程 {pid} 的堆栈时出错: {e}", file=sys.stderr)
        return None


def process_single_process(pid, dump_path, world_size=None):
    """处理单个进程"""
    print(f"正在处理进程 {pid}...")
    
    # 检查进程是否存在
    if not os.path.exists(f"/proc/{pid}"):
        print(f"进程 {pid} 不存在", file=sys.stderr)
        return False
    
    # 获取进程环境变量
    env_vars = get_process_env(pid)
    
    # 获取RANK和WORLD_SIZE
    rank = env_vars.get('RANK')
    if rank is not None:
        rank = int(rank)
    else:
        rank = 0  # 默认值
    
    if world_size is None:
        world_size_env = env_vars.get('WORLD_SIZE')
        if world_size_env is not None:
            world_size = int(world_size_env)
        else:
            world_size = 1  # 默认值
    
    # 获取进程状态
    state = get_process_state(pid)
    
    # 收集堆栈（包括Python和native）
    stack_data = collect_python_stack(pid, dump_path, rank)
    
    # 保存数据
    data = {
        'pid': pid,
        'rank': rank,
        'world_size': world_size,
        'process_state': state,
        'stack_data': stack_data  # 包含了Python和native堆栈
    }
    
    filename = f"{str(rank).zfill(5)}-{str(world_size).zfill(5)}.stackdata"
    filepath = os.path.join(dump_path, filename)
    
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"进程 {pid} (rank {rank}) 的数据已保存到 {filepath}")
        return True
    except Exception as e:
        print(f"保存进程 {pid} 的数据时出错: {e}", file=sys.stderr)
        return False


def run_auto_detect_mode(dump_path):
    """自动检测模式：查找GPU进程并收集堆栈"""
    print("正在自动检测GPU进程...")
    
    # 1. 获取GPU进程的宿主机PID
    print("正在获取GPU进程列表...")
    host_pids = find_gpu_processes()
    
    if not host_pids:
        print("未找到GPU进程", file=sys.stderr)
        return False
    
    print(f"找到 {len(host_pids)} 个GPU进程 (宿主机PID): {host_pids}")
    
    # 2. 将宿主机PID转换为容器PID
    print("正在转换PID...")
    container_pids = convert_host_pids_to_container_pids(host_pids)
    
    print(f"转换后的容器PID: {container_pids}")
    
    # 3. 并行处理所有GPU进程
    success_count = 0
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(process_single_process, pid, dump_path)
            for pid in container_pids
        ]
        
        for future in futures:
            if future.result():
                success_count += 1
    
    print(f"成功处理 {success_count}/{len(container_pids)} 个GPU进程")
    return success_count > 0


def run_manual_mode(base_pid, world_size, dump_path):
    """手动模式：根据指定的PID范围收集堆栈"""
    print(f"手动模式: 处理 {world_size} 个进程，起始PID为 {base_pid}")
    
    # 生成进程PID列表
    pids = list(range(base_pid, base_pid + world_size))
    
    print(f"将处理 {world_size} 个进程: {pids}")
    
    # 并行处理所有进程
    success_count = 0
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(process_single_process, pid, dump_path, world_size)
            for pid in pids
        ]
        
        for future in futures:
            if future.result():
                success_count += 1
    
    print(f"成功处理 {success_count}/{len(pids)} 个进程")
    return success_count > 0


def main():
    parser = argparse.ArgumentParser(description="自动收集GPU进程的堆栈信息")
    parser.add_argument("--dump-path", type=str, required=True, help="指定dump路径")
    parser.add_argument("--pid", type=int, default=-1, help="第一个rank进程的PID（手动模式）")
    parser.add_argument("--world-size", type=int, default=8, help="世界大小（进程数），默认为8")
    parser.add_argument("--auto", action="store_true", help="自动检测GPU进程模式")
    
    args = parser.parse_args()
    
    # 创建dump目录
    dump_path = Path(args.dump_path)
    dump_path.mkdir(parents=True, exist_ok=True)
    
    # 检查必要的工具是否存在
    required_tools = ['py-spy']
    missing_tools = []
    for tool in required_tools:
        if not shutil.which(tool):
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"警告: 以下工具未找到: {', '.join(missing_tools)}", file=sys.stderr)
        print("请确保已安装这些工具以获得完整的堆栈信息", file=sys.stderr)
    
    success = False
    if args.auto or args.pid == -1:
        # 自动检测模式
        success = run_auto_detect_mode(str(dump_path))
    else:
        # 手动模式
        success = run_manual_mode(args.pid, args.world_size, str(dump_path))
    
    if success:
        print(f"堆栈数据已保存到目录: {dump_path}")
        return 0
    else:
        print("未能成功收集任何进程的堆栈信息", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())