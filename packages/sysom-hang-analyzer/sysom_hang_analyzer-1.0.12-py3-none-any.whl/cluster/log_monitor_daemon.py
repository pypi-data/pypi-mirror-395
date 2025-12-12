import argparse
import os
import time
from datetime import datetime, timedelta
import urllib.request
import json
import logging
import sys
import subprocess

# 配置日志
def setup_logging(log_file='/tmp/stack_log_monitor.log', daemon_mode=False):
    """设置日志配置"""
    # 清除现有的处理器
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        
    if daemon_mode:
        # 守护进程模式下只写入文件
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file)
            ],
            force=True
        )
    else:
        # 前台模式下同时输出到文件和控制台
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ],
            force=True
        )
    return logging.getLogger(__name__)

def check_log_activity(log_files, threshold_minutes=5, logger=None):
    """
    检查日志文件是否在指定时间内有活动
    
    Args:
        log_files: 日志文件路径列表
        threshold_minutes: 阈值时间(分钟)，默认5分钟
        logger: 日志记录器
    
    Returns:
        bool: 如果所有文件都超过阈值时间未更新返回True，否则返回False
    """
    threshold = timedelta(minutes=threshold_minutes)
    current_time = datetime.now()
    
    for log_file in log_files:
        if not os.path.exists(log_file):
            if logger:
                logger.warning(f"日志文件不存在: {log_file}")
            continue
            
        # 获取文件最后修改时间
        mtime = datetime.fromtimestamp(os.path.getmtime(log_file))
        time_diff = current_time - mtime
        
        if logger:
            logger.debug(f"{log_file} 最后更新时间: {mtime}, 距离现在: {time_diff}")
        
        # 如果有任何一个文件在阈值时间内有更新，则不触发
        if time_diff < threshold:
            if logger:
                logger.info(f"文件 {log_file} 在 {threshold_minutes} 分钟内有更新，不触发采集")
            return False
    
    # 所有文件都超过阈值时间未更新
    if logger:
        logger.info(f"所有文件超过 {threshold_minutes} 分钟未更新，准备触发采集")
    return True

def trigger_collection(coordinator_host, coordinator_port, logger=None):
    """触发分布式采集"""
    try:
        url = f"http://{coordinator_host}:{coordinator_port}/trigger"
        if logger:
            logger.info(f"正在触发采集: {url}")
        req = urllib.request.Request(url, method='GET')
        response = urllib.request.urlopen(req, timeout=10)
        result = json.loads(response.read().decode())
        if logger:
            logger.info(f"触发结果: {result}")
        return True
    except Exception as e:
        if logger:
            logger.error(f"触发采集失败: {e}")
        return False

def has_new_collection_data(analysis_base_path, last_analysis_time, logger=None):
    """
    检查是否有新的采集数据
    
    Args:
        analysis_base_path: 分析基础路径
        last_analysis_time: 上次分析时间戳
        logger: 日志记录器
        
    Returns:
        bool: 如果有新的采集数据返回True，否则返回False
    """
    if not os.path.exists(analysis_base_path):
        return False
    
    # 检查分析基础路径下的最新修改时间
    try:
        latest_mtime = 0
        for root, dirs, files in os.walk(analysis_base_path):
            for file in files:
                filepath = os.path.join(root, file)
                mtime = os.path.getmtime(filepath)
                if mtime > latest_mtime:
                    latest_mtime = mtime
                    
        # 如果最新的文件修改时间晚于上次分析时间，则有新数据
        has_new_data = latest_mtime > last_analysis_time
        if logger:
            if has_new_data:
                logger.info(f"发现新的采集数据 (最新数据时间: {datetime.fromtimestamp(latest_mtime)}, 上次分析时间: {datetime.fromtimestamp(last_analysis_time)})")
            else:
                logger.info("没有发现新的采集数据")
        return has_new_data
    except Exception as e:
        if logger:
            logger.error(f"检查新采集数据时出错: {e}")
        return False

