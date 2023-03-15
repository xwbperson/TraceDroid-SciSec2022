import logging.config
import logging.handlers
import configparser
import uuid
import pymysql  # pip install pymysql

# 从配置文件中读取数据库连接信息和文件路径信息
logging.config.fileConfig('log.conf')
logger = logging.getLogger('APKTestEngine')

config = configparser.ConfigParser()
config.read('./config.conf')
deviceConfig = config['device']
fileConfig = config["filePath"]


# 用于从配置文件中读取数据库连接信息，getDBConnection()函数将其用于建立数据库连接
def getDBConfig() -> object:
    """

    :return: 数据库配置信息
    """
    config = configparser.ConfigParser()
    config.read('/home/chj/APKTestEngine/config.conf')
    dbConfig = config['database']
    return dbConfig


# 用于将APK元数据写入数据库中，包括APP名称、APK名称、包名、APK文件路径、APK商店名
# 将needAnalyse设置为1，表示需要进行预处理
def writeAPKMetaData(APPName, APKName, packageName, APKFilePath, APKStoreName, needAnalyse):
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


def getDBConnection() -> object:
    '''

    :return: 数据库连接
    '''
    dbConfig = getDBConfig()
    host = dbConfig['host']
    port = int(dbConfig['port'])
    user = dbConfig['user']
    password = dbConfig['password']
    database = dbConfig['database']
    DBConnection = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
    return DBConnection


# 根据APKID查询APK元数据信息，返回值为字典类型
def getAPKMetadataByID(APKID):
    '''

    :param APKID: APKID
    :return: 该APKID对应的APK元数据信息，是字典类型
    '''
    DBConnection = getDBConnection()
    DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
    selectSql = "SELECT * FROM APKMetadata WHERE APKID = %s"
    DBCursor.execute(selectSql, APKID)
    APK = DBCursor.fetchone()
    DBCursor.close()
    return APK


# 预处理完成后调用此函数，将预处理日志写入数据库
# 将单个APK的元数据入库，在进行预处理前调用。将APKID、APKName和APPName写入PreProcessLog表中
def writePreProcessLog(APK):
    '''

    :param APK: 单个APK的元数据信息
    :return: 返回日志是否写入成功
    '''
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


# 根据APKID查询APP信息，将APP抓包的相关信息写入CaptureLog数据库，包括pcap文件存储路径、调用栈文件存储路径
# 将抓包信息写入CaptureLog表中，包括logID、APKID、APKName、APPName、pcap文件路径和stack文件路径
def writeCaptureLog(APK, pcapFileName, stackFileName):
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
        DBCursor.execute(insertSql,
                         [str(logID), str(APKID), APK["APKName"], APK["APPName"], pcapFilePath, stackFilePath, 1])
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


# 该函数从数据库中读取所有APK信息，并返回需要进行预处理的APK信息
# 从数据库中读取需要进行预处理的APK信息，以字典类型返回
# 如果出现已经处理过的APK，则将其needAnalyse标记为2，表明需要重新处理
def getUnProcessedAPKs():
    '''

    :return: APKDict，这是个字典，对应着MySQL中APKMetadata表
    '''

    logger.debug('start getting unprocessed APK Dict...')
    DBConnection = getDBConnection()
    DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
    selectSql = "SELECT * FROM APKMetadata WHERE needAnalyse = 1"
    DBCursor.execute(selectSql)
    APKDict = DBCursor.fetchall()
    logger.debug('APKDict size is: %d', len(APKDict))
    logger.debug(APKDict)
    # for APK in APKDict:
    #    print(APK["APKName"])
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


# 用于读取已处理的最后一个APK的APKID，用于判断出现已处理过的APK的情况
def getProcessedAPKID():
    logger.debug("start getting processed APK Dcit")
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


# 用于根据logID查询CaptureLog中的信息
def findCaptureLogByID(logID):
    logger.debug("findCaptureLogByLogID: %s" % logID)
    DBConnection = getDBConnection()
    DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
    selectSql = "SELECT * FROM CaptureLog WHERE logID = %s"
    DBCursor.execute(selectSql, logID)
    captureLogDict = DBCursor.fetchone()
    logger.debug("findCaptureLogByID OK %s" % captureLogDict)
    return captureLogDict


# 用于将APK的needAnalyse标记为0，表示预处理已完成
def updateAPKFlag(APK):
    logger.info('updateAPKFlag...')
    DBConnection = getDBConnection()
    DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
    updateSql = "update APKMetadata SET lastModifiedTime = CURRENT_TIMESTAMP, needAnalyse = 0 WHERE APKID = %s"
    try:
        DBCursor.execute(updateSql, APK["APKID"])
        DBConnection.commit()
        logger.debug("updateAPKFlag ok")
    except Exception as e:
        logger.error("Exception: %s" % e)
        DBConnection.rollback()
        logger.error('fail to update needAnalyse to db: %s', APK)
    DBConnection.close()
    return


# 用于将APK的needAnalyse标记为2，表示需要重新预处理
def updateAPKFlag2(APK):
    logger.info('updateAPKFlag...')
    DBConnection = getDBConnection()
    DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
    updateSql = "update APKMetadata SET lastModifiedTime = CURRENT_TIMESTAMP, needAnalyse = 2 WHERE APKID = %s"
    try:
        DBCursor.execute(updateSql, APK["APKID"])
        DBConnection.commit()
        logger.debug("updateAPKFlag ok")
    except Exception as e:
        logger.error("Exception: %s" % e)
        DBConnection.rollback()
        logger.error('fail to update needAnalyse to db: %s', APK)
    DBConnection.close()
    return


# 用于将CaptureLog的needExtract标记为0，表示抓包信息已提取完成
def updateCaptureLogFlag(APK, logID):
    """

    Args:
        APK:
        logID:

    Returns:

    """

    logger.info('update extract flag, logID: %s', logID)
    DBConnection = getDBConnection()
    DBCursor = DBConnection.cursor(pymysql.cursors.DictCursor)
    updateSql = "UPDATE CaptureLog SET needExtract = 0, extractTime = CURRENT_TIMESTAMP WHERE logID = %s"
    try:
        DBCursor.execute(updateSql, logID)
        DBConnection.commit()
        logger.debug("updateCaptureLogFlag OK, logID: %s" % logID)
    except Exception as e:
        logger.error("Exception: %s" % e)
        DBConnection.rollback()
        logger.error('updateCaptureLogFlag failed. logID: %s', logID)
    DBConnection.close()


if __name__ == '__main__':
    captureLog = findCaptureLogByID("e7b0dc7e-efaa-4b80-8317-400c8d7e9877")
    logID = captureLog["logID"]
    updateCaptureLogFlag(0, logID)
