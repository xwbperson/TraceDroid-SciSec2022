导入所需库
import logging.config
import logging.handlers
import configparser
import uuid
import pymysql  # pip install pymysql

配置日志
logging.config.fileConfig('log.conf')
logger = logging.getLogger('APKTestEngine')

读取配置文件
config = configparser.ConfigParser()
config.read('./config.conf')
deviceConfig = config['device']
fileConfig = config["filePath"]

def getDBConfig() -> object:
"""
获取数据库配置信息
:return: 数据库配置信息
"""
config = configparser.ConfigParser()
config.read('/home/chj/APKTestEngine/config.conf')
dbConfig = config['database']
return dbConfig

写APK元数据信息到数据库
def writeAPKMetaData(APPName, APKName, packageName, APKFilePath, APKStoreName, needAnalyse):
"""
写APK元数据信息到数据库
:param APPName: APP名称
:param APKName: APK名称
:param packageName: 包名
:param APKFilePath: APK文件路径
:param APKStoreName: APK商店名称
:param needAnalyse: 是否需要进行分析
:return:
"""
DBConnection = getDBConnection()
DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
try:
insertSql = "INSERT INTO APKMetadata (APPName, APKName, packageName, APKFilePath, APKStoreName, lastModifiedTime, needAnalyse) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s)"
DBCursor.execute(insertSql, [APPName, APKName, packageName, APKFilePath, APKStoreName, needAnalyse])
DBConnection.commit()
logger.debug("writeAPKMetaData OK")
except Exception as e:
logger.error(e)
DBConnection.rollback()
finally:
DBConnection.close()
return

获取数据库连接
def getDBConnection() -> object:
"""
获取数据库连接
:return: 数据库连接
"""
dbConfig = getDBConfig()
host = dbConfig['host']
port = int(dbConfig['port'])
user = dbConfig['user']
password = dbConfig['password']
database = dbConfig['database']
DBConnection = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
return DBConnection

根据APKID查询APP信息
def getAPKMetadataByID(APKID):
"""
根据APKID查询APP信息
:param APKID: APKID
:return: 该APKID对应的APK元数据信息，是字典类型
"""
DBConnection = getDBConnection()
DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
selectSql = "SELECT * FROM APKMetadata WHERE APKID = %s"
DBCursor.execute(selectSql, APKID)
APK = DBCursor.fetchone()
DBCursor.close()
return APK

写预处理日志到数据库
def writePreProcessLog(APK):
"""
写预处理日志到数据库
:param APK: 单个APK的元数据信息
:return: 返回日志是否写入成功
"""
result = 0
logger.info('writing preprocess log to db: %s', APK)
APKID = APK["APKID"]
DBConnection = getDBConnection()
DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
insertSql = "INSERT INTO PreProcessLog(APKID, APKName, APPName) VALUES (%s, %s, %s) "
try:
DBCursor.execute(insertSql, [APKID, APK["APKName"], APK["APPName"]])
DBConnection.commit()
logger.debug("writePreProcessLog OK")
except Exception as e:
logger.error("Exception: %s" % e)
DBConnection.rollback()
logger.error("writePreProcessLog failed!")
DBConnection.close()
return result

写APP抓包相关信息到CaptureLog表
def writeCaptureLog(APK, pcapFileName, stackFileName):
"""
写APP抓包相关信息到CaptureLog表，包括pcap文件存储路径、调用栈文件存储路径
:param APK: APK元数据信息
:param pcapFileName: pcap文件名
:param stackFileName: 调用栈文件名
:return: 写入结果和logID
"""
logger.info('writing capture log to db: %s', APK)
APKID = APK["APKID"]
DBConnection = getDBConnection()
DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
logID = uuid.uuid4()
logger.debug("logID: %s" % logID)
pcapFilePath = fileConfig["pcapFilePathPrefix"] + pcapFileName
stackFilePath = fileConfig["stackFilePathPrefix"] + stackFileName
insertSql = "INSERT INTO CaptureLog(logID, APKID, APKName, APPName, pcapFilePath, stackFilePath, needExtract) VALUES (%s, %s, %s, %s, %s, %s, %s)"
try:
DBCursor.execute(insertSql, [str(logID), str(APKID), APK["APKName"], APK["APPName"], pcapFilePath, stackFilePath, 1])
DBConnection.commit()
logger.debug("writeCaptureLog OK, logID: %s" % logID)
DBConnection.close()
return 1, logID
except Exception as e:
logger.error("Exception: %s" % e)
logger.error("writeCaptureLog failed. APK: %s" % APK)
DBConnection.rollback()
DBConnection.close()
return 0, logID