def perform_analysis(analysis_base_path="/tmp/stack_analysis", last_analysis_time=0, logger=None):
    """
    执行自动分析
    
    Args:
        analysis_base_path: 分析基础路径
        last_analysis_time: 上次分析时间戳
        logger: 日志记录器
    """
    try:
        # 首先检查是否有新的采集数据
        if not has_new_collection_data(analysis_base_path, last_analysis_time, logger):
            if logger:
                logger.info("没有新的采集数据，跳过分析")
            return True
            
        if logger:
            logger.info("开始执行自动分析...")
        
        # 构建命令，确保在正确的目录下执行
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        cmd = [
            "python3", "sysom_hang_analyzer.py",
            "aggregate",
            "/tmp/stack_data_all",
            analysis_base_path
        ]
        
        if logger:
            logger.info(f"执行分析命令: {' '.join(cmd)}")
        
        # 在正确的目录下执行命令
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=current_dir)
        
        if result.returncode == 0:
            if logger:
                logger.info("自动分析完成")
            return True
        else:
            if logger:
                logger.error(f"自动分析失败: {result.stderr}")
            return False
            
    except Exception as e:
        if logger:
            logger.error(f"执行自动分析时出错: {e}")
        return False

def monitor_logs_and_trigger(coordinator_host, coordinator_port, 
                           log_files, check_interval=60, threshold_minutes=5,
                           logger=None, trigger_mode="continuous", 
                           analysis_base_path="/tmp/stack_analysis"):
    """
    监控日志文件并自动触发采集和分析
    
    Args:
        coordinator_host: 协调器主机地址
        coordinator_port: 协调器端口
        log_files: 要监控的日志文件列表
        check_interval: 检查间隔(秒)，默认60秒
        threshold_minutes: 触发阈值(分钟)，默认5分钟
        logger: 日志记录器
        trigger_mode: 触发模式 ("continuous"=持续触发, "once"=只触发一次)
        analysis_base_path: 分析结果基础路径
    """
    if logger:
        logger.info(f"开始监控日志文件: {log_files}")
        logger.info(f"检查间隔: {check_interval}秒, 触发阈值: {threshold_minutes}分钟")
        logger.info(f"协调器地址: {coordinator_host}:{coordinator_port}")
        logger.info(f"触发模式: {'只触发一次' if trigger_mode == 'once' else '持续触发'}")
        logger.info(f"分析结果保存路径: {analysis_base_path}")
    
    has_triggered = False
    last_trigger_time = 0
    last_analysis_time = 0  # 记录上次分析时间
    cooldown_period = threshold_minutes * 60  # 冷却时间等于阈值时间
    
    while True:
        try:
            current_time = time.time()
            
            # 检查是否处于冷却期
            if current_time - last_trigger_time < cooldown_period:
                if logger:
                    remaining_cooldown = cooldown_period - (current_time - last_trigger_time)
                    logger.debug(f"处于冷却期，剩余 {remaining_cooldown:.0f} 秒")
                time.sleep(min(check_interval, remaining_cooldown))
                continue
                
            if check_log_activity(log_files, threshold_minutes, logger):
                if logger:
                    logger.info("检测到日志长时间未更新，检查是否触发采集...")
                
                # 如果是只触发一次模式，且已经触发过，则跳过
                if trigger_mode == "once" and has_triggered:
                    if logger:
                        logger.info("已触发过采集，跳过本次触发（只触发一次模式）")
                else:
                    if logger:
                        logger.info("触发分布式采集...")
                    if trigger_collection(coordinator_host, coordinator_port, logger):
                        if logger:
                            logger.info("分布式堆栈采集已触发")
                        
                        # 等待一段时间让采集完成
                        if logger:
                            logger.info("等待采集完成...")
                        time.sleep(10)
                        
                        # 执行自动分析
                        if perform_analysis(analysis_base_path, last_analysis_time, logger):
                            if logger:
                                logger.info("自动分析完成")
                            last_analysis_time = time.time()  # 更新分析时间
                        else:
                            if logger:
                                logger.error("自动分析失败")
                        
                        last_trigger_time = time.time()  # 更新最后触发时间
                        has_triggered = True
                        
                        # 如果是只触发一次模式，触发后退出
                        if trigger_mode == "once":
                            if logger:
                                logger.info("只触发一次模式下程序退出")
                            return True
                    else:
                        if logger:
                            logger.error("触发分布式堆栈采集失败")
            else:
                if logger:
                    logger.info("日志文件近期有活动，继续监控...")
                
        except KeyboardInterrupt:
            if logger:
                logger.info("收到中断信号，监控已停止")
            break
        except Exception as e:
            if logger:
                logger.error(f"监控过程中发生错误: {e}")
            
        # 等待下次检查
        time.sleep(check_interval)
    
    return True

