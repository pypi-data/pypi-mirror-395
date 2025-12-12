# setup.py
import os
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
import subprocess
import sys

def install_system_dependencies():
    """自动安装系统依赖"""
    try:
        # 检查是否是基于 Debian/Ubuntu 的系统
        if os.path.exists('/etc/debian_version'):
            print("检测到 Debian/Ubuntu 系统，正在安装系统依赖...")
            try:
                subprocess.check_call(['sudo', 'apt-get', 'update'])
                subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'gdb'])
                print("gdb 安装完成")
            except Exception as e:
                print(f"在 Debian/Ubuntu 上安装 gdb 失败: {e}")
                print("请手动安装: sudo apt-get install gdb")
        
        # 检查是否是基于 RedHat/CentOS/Fedora 的系统
        elif os.path.exists('/etc/redhat-release'):
            print("检测到 RedHat/CentOS/Fedora 系统，正在安装系统依赖...")
            try:
                # 尝试使用 dnf (较新的系统)
                try:
                    subprocess.check_call(['sudo', 'dnf', 'install', '-y', 'gdb'])
                    print("gdb 安装完成")
                except:
                    # 如果 dnf 不可用，尝试使用 yum (较老的系统)
                    subprocess.check_call(['sudo', 'yum', 'install', '-y', 'gdb'])
                    print("gdb 安装完成")
            except Exception as e:
                print(f"在 RedHat/CentOS/Fedora 上安装 gdb 失败: {e}")
                print("请手动安装: sudo yum install gdb 或 sudo dnf install gdb")
        
        # 检查是否是基于 Arch Linux 的系统
        elif os.path.exists('/etc/arch-release'):
            print("检测到 Arch Linux 系统，正在安装系统依赖...")
            try:
                subprocess.check_call(['sudo', 'pacman', '-S', '--noconfirm', 'gdb'])
                print("gdb 安装完成")
            except Exception as e:
                print(f"在 Arch Linux 上安装 gdb 失败: {e}")
                print("请手动安装: sudo pacman -S gdb")
        
        else:
            print("未知的系统类型，无法自动安装 gdb")
            print("请手动安装 gdb:")
            print("  Ubuntu/Debian: sudo apt-get install gdb")
            print("  CentOS/RHEL: sudo yum install gdb")
            print("  Fedora: sudo dnf install gdb")
            print("  Arch Linux: sudo pacman -S gdb")
            
    except Exception as e:
        print(f"安装系统依赖时出错: {e}")

def install_py_spy():
    """安装 py-spy"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'py-spy'])
    except Exception as e:
        print(f"Warning: Failed to install py-spy: {e}")

def install_pstack():
    """安装 pstack"""
    try:
        import shutil
        source_pstack = os.path.join(os.path.dirname(__file__), 'cluster', 'pstack')
        dest_pstack = '/opt/conda/bin/pstack'
        
        if os.path.exists(source_pstack):
            # 确保目标目录存在
            os.makedirs(os.path.dirname(dest_pstack), exist_ok=True)
            shutil.copy2(source_pstack, dest_pstack)
            # 设置执行权限
            os.chmod(dest_pstack, 0o755)
            print(f"Successfully installed pstack to {dest_pstack}")
        else:
            print("Warning: pstack script not found")
    except Exception as e:
        print(f"Warning: Failed to install pstack to /opt/conda/bin/: {e}")

class PostInstallCommand(install):
    """Custom post-installation for installation mode."""
    def run(self):
        install.run(self)
        # install_system_dependencies()
        install_py_spy()
        install_pstack()

class PostDevelopCommand(develop):
    """Custom post-develop for development mode."""
    def run(self):
        develop.run(self)
        # install_system_dependencies()
        install_py_spy()
        install_pstack()

class PostEggInfoCommand(egg_info):
    """Custom post-egg_info for egg_info mode."""
    def run(self):
        egg_info.run(self)
        # install_system_dependencies()
        install_py_spy()
        install_pstack()

setup(
    name="sysom-hang-analyzer",
    version="1.0.12",
    author="Your Name",
    author_email="your.email@example.com",
    description="Distributed stack collection and analysis tool",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        'cluster': ['flamegraph.pl', 'pstack'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6",
    install_requires=[
        "tqdm",
        "py-spy",
    ],
    entry_points={
        "console_scripts": [
            "distributed-coordinator=cluster.distributed_coordinator:main",
            "node-agent=cluster.node_agent:main",
            "stack-collector=cluster.auto_stack_collector:main",
            "stack-processor=cluster.stack_processor:main",
            "aggregate-analysis=cluster.aggregate_analysis:main",
            "trigger-collection=cluster.trigger_distributed_collection:main",
            "sysom-hang-analyzer=cluster.sysom_hang_analyzer:main",
        ],
    },
    scripts=['cluster/pstack', 'cluster/flamegraph.pl'],
    cmdclass={
        'install': PostInstallCommand,
        'develop': PostDevelopCommand,
        'egg_info': PostEggInfoCommand,
    },
)