获取未处理的APK信息
def getUnProcessedAPKs():
"""
该函数从数据库中读取所有APK信息，并返回需要进行预处理的APK信息
:return: APKDict，这是个字典，对应着MySQL中APKMetadata表
"""
logger.debug('start getting unprocessed APK Dict...')
DBConnection = getDBConnection()
DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
selectSql = "SELECT * FROM APKMetadata WHERE needAnalyse = 1"
DBCursor.execute(selectSql)
APKDict = DBCursor.fetchall()
logger.debug('APKDict size is: %d', len(APKDict))
logger.debug(APKDict)
DBConnection.close()
lastProcessedAPKID = getProcessedAPKID()
for APK in APKDict:
if APK["APKID"] <= lastProcessedAPKID:
logger.debug("find one error APK, updating flag to 2... ")
logger.debug(APK)
updateAPKFlag2(APK)
else:
continue
return APKDict

获取已处理的最后一个APKID
def getProcessedAPKID():
"""
获取已处理的最后一个APKID
:return: 最后一个APKID
"""
logger.debug("start getting processed APK Dict")
DBConnection = getDBConnection()
DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
selectSql = "SELECT * FROM APKMetadata WHERE needAnalyse = 0 ORDER BY APKID DESC"
DBCursor.execute(selectSql)
processedAPKLast = DBCursor.fetchone()
if processedAPKLast is not None and len(processedAPKLast) == 1:
logger.debug('processedAPKlast is: ')
logger.debug(processedAPKLast)
DBConnection.close()
return processedAPKLast["APKID"]
else:
DBConnection.close()
return 0

根据logID查找抓包相关信息
def findCaptureLogByID(logID):
"""
根据logID查找抓包相关信息
:param logID: logID
:return: 抓包相关信息
"""
logger.debug("findCaptureLogByLogID: %s" % logID)
DBConnection = getDBConnection()
DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
selectSql = "SELECT * FROM CaptureLog WHERE logID = %s"
DBCursor.execute(selectSql, logID)
captureLogDict = DBCursor.fetchone()
logger.debug("captureLogDict is: %s" % captureLogDict)
DBConnection.close()
return captureLogDict

更新APK元数据信息的needAnalyse字段为2，表示出错
def updateAPKFlag2(APK):
"""
更新APK元数据信息的needAnalyse字段为2，表示出错
:param APK: 要更新的APK元数据信息
:return: 更新结果
"""
logger.debug("start updating APK flag to 2...")
DBConnection = getDBConnection()
DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
updateSql = "UPDATE APKMetadata SET needAnalyse = 2 WHERE APKID = %s"
try:
DBCursor.execute(updateSql, APK["APKID"])
DBConnection.commit()
logger.debug("update APK flag to 2 success for APK: %s" % APK)
except Exception as e:
logger.error("Exception: %s" % e)
logger.error("update APK flag to 2 failed for APK: %s" % APK)
DBConnection.rollback()
DBConnection.close()
return 0
return 1

更新APK元数据信息的needAnalyse字段为0，表示已处理完毕
def updateAPKFlag0(APK):
"""
更新APK元数据信息的needAnalyse字段为0，表示已处理完毕
:param APK: 要更新的APK元数据信息
:return: 更新结果
"""
logger.debug("start updating APK flag to 0...")
DBConnection = getDBConnection()
DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
updateSql = "UPDATE APKMetadata SET needAnalyse = 0 WHERE APKID = %s"
try:
DBCursor.execute(updateSql, APK["APKID"])
DBConnection.commit()
logger.debug("update APK flag to 0 success for APK: %s" % APK)
except Exception as e:
logger.error("Exception: %s" % e)
logger.error("update APK flag to 0 failed for APK: %s" % APK)
DBConnection.rollback()
DBConnection.close()
return 0
return 1

更新CaptureLog表的needExtract字段为0，表示已经提取了信息
def updateCaptureLogFlag0(logID):
"""
更新CaptureLog表的needExtract字段为0，表示已经提取了信息
:param logID: 要更新的logID
:return: 更新结果
"""
logger.debug("start updating CaptureLog flag to 0...")
DBConnection = getDBConnection()
DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
updateSql = "UPDATE CaptureLog SET needExtract = 0 WHERE logID = %s"
try:
DBCursor.execute(updateSql, str(logID))
DBConnection.commit()
logger.debug("update CaptureLog flag to 0 success for logID: %s" % logID)
except Exception as e:
logger.error("Exception: %s" % e)
logger.error("update CaptureLog flag to 0 failed for logID: %s" % logID)
DBConnection.rollback()
DBConnection.close()
return 0
return 1

从CaptureLog表中删除记录
def deleteCaptureLog(logID):
"""
从CaptureLog表中删除记录
:param logID: 要删除的logID
:return: 删除结果
"""
logger.debug("start deleting CaptureLog...")
DBConnection = getDBConnection()
DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
deleteSql = "DELETE FROM CaptureLog WHERE logID = %s"
try:
DBCursor.execute(deleteSql, str(logID))
DBConnection.commit()
logger.debug("delete CaptureLog success for logID: %s" % logID)
except Exception as e:
logger.error("Exception: %s" % e)
logger.error("delete CaptureLog failed for logID: %s" % logID)
DBConnection.rollback()
DBConnection.close()
return 0
return 1