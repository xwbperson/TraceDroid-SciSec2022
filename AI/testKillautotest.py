import os
import subprocess

"""
该脚本主要通过执行 shell 命令来实现自动化测试操作，
具体而言，通过使用 adb 命令来管理应用程序的安装、启动、关闭等操作。
其中，os 模块的 sleep() 函数用于等待应用程序启动或关闭完成。
最终，通过检查应用程序的 PID 值来验证应用程序是否已经成功关闭
"""
PACKAGE_NAME = "com.android.systemui"


def run_command(command):
    """执行 shell 命令"""
    print(f"执行命令: {command}")
    os.system(command)


def check_app_installed():
    """检查应用程序是否已安装"""
    command = f"adb shell pm list packages {PACKAGE_NAME}"
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, universal_newlines=True)
    return PACKAGE_NAME in result.stdout


def install_app():
    """安装应用程序"""
    apk_file = os.path.join(os.getcwd(), "systemui.apk")
    command = f"adb install -r {apk_file}"
    run_command(command)


def start_app():
    """启动应用程序"""
    command = f"adb shell am start -n {PACKAGE_NAME}/com.android.systemui.SysUI"
    run_command(command)
    # 等待应用程序启动完成
    os.sleep(5)


def kill_app():
    """关闭应用程序"""
    command = f"adb shell am force-stop {PACKAGE_NAME}"
    run_command(command)


def check_app_closed():
    """检查应用程序是否已经关闭"""
    command = f"adb shell pidof {PACKAGE_NAME}"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    pid = result.stdout.strip()
    return not pid or pid == '0'


if __name__ == "__main__":
    # 检查应用程序是否已经安装，如果没有，就先安装
    if not check_app_installed():
        install_app()

    # 启动应用程序，并等待应用程序启动完成
    start_app()

    # 关闭应用程序，并等待应用程序关闭完成
    kill_app()
    os.sleep(5)

    # 检查应用程序是否已经关闭
    if check_app_closed():
        print("应用程序关闭成功")
    else:
        print("应用程序关闭失败")
