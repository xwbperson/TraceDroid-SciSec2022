
### 根目录
| 文件名                          | 作用                                                                                |
|------------------------------|-----------------------------------------------------------------------------------|
| config.conf                  | 配置文件，如数据库相关信息、设备串号、检测参数、文件路径                                                      |
| DBUtils.py                   | 用于数据库连接和操作，包括了数据库连接权限验证、连接池对象的建立、数据库增删改查操作的实现，以及一些辅助函数                            |
| demo.py                      | 演示脚本，用于展示该项目的一些主要功能                                                               |
| DynamicGetUIXml.py           | 动态获取 Android 应用程序布局信息                                                             |
| EditDistance.py              | 编辑距离算法，计算映射表中的元素 ID 与实际字符串内容之间的编辑距离，确定哪些元素可以被合并                                   |
| ElementMappedToCharacter.py  | 生成映射表，将每个元素 ID 映射到字符串，并保存字符串的出现次数                                                 |
| GetNotMapElementFrequency.py | 用于辅助映射表的生成                                                                        |
| GetXmlInformation.py         | 从布局文件中提取元素信息并进行映射表的生成                                                             |
| hook.js                      | 在 Android 应用程序运行时通过 Frida 动态挂载获取其细节信息。该文件在 Detector.py 中被调用，用于在应用程序中动态检测敏感操作并进行记录 |
| init.py                      | 解析配置文件和初始化项目所需的各种对象、变量和设置                                                         |
| log.conf                     | 日志配置文件，用于配置日志的输出格式、等级和保存路径等                                                       |
| main.py                      | 调用其他文件中的函数并进行处理，对 Android 应用程序进行检测和分析                                             |
| ProcessXml.py                | 处理 Android 应用程序的 XML 布局文件                                                         |
| README.md                    | 项目的说明文档                                                                           |
| README2.md                   | 项目中各个文件的用途                                                                        |
| README_zh.md                 | 项目的说明文档中文版                                                                        |
| SimilarityCompareByUI.py     | 使用界面元素匹配算法比较两个应用程序在用户界面上的相似度                                                      |
| stack.conf                   | 配置文件，指定 Stack Tracer 匹配规则和筛选条件                                                    |
| subkill_test.py              | 测试脚本，用于测试 TraceDroid 的子模块 subkill 的功能                                             |
| tcs.py                       | 测试脚本，用于测试 TraceDroid 的测试用例选择模块 tcs 的功能                                            |
| test.py                      | 测试脚本，用于运行 TraceDroid 的大多数测试用例并输出结果                                                |
| testAlarm.py                 | 测试脚本，用于测试 TraceDroid 的跟踪引擎在处理 Android Alarm 相关事件时的功能                              |
| testAlarm2.py                | 测试脚本，用于测试 TraceDroid 的跟踪引擎在处理实时闹钟事件时的功能                                           |
| TestEngine.conf              | 配置文件，指定 TraceDroid 跟踪引擎的配置选项                                                      |
| UIElementFrequency.py        | 用于分析应用程序的 UI 元素在执行过程中的出现频率                                                        |

