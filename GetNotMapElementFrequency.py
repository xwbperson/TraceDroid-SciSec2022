import os
import glob


# 得到没有进行映射的元素出现的频率,统计文件中特定字符频率的功能
'''
分析Android APK应用程序中XML格式的布局文件（.xml文件）信息时，统计特定字符在文件中出现的频率
字符‘%’可能代表布局文件中用于定位位置或者在控件中展示文本内容的占位符
字符 ‘&’ 则可能代表命名空间或者作为字符的转义符
。统计这些字符的频率，可能有助于后续对布局文件的解析、渲染和优化等工作
'''
def remainingElementFrequency(filePath):
    filePathList = os.listdir(filePath);
    for i in filePathList:
        fileList = os.path.join(filePath, i);
        fileList = glob.glob(os.path.join(fileList, '*'))
        for file in fileList:
            ApkName = os.path.splitext(file)[0]  # 将txt文件按照它们的文件名和后缀做一个分割
            ApkName = ApkName.split("/")[-1]
            f = open(file)
            contents = f.readlines()
            length = 0;
            ele_per = 0;
            ele_and = 0;
            for msg in contents:
                msg = msg.strip('\n')
                length = length + len(msg)
                ele_and = ele_and + msg.count('&')
                ele_per = ele_per + msg.count('%')
            print(ApkName + ": The frequency of '%' is ", float('%.4f' % (ele_per / length)))
            print(ApkName + ": The frequency of '&' is ", float('%.4f' % (ele_and / length)))