def daemonize():
    """将进程转为守护进程"""
    try:
        pid = os.fork()
        if pid > 0:
            # 父进程退出
            sys.exit(0)
    except OSError as e:
        print(f"fork失败: {e}")
        sys.exit(1)
    
    # 修改子进程环境
    os.chdir("/")
    os.setsid()
    os.umask(0)
    
    # 第二次fork
    try:
        pid = os.fork()
        if pid > 0:
            # 第二个父进程退出
            sys.exit(0)
    except OSError as e:
        print(f"第二次fork失败: {e}")
        sys.exit(1)
    
    # 重定向标准输入、输出、错误
    sys.stdin.flush()
    sys.stdout.flush()
    sys.stderr.flush()
    
    with open('/dev/null', 'r') as dev_null_r:
        os.dup2(dev_null_r.fileno(), sys.stdin.fileno())
    
    with open('/tmp/stack_log_monitor.log', 'a') as log_file:
        os.dup2(log_file.fileno(), sys.stdout.fileno())
        os.dup2(log_file.fileno(), sys.stderr.fileno())

def main():
    parser = argparse.ArgumentParser(description="监控日志文件变化并自动触发分布式堆栈采集和分析")
    parser.add_argument("--coordinator-host", 
                       default=os.environ.get("MASTER_ADDR"),
                       required=False,
                       help="协调器主机地址（默认使用 MASTER_ADDR 环境变量）")
    parser.add_argument("--coordinator-port", type=int, default=8080, help="协调器端口")
    parser.add_argument("--log-files", nargs='+', 
                       default=["/out.log", "/err.log"],
                       help="要监控的日志文件路径（默认: /out.log /err.log）")
    parser.add_argument("--check-interval", type=int, default=60, 
                       help="检查间隔(秒)，默认60秒")
    parser.add_argument("--threshold-minutes", type=int, default=5,
                       help="触发阈值(分钟)，默认5分钟")
    parser.add_argument("--daemon", action="store_true",
                       help="以后台守护进程模式运行")
    parser.add_argument("--log-file", default="/tmp/stack_log_monitor.log",
                       help="日志文件路径")
    parser.add_argument("--trigger-mode", choices=["continuous", "once"], default="continuous",
                       help="触发模式: continuous=持续触发, once=只触发一次 (默认: continuous)")
    parser.add_argument("--analysis-base-path", default="/tmp/stack_analysis",
                       help="分析结果基础路径")
    
    args = parser.parse_args()
    
    # 设置日志
    logger = setup_logging(args.log_file, args.daemon)
    
    # 如果指定了daemon参数，则转为守护进程
    if args.daemon:
        logger.info("正在转为守护进程模式运行...")
        daemonize()
        # 守护进程模式下重新设置日志（因为文件描述符可能已改变）
        logger = setup_logging(args.log_file, True)
        logger.info("已转为守护进程模式")
    
    # 参数验证
    if not args.coordinator_host:
        logger.error("错误: 必须提供协调器主机地址")
        sys.exit(1)
    
    try:
        monitor_logs_and_trigger(
            coordinator_host=args.coordinator_host,
            coordinator_port=args.coordinator_port,
            log_files=args.log_files,
            check_interval=args.check_interval,
            threshold_minutes=args.threshold_minutes,
            logger=logger,
            trigger_mode=args.trigger_mode,
            analysis_base_path=args.analysis_base_path
        )
    except Exception as e:
        logger.error(f"程序异常退出: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()