### Analyse
| 文件名                    | 作用                                                    |
|------------------------|-------------------------------------------------------|
| AnalyseLog.conf        | 日志的配置文件                                               |
| config.py              | 配置文件                                                  |
| DBUtils.py             | 封装了一些数据库操作                                            |
| host_ranking           | 主机评级引擎，用于识别依赖网络资源的行为，根据主机的 IP 地址和可靠性，评估其对应用程序安全的影响    |
| HostRanking.py         | 核心脚本，用于识别应用程序中使用的主机的 IP 地址，评估其可信度，并提供其 IP 地址的实时位置     |
| hostToLibraries.txt    | 映射主机到使用到的库文件的名称                                       |
| hostToPackageALL.txt   | 映射主机到所有已安装应用程序中使用的包名                                  |
| hostToPackageNew.txt   | 映射主机到新安装的应用程序中使用的包名                                   |
| hostToStcak.py         | 解析 TraceDroid 捕获的 Android 应用程序栈跟踪信息，并对栈跟踪进行处理和统计      |
| HTTP2Analyse.py        | 对 TraceDroid 生成的 HTTP2 流量数据进行分析                       |
| httpAnalyseTest.py     | 用于测试 HTTP 分析器的正则表达式和组件解析器                             |
| HTTPUpdate.py          | 解析应用程序的 HTTP 请求和响应，并将数据保存到数据库中来实现数据的持久化               |
| httpURLDecode.py       | 解码 HTTP 数据中的 URL 编码数据                                 |
| insertHTTPXDR.py       | 针对 UDP 流量，将 XDR 协议转换为 HTTP 协议，并将其插入到 TraceDroid 的数据库中 |
| LibAnalyse.py          | 对 Android 应用程序中使用的库文件进行分析                             |
| libRequestAnalyse.py   | 对 Android 应用程序中库的 HTTP 请求和响应进行分析                      |
| MergeHTTP.py           | 将多个 HTTP 请求和响应合并为一个请求和响应                              |
| packageNameUpdate.py   | 对应用程序包名称进行更新                                          |
| PIIAnalyse.py          | 对应用程序中可能泄露敏感信息的点进行分析                                  |
| postFileAnalyse.py     | 对应用程序的 POST 请求上传的文件进行分析                               |
| postFileTest.py        | 用于测试文件上传数据处理的一些方法                                     |
| sankeyCreate.py        | 生成 Sankey 图来展示主机和应用程序之间的 HTTP 交互                      |
| StackUpdate.py         | 用于更新应用程序的栈跟踪信息                                        |
| testInitHttpMessage.py | 用于测试 HTTP 报文解析器的初始化过程                                 |
| updateHTTPHost.py      | 针对应用程序的 HTTP 请求和响应，更新主机列表和应用程序与主机之间的关系                |
| updateHTTPStack.py     | 更新应用程序的栈跟踪信息和应用程序和主机之间的关系                             |

### experiment result
| 文件名                                                    | 作用                                             |
|--------------------------------------------------------|------------------------------------------------|
| domain category.csv                                    | 记录了经过主机 IP 地址分类之后，所有主机被分在了哪些 Internet 上的域名类别下面 |
| fiels checked manually transmitted out.xlsx            | 被手动检查过的从使用设备传输出的文件列表，以及一些有关这些文件的详细信息           |
| figure 6 & figure 7 data.xlsx                          | 记录了实验结果的数据，用于生成 TraceDroid 论文中的图表 6 和图表 7      |
| file names transmitted by each lib.csv                 | 记录了每个库文件上传的文件列表，以及一些有关这些文件的详细信息                |
| file sample.7z                                         | 一些实验的数据样本，以便让其他人可以验证实验结果                       |
| file type transmitted by lib.xlsx                      | 记录了每个库文件上传的文件类型，以及一些与文件类型相关的额外信息               |
| filename format group.csv                              | 根据文件名模式来对传输的文件进行分组，以便于更好地进行分类和分析               |
| gzAnalyseResult.csv                                    | 记录了通过对传输的文件进行分析而得到的一些关于 gzip 文件的统计数据和结果        |
| host-to-lib mappingtxt                                 | 记录了主机到使用到的库文件的名称之间的映射                          |
| lib-Host-mapping.txt                                   | 记录了库文件到使用它们的主机之间的映射关系                          |
| libraries verified manually.xlsx                       | 记录了手动验证过的库文件列表，以及这些库文件的详细信息                    |
| lib_list.txt                                           | 列出了 TraceDroid 目前使用的库文件列表                      |
| logAnalyseResult.csv                                   | 记录了通过对 TraceDroid 生成的日志进行分析而得到的一些统计数据和结果       |
| overview of files transmitted out from use device.xlsx | 记录了从使用设备上传的文件的概述信息，包括文件名、大小、类型等等               |
| request which can be replayde.log                      | 记录了可以被重放的 HTTP 请求的一些详细信息                       |
| txtAnalyseResult.csv                                   | 记录了通过对文本文件进行分析而得到的一些统计数据和结果                    |
| white list.txt                                         | 列出了白名单信息，用于过滤掉系统或者合法使用的网络活动，只关注不合法的网络活动        |
| zipAnalyseResult.csv                                   | 记录了通过对传输的 zip 文件进行分析而得到的一些关于 zip 文件的统计数据和结果    |
| figure data                                            | 存储了 TraceDroid 论文中所用到的一些实验数据，方便其他人进行验证和评估      |

