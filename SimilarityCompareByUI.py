import os
import sys
import EditDistance as ED


# 用于比较输入目录下的文件内容的相似度，并输出相似度的值
def SimilarityCompare(filePath):
    dirList = os.listdir(filePath)
    # 获取目录下所有文件名列表
    for i in range(len(dirList)):
        fileList = os.listdir(filePath + "\\" + dirList[i])
        # 对于每个目录，获取其下第一个和第二个文件的文件名 fileName1 和 fileName2
        fileName1 = filePath + "\\" + dirList[i] + "\\" + fileList[0]
        fileName2 = filePath + "\\" + dirList[i] + "\\" + fileList[1]
        # 读取文件内容，并将其存储在相应的字符串列表 contents_file1 和 contents_file2 中
        f1 = open(fileName1)
        contents_file1 = f1.readlines();
        f1.close()
        f2 = open(fileName2)
        contents_file2 = f2.readlines();
        f2.close()
        num = 0
        # 对于字符串列表 contents_file1 中的每个字符串 msg1，
        # 计算其和字符串列表 contents_file2 中的每个字符串 msg2 的编辑距离相似度，
        # 并找到最大值。如果两个字符串的长度差超过 5，则不进行比较
        for msg1 in contents_file1:
            num = num + 1;
            maxSim = sys.float_info.min
            msg1 = msg1.strip('\n')
            for msg2 in contents_file2:
                msg2 = msg2.strip('\n')
                if (len(msg1) - len(msg2)) < 5:
                    maxSim = max(maxSim, ED.editDistanceSimilarity(msg1, msg2))
            print(maxSim)
