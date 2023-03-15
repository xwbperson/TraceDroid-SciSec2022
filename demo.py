import xml.etree.ElementTree as ET
import time
import subprocess

'''
主要用于解析 Android 应用程序的 UI 层级结构
通过调用 xml.etree.ElementTree 模块的相关函数来解析 XML 格式的 UI 层级结构文件
遍历所有的节点，将节点的标签（tag）和深度（level）信息存储到 result_list 变量中
该变量可以在遍历完整个节点树之后返回
剔除了某些属性为“invisible”或“gone”的节点
这些节点在 UI 展示时不可见，因此无需纳入到 UI 层级结构中
'''


# 遍历所有的节点
def walkData(root_node, level, result_list):
    key = '{http://schemas.android.com/apk/res/android}visibility'
    if root_node.attrib.__contains__(key) and (
            root_node.attrib[key] == 'invisible' or root_node.attrib[key] == 'gone'):
        return
    temp_list = [level, root_node.tag]
    result_list.append(temp_list)

    # 遍历每个子节点
    children_node = root_node.iter()
    if len(children_node) == 0:
        return
    for child in children_node:
        walkData(child, level + 1, result_list)
    return


# 实现对节点的遍历，并返回遍历结果
def getXmlData(file_name):
    level = 1  # 节点的深度从1开始
    result_list = []
    root = ET.parse(file_name).getroot()
    walkData(root, level, result_list)
    return result_list


if __name__ == "__main__":
    strs = "adaaaadedacd"
    print(strs.count('a'), 1, 2)