### Graph
这些 Python 脚本用于处理实验结果数据，生成可视化的图表，以更直观、清晰地展示实验结果。图表可以提供给研究人员、开发者等进行分析、探索应用程序的行为以及其潜在的安全威胁。例如，通过 barAPPLib.py 脚本生成的条形图可以直观地显示出每个应用程序使用的库文件数量，从而帮助研究人员了解应用程序的构成和可能存在的安全问题；而 heatmapLibAPPCate.py 生成的热力地图则展示了库文件和应用程序类别之间的关系，可以更好地为研究人员提供应用程序风险评估和安全管理策略。

| 文件名                    | 作用                                  |
|------------------------|-------------------------------------|
| barAPPLib.py           | 生成了一个条形图，显示了每个应用程序使用的库文件数量          |
| barDomainLib.py        | 生成了一个条形图，分别显示了每个应用程序使用的主机数和库文件数     |
| boxplotCreate.py       | 生成了一个箱线图，是用来衡量每个应用程序上传和下载文件的数量的分布情况 |
| boxplotCreateHost.py   | 生成了一个箱线图，是用来衡量每个主机上传和下载文件的数量的分布情况   |
| heatmapLibAPPCate.py   | 生成了一个热力地图，显示了每个库文件和应用程序类别之间的关系      |

### PcapExtract
用于从抓包文件中提取应用程序的网络传输数据，主要适用于 Android 平台的应用程序，可以针对不同的网络传输协议进行提取，并将数据保存到数据库中以方便后续的分析和处理。使用 requestReplayTest.py 可以对从抓包文件中提取出的 HTTP 请求进行重放测试，以验证提取的网络传输数据的正确性。这些工具可以帮助研究人员更好地了解应用程序的通信行为，识别潜在的安全问题，从而提高应用程序的安全性和稳定性。

| 文件名                   | 作用                                |
|-----------------------|-----------------------------------|
| config.conf           | 配置文件，用于配置抓包文件的路径、提取数据的相关参数等       |
| DBUtils.py            | 用于操作数据库的 Python 类                 |
| ExtractLog.conf       | 配置文件，用于配置从抓包文件中提取数据的相关日志信息        |
| extractUtils.py       | 用于从 TCP/UDP/ICMP 流中提取应用程序网络传输数据   |
| PcapExtractEngine.py  | 从抓包文件中提取应用程序网络传输数据，整理并保存到数据库      |
| requestReplayTest.py  | 用于重放从抓包文件中提取的 HTTP 请求的 Python 脚本  |

### PIIAnalyse
这些 Python 脚本都用于分析应用程序中可能存在的 PII，例如电话号码、电子邮件、用户名、密码等敏感信息，为研究人员提供更深入的应用程序安全性分析。这些工具可以帮助研究人员更好地了解应用程序使用敏感信息的情况，识别潜在的风险，从而提高应用程序的安全性和隐私性。

