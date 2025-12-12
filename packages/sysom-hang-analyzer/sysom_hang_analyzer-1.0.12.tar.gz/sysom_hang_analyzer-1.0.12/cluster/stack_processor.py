# stack_processor.py
import argparse
import json
import os
import sys
from pathlib import Path
import re
from collections import defaultdict


class StackTrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_stack = False
        self.ranks = set()  # 存储经过此节点的所有rank


class StackTrie:
    def __init__(self, all_ranks):
        self.root = StackTrieNode()
        self.all_ranks = all_ranks

    def insert(self, words, rank):
        node = self.root
        for word in words:
            # 跳过包含lto_priv的行
            if "lto_priv" in word:
                break
            if word not in node.children:
                node.children[word] = StackTrieNode()
            node = node.children[word]
            node.ranks.add(rank)
        node.is_end_of_stack = True
        node.ranks.add(rank)

    def _format_rank_str(self, ranks):

        leak_ranks = list(self.all_ranks - set(ranks))
        ranks = list(ranks)

        def _inner_format(ranks):
            """fold continuous ranks, [0,1,2,5,6,7]->[0-2,5-7]
            return has stack and leak stack, suppose we have 8 ranks(0-7)
            [0,1,2,5,6,7]->0-2/5-7|3-4, means rank 0-2,5-7 has this stacktrace,
            while rank 3-4 do not have this stacktrace
            """
            ranks = sorted(ranks)
            str_buf = []
            low = 0
            high = 0
            total = len(ranks)
            while high < total - 1:
                low_value = ranks[low]
                high_value = ranks[high]
                while high < total - 1 and high_value + 1 == ranks[high + 1]:
                    high += 1
                    high_value = ranks[high]
                low = high + 1
                high += 1
                if low_value != high_value:
                    str_buf.append(f"{low_value}-{high_value}")
                else:
                    str_buf.append(str(low_value))
            if high == total - 1:
                str_buf.append(str(ranks[high]))
            return "/".join(str_buf)

        has_stack_ranks = _inner_format(ranks)
        leak_stack_ranks = _inner_format(leak_ranks)
        return f"@{'|'.join([has_stack_ranks, leak_stack_ranks])}"

    def _traverse_with_all_stack(self, node, path):
        for word, child in node.children.items():
            rank_str = self._format_rank_str(child.ranks)
            if child.is_end_of_stack:
                yield ";".join(path + [word]) + rank_str
            word += rank_str
            yield from self._traverse_with_all_stack(child, path + [word])

    def __iter__(self):
        yield from self._traverse_with_all_stack(self.root, [])


def is_hex_address(name):
    """判断是否是十六进制地址"""
    # 匹配 0x 开头的十六进制地址
    hex_pattern = re.compile(r'^0x[0-9a-fA-F]+$')
    return bool(hex_pattern.match(name))


def process_combined_stacks(data_files, output_path):
    """处理组合堆栈（Python和Native）"""
    if not data_files:
        print("没有找到堆栈数据文件")
        return

    # 获取world_size
    first_file = data_files[0]
    with open(first_file, 'r') as f:
        first_data = json.load(f)
    world_size = first_data.get('world_size', 1)
    all_ranks = set(range(world_size))

    # 创建trie树
    stack_trie = StackTrie(all_ranks)

    # 处理每个文件
    for file_path in data_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
            continue
        
        rank = data['rank']
        
        # 添加进程状态作为根节点
        stack_trie.insert([f"State@{data.get('process_state', 'Unknown')}"], rank)
        
        # 处理堆栈数据（现在包含Python和native堆栈）
        stack_data = data.get('stack_data', [])
        for thread in stack_data:
            frames = thread.get('frames', [])
            # 反转堆栈顺序（从底部到顶部）
            stack_frames = []  # 不再需要标记PYTHON_STACK或NATIVE_STACK
            
            for frame in reversed(frames):
                func_name = frame.get('name', 'unknown')
                filename = frame.get('filename', 'unknown')
                line = frame.get('line', 0)
                
                # 过滤掉十六进制地址名称
                if is_hex_address(func_name):
                    continue
                
                # 判断是否是native帧
                module = frame.get('module', None)
                if module and (module.endswith('.so') or '.so.' in module):
                    # Native帧
                    short_filename = frame.get('short_filename', filename)
                    func_file_name = f"{func_name}@{short_filename}:{line}"
                    stack_frames.append(f"NATIVE:{func_file_name}")
                else:
                    # Python帧
                    func_file_name = f"{func_name}@{filename}:{line}"
                    stack_frames.append(f"PYTHON:{func_file_name}")
            
            # 插入到trie树
            if len(stack_frames) > 0:  # 确保有实际的堆栈帧
                stack_trie.insert(stack_frames, rank)

    # 生成输出文件
    stack_file = os.path.join(output_path, "combined_stack")
    try:
        with open(stack_file, 'w') as f:
            count = 0
            for stack in stack_trie:
                if stack and not stack.startswith(';'):  # 确保堆栈不为空且不以分号开头
                    # 确保每行都以" 1"结尾
                    if not stack.endswith(" 1"):
                        stack = stack + " 1"
                    f.write(f"{stack}\n")
                    count += 1
            print(f"组合堆栈已保存到: {stack_file} (共{count}行)")
    except Exception as e:
        print(f"保存组合堆栈文件时出错: {e}")
        
    # 生成统一的火焰图
    flamegraph_file = os.path.join(output_path, "combined_stack.svg")
    os.system(
        "flamegraph.pl --color python --width 1600 --title "
        f"'Combined Python and Native Stacks' < {stack_file} "
        f"> {flamegraph_file}"
    )
    print(f"火焰图已保存到: {flamegraph_file}")


def main():
    parser = argparse.ArgumentParser(description="处理堆栈数据")
    parser.add_argument("--path", "-p", type=str, required=True, help="堆栈数据路径")
    parser.add_argument("--output-dir", "-o", type=str, help="输出目录（默认与输入路径相同）")
    
    args = parser.parse_args()
    
    path = Path(args.path)
    if not path.exists():
        print(f"路径 {path} 不存在")
        return 1
    
    # 设置输出目录
    output_dir = args.output_dir if args.output_dir else str(path)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 查找所有.stackdata文件
    data_files = list(path.glob("*.stackdata"))
    if not data_files:
        print(f"在路径 {path} 中未找到任何.stackdata文件")
        return 1
    
    print(f"找到 {len(data_files)} 个堆栈数据文件")
    
    # 处理组合堆栈（Python和Native）
    process_combined_stacks(data_files, str(output_path))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())