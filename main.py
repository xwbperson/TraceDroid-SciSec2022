import configparser
import logging.config
import logging.handlers
import os
import signal
import time
import subprocess

import psutil

import init
import uiautomator2 as u2
import DBUtils

# 加载一个log.conf文件
logging.config.fileConfig('log.conf')
# 创建一个名为“APKTestEngine”的日志记录器（logger），以方便在后续的代码中使用该记录器输出日志信息
logger = logging.getLogger('APKTestEngine')
# 创建一个ConfigParser对象
config = configparser.ConfigParser()
# 读取配置文件config.conf，并将读取到的设备配置信息和文件路径配置信息分别存储到变量deviceConfig和fileConfig中
config.read('./config.conf')
deviceConfig = config['device']
fileConfig = config["filePath"]


# 使用uiautomator2库连接设备
# 为了保证程序的通用性，连接设备应该在脚本中动态指定，而不是在代码中写死
# device = u2.connect(deviceConfig['deviceID'])

# 进行APP的初始化操作，并将初始化操作日志存入数据库
# 对一个应用的APK文件进行预处理，以便进行后续的测试
def preProcessAPK(APK) -> object:
    """

    :param APK，单个APK的元数据信息
    :return:
    """

    # 表明正在对应用进行预处理操作，同时输出APK的名称、APP名和APK文件路径等元数据信息
    logger.info('start preprocessing app')
    logger.info('APK Name: %s; APP Name: %s; APKFilePath: %s', APK["APKName"], APK["APPName"], APK["APKFilePath"])

    # APKFilePath = APK["APKFilePath"]
    # 调用init.verifyPermissions()函数，对APK进行权限验证，并将验证结果作为函数返回值返回
    return init.verifyPermissions(APK)


