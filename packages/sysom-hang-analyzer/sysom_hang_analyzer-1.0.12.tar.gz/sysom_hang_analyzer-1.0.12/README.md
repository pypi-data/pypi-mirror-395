# SYSOM Hang Analyzer

分布式堆栈收集和分析工具包，用于收集和分析多节点Python程序的堆栈信息。

## 功能特性

- 自动检测GPU进程并收集Python和原生堆栈
- 分布式收集支持（多节点协调）
- 堆栈数据分析和可视化
- 生成火焰图(flame graphs)


## 系统依赖

在安装Python包之前，请确保安装了必要的系统依赖：

<!-- ### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install gdb

### CentOS/RHEL:
```bash
sudo yum install gdb

### Fedora:
```bash
sudo dnf install gdb -->

## 安装

```bash
pip install sysom-hang-analyzer