import os
import signal
import subprocess
import time
import uiautomator2 as u2

# 连接了一台 Android 设备，并返回一个 device 对象，该对象可以用于控制设备上的应用程序
device = u2.connect('8BSX1EQGX')
# 定义了一个 captureCommand 变量，该变量包含了一个命令行指令，
# 用于在设备上执行一个名为 tcs.py 的 Python 程序，
# 并将程序输出重定向到一个名为 tom2.pcap 的文件中
captureCommand = 'python3 tcs.py -U -f com.outfit7.mytalkingtom2.qihoo -v -p tom2.pcap'
# 启动一个新的进程，并将 captureCommand 作为参数传递给 Popen()，以便在子进程中执行该命令行指令
sub = subprocess.Popen(captureCommand, shell=True, bufsize=-1, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
# 获取子进程的 PID，打印输出
pid = sub.pid
print(pid)
# 在主程序中加入一个简单的等待时间函数 time.sleep(60)，让程序等待 60 秒钟
time.sleep(60)
# 尝试通过 os.kill() 和 sub.kill() 停止子进程的运行，并输出 PID 被杀的信息
try:
    os.kill(pid, signal.SIGINT)
    os.kill(pid, signal.SIGTERM)
    sub.kill()
except:
    pass

# killCommand = 'kill -2 %s' % pid
# os.system(killCommand)
print('%s killed' % pid)
# 停止名为 'com.outfit7.mytalkingtom2.qihoo' 的 Android 应用程序，
# 并输出应用程序关闭的信息
device.app_stop('com.outfit7.mytalkingtom2.qihoo')
print('app stoped')

"""
这段代码是一段用于停止一个应用程序并杀死子进程的 Python 代码片段。
其主要用途是展示如何使用 Python 来控制 Android 设备和执行命令行指令，
并且使用 os.kill() 和 sub.kill() 来结束已经启动的子进程，并停止运行指定的应用程序
"""