def startCapture(APK):
    """

    :param APKID: 单个APK的元数据信息
    :return:
    """
    # 从APK参数中读取应用的元数据信息，包括应用的ID、名称、包名等
    APKID = APK["APKID"]
    APKName = APK["APKName"]
    packageName = APK["packageName"]
    APPName = APK["APPName"]
    # 表明正在启动流量捕获和自动点击脚本，并输出应用的名称和ID信息
    logger.debug('start capture APK traffic')
    logger.debug('APK Name: %s; APP Name: %s', APK["APKName"], APKName)
    # 生成一个pcap文件名，将其存储到变量pcapFileName中
    pcapFileName = APKName + str(time.time()) + ".pcap"
    # 生成一个空的进程名，将其存储到变量stackFileName中
    stackFileName = "tmpName"
    # 从APK参数中读取APK文件路径，并将其存储到变量APKFilePath中
    APKFilePath = APK["APKFilePath"]

    logger.debug("pcapFileName: %s", pcapFileName)
    logger.debug("packageName: %s", packageName)

    # 创建一个名为sub的新进程，调用tcs.py脚本进行流量捕获，并将捕获结果保存到指定的pcap文件中
    sub = subprocess.Popen(
        ["python3", "tcs.py", "-U", "-f", packageName, "-p", fileConfig["pcapFilePathPrefix"] + pcapFileName],
        bufsize=-1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # 记录该进程的pid，并等待20秒，以确保流量捕获进程已经成功启动，并开始捕获流量数据
    pid = sub.pid
    time.sleep(20)

    # 启动自动点击脚本，并等待180秒，以模拟应用的正常使用过程
    logger.debug("starting auto click process...")
    clickProcess = startAutoClick()

    logger.debug("waiting for 180 seconds...")
    time.sleep(180)

    try:
        # 向自动点击进程发送一个SIGKILL信号，以终止自动点击进程
        logger.debug("try to kill autoClick...")
        os.kill(clickProcess.pid, 9)
    except:
        logger.debug("kill autoClick failed")
        pass

    try:
        # 向流量捕获进程发送SIGINT信号，以终止流量捕获进程
        logger.debug("try to signal to capture process")
        sub.send_signal(signal.SIGINT)
    except:
        logger.debug("signal failed")
        pass

    time.sleep(5)
    # 终止流量捕获子进程
    logger.debug("killing capture process")
    sub.kill()
    # 终止自动点击脚本的进程
    logger.debug("killing autoClick process")
    clickProcess.kill()

    d = u2.connect('8BSX1EQGX')
    d.app_stop(packageName)
    logger.debug("stop app ok")
    logger.debug("pcapFileName: %s, stackFileName: %s" % (pcapFileName, stackFileName))

    # 使用ADB命令卸载应用程序
    uninsatllCommand = "adb uninstall %s" % packageName
    os.system(uninsatllCommand)
    logger.debug("apk %s uninstalled !!!" % packageName)
    # 将pcap文件名和进程名作为函数返回值返回
    return pcapFileName, stackFileName


"""
函数的作用是启动自动点击脚本，该脚本能够模拟用户对应用程序的随机点击行为，
从而使应用程序在不同的使用场景下产生各种数据包，以便我们对应用程序的网络性
能进行测试和分析
"""
"""    
subprocess.Popen()函数启动一个新进程，指定要执行的程序为以python3解释器解释的test.py文件
bufsize=-1参数指定使用系统默认缓存大小
stdin=subprocess.PIPE参数将stdin设为PIPE，即可将子进程的标准输入设为管道，从而将自动点击脚本的输入流放到管道中
stdout=subprocess.PIPE参数将stdout设为PIPE，即可将自动点击脚本的输出流放到管道中
用stderr=subprocess.STDOUT参数将stderr指定为STDIN，从而将子进程的错误输出输出到标准输出
"""


def startAutoClick():
    # 启动名为test.py的Python脚本，并返回新创建的进程对象（subProcess）
    subProcess = subprocess.Popen(["python3", "test.py"], bufsize=-1, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return subProcess


if __name__ == '__main__':
    # 在系统启动的时候输出一条信息，日志级别为INFO，用于提示用户或开发人员系统正在启动
    logger.info('\n==========system starting==========')
    while 1:
        # 通过getUnProcessedAPKs函数获取要测试的应用信息
        APKDict = DBUtils.getUnProcessedAPKs()
        # 检测是否存在需要测试的应用
        if len(APKDict) == 0:
            # 如果没有需要测试的应用（即获取到的APKDict字典为空），那么就输出一条信息，提示用户或开发人员没有应用需要进行测试
            logger.info('no apk needs to be tested, waiting for next time...')
            time.sleep(30)
            continue
        else:
            for APK in APKDict:
                # 输出调试信息，提示当前测试的应用
                logger.info('--------start APK test--------')
                # 输出当前主进程的pid
                logger.debug("main pid: %s" % os.getpid())
                # 杀死所有子进程的信息
                logger.debug("killing all children process..")
                procs = psutil.Process().children()
                for p in procs:
                    logger.debug("child process id: %s" % p.pid)
                    logger.debug("child process name: %s" % p.name())
                    p.terminate()
                # 调用preProcessAPK函数对应用进行初始化操作，获取操作结果
                result = preProcessAPK(APK)
                if result:
                    # 如果初始化操作成功，则使用DBUtils.writePreProcessLog函数记录操作日志
                    DBUtils.writePreProcessLog(APK)
                    # 进行数据包抓取操作（调用startCapture函数）
                    pcapFileName, stackFileName = startCapture(APK)
                    # 自动点击操作（调用startAutoClick函数）
                    childClickPid = startAutoClick()
                    # .使用DBUtils.writeCaptureLog函数记录获取的数据包和点击信息，并更新应用测试状态
                    re, logID = DBUtils.writeCaptureLog(APK, pcapFileName, stackFileName)
                    DBUtils.updateAPKFlag(APK)

                    # 对数据进行提取和分析的操作，具体实现可以根据需求进行调整
                    # extractUtils.extractHTTPMetadata(APK, logID)
                    # DBUtils.updateCaptureLogFlag(APK, logID)
                else:
                    # 初始化操作失败，则输出警告信息
                    logger.warning("APK preProcess failed %s", APK["APKName"])
                    pass
                # .每处理完一个应用，就调用time模块中的sleep函数暂停3秒，防止连续处理多个应用导致系统负载过高
                time.sleep(3)