| 用户名               | 作用                          |
|-------------------|-----------------------------|
| appLibAnalyse.py  | 分析应用程序所使用的库文件               |
| fileLibAPP.py     | 统计应用程序上传和下载文件               |
| libHostAPP.py     | 统计应用程序使用的主机数量和库文件数量         |
| PIICount.py       | 分析应用程序中出现的所有 PII 类型         |
| PIICountCross.py  | 分析应用程序中跨越多个网络协议的 PII 类型     |
| PIICountHost.py   | 统计每个主机上出现的 PII 类型           |
| PIICountHTTP.py   | 分析应用程序中 HTTP 请求中出现的 PII 类型  |
| PIICountHTTPS.py  | 分析应用程序中 HTTPS 请求中出现的 PII 类型 |
| PIIFileCount.py   | 统计应用程序上传和下载的文件中出现的 PII 类型   |
| PIILibAnalyse.py  | 分析应用程序中所使用的库文件中出现的 PII 类型   |
| PIILibAppCount.py | 统计应用程序中每个库文件出现 PII 类型       |
| postPackage.py    | 用于发送 HTTP POST 请求           |

### Spiders


| 文件名                     | 作用                            |
|-------------------------|-------------------------------|
| 360APPStoreAPKSpider.py | 从 360 应用商店上抓取应用程序 APK         |
| anzhiApkSpider.py       | 从安智市场上抓取应用程序 APK              |
| apk20ApkSpider.py       | 从 APK20 网站上抓取应用程序 APK         |
| apkpureAPKSpider.py     | 从 APKPure 网站上抓取应用程序 APK       |
| baiduAPKSpider.py       | 从百度应用市场上抓取应用程序 APK            |
| fdroidAPKSpider.py      | 从 F-Droid 应用市场上抓取应用程序 APK     |
| gamedogAPKSpider.py     | 从游戏狗应用市场上抓取应用程序 APK           |
| getjarAPKSpider.py      | 从 GetJar 应用市场上抓取应用程序 APK      |
| googleplayAPKSpider.py  | 从 Google Play 应用市场上抓取应用程序 APK |
| kuanAPKSpider.py        | 从酷安网上抓取应用程序 APK               |
| lenovoAPKSpider.py      | 从联想应用市场上抓取应用程序 APK            |
| liquAPKSpider.py        | 从力趣网上抓取应用程序 APK               |
| meizuApkSpider.py       | 从魅族应用市场上抓取应用程序 APK            |
| pconlineAPKSpider.py    | 从太平洋软件网上抓取应用程序 APK            |
| shafawangAPKSpider.py   | 从沙发网上抓取应用程序 APK               |
| slidemeAPKSpider.py     | 从 SlideME 应用市场上抓取应用程序 APK     |
| sougouAPKSpider.py      | 从搜狗应用市场上抓取应用程序 APK            |
| torrapkApkSpider.py     | 从 TORRENT APK 应用市场上抓取应用程序 APK |
| wandoujiaApkSpider.py   | 从豌豆荚应用市场上抓取应用程序 APK           |
| xiaomiAPPStoreSpider.py | 从小米应用商店上抓取应用程序 APK            |
| yingyongbaoAPKSpider.py | 从应用宝应用市场上抓取应用程序 APK           |
| yingyonghuiAPKSpider.py | 从应用汇应用市场上抓取应用程序 APK           |
| zolAPKSpider.py         | 从中关村在线网站上抓取应用程序 APK           |

### StackExtract


| 应用名               | 作用                                                                          |
|-------------------|-----------------------------------------------------------------------------|
| config.conf       | 配置应用程序的 Android SDK 路径、源代码路径、应用程序 APK 路径等信息的配置文件                            |
| DBUtils.py        | 提供数据库连接、数据插入、查询等功能                                                          |
| main.py           | Android 应用程序的函数调用信息和栈轨迹信息提取的主程序，主要使用了第三方库 frida 作为动态插桩工具，实现了对应用程序的函数调用信息的提取 |
| StackExtract.conf | 配置应用程序的包名、模块名、类名、函数名、参数、返回值等信息的配置文件                                         |


### testdir


| 文件名                  | 作用            |
|----------------------|---------------|
| testKillautotest.py  | 没什么作用，但有补全的代码 |









