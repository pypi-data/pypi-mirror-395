#!/bin/bash
# deploy_distributed_stack.sh

# 部署协调器（在主节点上运行）
deploy_coordinator() {
    local host=${1:-0.0.0.0}
    local port=${2:-8080}
    local dump_path=${3:-/tmp/stack_data}
    
    echo "部署协调器: $host:$port"
    nohup python3 distributed_coordinator.py \
        --host "$host" \
        --port "$port" \
        --dump-path "$dump_path" > /tmp/coordinator.log 2>&1 &
    
    echo "协调器已启动，日志: /tmp/coordinator.log"
}

# 部署节点代理（在每个训练节点上运行）
deploy_node_agent() {
    local coordinator_host=$1
    local coordinator_port=${2:-8080}
    local node_id=$3
    local dump_path=${4:-/tmp/stack_data}
    
    if [ -z "$coordinator_host" ]; then
        echo "错误: 必须提供协调器主机地址"
        return 1
    fi
    
    echo "部署节点代理，连接到: $coordinator_host:$coordinator_port"
    nohup python3 node_agent.py \
        --coordinator-host "$coordinator_host" \
        --coordinator-port "$coordinator_port" \
        --node-id "$node_id" \
        --dump-path "$dump_path" > /tmp/node_agent.log 2>&1 &
    
    echo "节点代理已启动，日志: /tmp/node_agent.log"
}

# 触发采集
trigger_collection() {
    local coordinator_host=$1
    local coordinator_port=${2:-8080}
    
    if [ -z "$coordinator_host" ]; then
        echo "错误: 必须提供协调器主机地址"
        return 1
    fi
    
    echo "触发分布式堆栈采集..."
    python3 trigger_distributed_collection.py \
        --coordinator-host "$coordinator_host" \
        --coordinator-port "$coordinator_port"
}

# 聚合分析
aggregate_analysis() {
    local input_dir=$1
    local output_dir=$2
    
    if [ -z "$input_dir" ] || [ -z "$output_dir" ]; then
        echo "错误: 必须提供输入和输出目录"
        return 1
    fi
    
    echo "聚合分析数据..."
    python3 aggregate_analysis.py \
        --input-dir "$input_dir" \
        --output-dir "$output_dir"
}

# 显示帮助
show_help() {
    echo "用法: $0 [选项]"
    echo "选项:"
    echo "  coordinator [host] [port] [dump_path]  - 部署协调器"
    echo "  node-agent <coordinator_host> [port] [node_id] [dump_path] - 部署节点代理"
    echo "  trigger <coordinator_host> [port]     - 触发采集"
    echo "  aggregate <input_dir> <output_dir>     - 聚合分析"
    echo "  help                                  - 显示此帮助"
}

# 主函数
main() {
    case "$1" in
        coordinator)
            deploy_coordinator "$2" "$3" "$4"
            ;;
        node-agent)
            deploy_node_agent "$2" "$3" "$4" "$5"
            ;;
        trigger)
            trigger_collection "$2" "$3"
            ;;
        aggregate)
            aggregate_analysis "$2" "$3"
            ;;
        help|*)
            show_help
            ;;
    esac
}

# 执行主函数
main "$@"