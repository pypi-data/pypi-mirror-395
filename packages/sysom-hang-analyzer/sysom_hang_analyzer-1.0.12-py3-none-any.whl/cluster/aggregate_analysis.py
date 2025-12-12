# aggregate_analysis.py
import argparse
import json
import os
import subprocess  # 添加导入
from pathlib import Path
import glob

def aggregate_stack_data(input_dir, output_dir):
    """聚合所有节点的堆栈数据"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 收集所有节点的数据
    all_stack_files = []
    for node_dir in input_path.iterdir():
        if node_dir.is_dir() and node_dir.name.startswith('node_'):
            stack_files = list(node_dir.glob("*.json"))
            all_stack_files.extend(stack_files)
    
    print(f"找到 {len(all_stack_files)} 个堆栈数据文件")
    
    # 合并所有数据
    aggregated_data = []
    for stack_file in all_stack_files:
        try:
            with open(stack_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    aggregated_data.extend(data)
                else:
                    aggregated_data.append(data)
        except Exception as e:
            print(f"读取文件 {stack_file} 失败: {e}")
    
    # 保存聚合数据
    aggregated_file = output_path / "aggregated_stack_data.json"
    with open(aggregated_file, 'w') as f:
        json.dump(aggregated_data, f, indent=2)
    
    print(f"聚合数据已保存到: {aggregated_file}")
    
    # 转换为原有格式以便分析
    convert_to_original_format(aggregated_data, output_path)
    
def convert_to_original_format(aggregated_data, output_path):
    """转换为原有.stackdata格式"""
    for i, data in enumerate(aggregated_data):
        if isinstance(data, list):
            # 如果是列表，处理每个元素
            for j, item in enumerate(data):
                filename = f"{i:05d}_{j:05d}.stackdata"
                filepath = output_path / filename
                with open(filepath, 'w') as f:
                    json.dump(item, f, indent=2)
        else:
            # 单个对象
            filename = f"{i:05d}.stackdata"
            filepath = output_path / filename
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
    
    print(f"已转换 {len(aggregated_data)} 个文件为原始格式")

def main():
    parser = argparse.ArgumentParser(description="聚合分布式堆栈数据")
    parser.add_argument("--input-dir", default="/tmp/stack_data_all", help="输入目录（协调器的dump路径）")
    parser.add_argument("--output-dir", default="/tmp/stack_analysis", help="输出目录")
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 调用聚合函数
    # aggregate_stack_data(args.input_dir, args.output_dir)
    
    # 运行原有分析脚本    
    cmd = [
        "python3", "-m", "cluster.stack_processor",
        "--path", args.input_dir,
        "--output-dir", args.output_dir,
    ]
    
    print("运行堆栈分析...")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print("分析完成")
    else:
        print("分析失败")

if __name__ == "__main__":
    main()