import numpy as np


# 计算两个字符串之间的编辑距离
# 通过动态规划的思想，计算删除、插入、替换
# 三种操作将第一个字符串转换成第二个字符串需要的最小操作次数，即编辑距离
# dp数组表示状态转移表，其中dp[i][j]表示字符串word1的前i个字符到字符串word2的前j个字符的编辑距离
# 最后返回dp[len1][len2]，即字符串word1转换成字符串word2需要的最小操作次数
def editDistance(word1, word2):
    len1 = len(word1)
    len2 = len(word2)
    dp = np.zeros((len1 + 1, len2 + 1))
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            delta = 0 if word1[i - 1] == word2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j - 1] + delta, min(dp[i - 1][j] + 1, dp[i][j - 1] + 1))
    return dp[len1][len2]


# 根据编辑距离计算相似度
# 计算编辑距离ed与两个字符串长度的最大值之间的比值，再用1减去这个比值，即可得到相似度
# 相似度的取值范围为0到1，值越大表示两个字符串越相似
def editDistanceSimilarity(word1, word2):
    ed = editDistance(word1, word2)
    return 1 - (ed / max(len(word1), len(word2)))
# 以上两个函数对于文本处理、字符串匹配、信息检索等领域都有着广泛的应用
