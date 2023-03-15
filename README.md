# 一个用于捕获和分析Android网络流量的框架
> Python 版本：Python 3.8

TraceDroid 是一个轻量级的 Android 流量收集和分析框架。TraceDroid Hook负责在 Android 框架层和本地层发送 HTTP/HTTPS 请求的关键函数，保存对应的调用栈、解析网络流量并恢复在流量中传输的文件。然后构建这三个组件（网络流量、调用栈和文件）之间的连接。

#### 依赖表

##### APKMetadata

| 字段名           | 类型           | 可空  | 键   | 默认值           | 备注           |
| ---------------- | -------------- | ----- | ---- | ----------------- | -------------- |
| APKID            | bigint(20)     | NO    | PRI  |                   | 自增长主键     |
| APPName          | varchar(1024)  | NO    |      |                   | 应用程序名称   |
| APKName          | varchar(1024)  | NO    |      |                   | APK 文件名称   |
| APKFilePath      | varchar(1024)  | NO    |      |                   | APK 文件路径   |
| APKStoreName     | varchar(1024)  | NO    |      |                   | APK 存储名称   |
| createTime       | datetime       | NO    |      | CURRENT_TIMESTAMP | 创建时间       |
| lastModifiedTime | datetime       | NO    |      |                   | 最后修改时间   |
| needAnalyse      | int(11)        | NO    |      | 1                 | 是否需要分析   |

##### CaptureLog

| 字段名         | 类型           | 可空  | 键   | 默认值           | 备注           |
| ------------- | -------------- | ----- | ---- | ----------------- | -------------- |
| logID         | bigint(20)     | NO    | PRI  |                   | 自增长主键     |
| APKID         | varchar(1024)  | NO    |      |                   | APK ID         |
| APKName       | varchar(1024)  | NO    |      |                   | APK 文件名称   |
| APPName       | varchar(1024)  | NO    |      |                   | 应用程序名称   |
| createTime    | datetime       | NO    |      | CURRENT_TIMESTAMP | 创建时间       |
| pcapFilePath  | varchar(1024)  | NO    |      |                   | pcap 文件路径  |
| stackFilePath | varchar(1024)  | NO    |      |                   | 调用栈文件路径 |
| needExtract   | int(11)        | NO    |      |                   | 是否需要提取   |
| extractTime   | datetime       | NO    |      |                   | 提取时间       |

##### PreProcessLog

| 字段名       | 类型           | 可空  | 键   | 默认值           | 备注           |
| ----------- | -------------- | ----- | ---- | ----------------- | -------------- |
| logID       | bigint(20)     | NO    | PRI  |                   | 自增长主键     |
| APKID       | bigint(20)     | NO    |      |                   | APK ID         |
| APKName     | varchar(1024)  | NO    |      |                   | APK 文件名称   |
| APPName     | varchar(1024)  | NO    |      |                   | 应用程序名称   |
| processTime | datetime       | NO    |      | CURRENT_TIMESTAMP | 处理时间       |

##### HTTP

| 字段名           | 类型                | 可空  | 键   | 默认值 | 备注                                      |
|----------------|-------------------|------|-------|-------|-------------------------------------------|
| id             | bigint(20) unsigned | NO   | PRI   | None   | 自增长主键                                |
| packageName    | varchar(1024)       | YES  |       |       | 应用程序包名                              |
| srcAddr        | varchar(1024)       | YES  |       |       | 源地址                                    |
| srcPort        | int(11)             | YES  |       | None  | 源端口                                    |
| dstAddr        | varchar(1024)       | YES  |       |       | 目的地址                                  |
| dstPort        | int(11)             | YES  |       | None  | 目的端口                                  |
| host           | varchar(1024)       | YES  |       |       | 请求的主机名                              |
| URL            | varchar(1024)       | YES  |       |       | 请求的 URL 地址                           |
| requestTime    | timestamp           | YES  |       | None  | 请求时间                                  |
| requestHeaders | varchar(1024)       | YES  |       |       | 请求头                                    |
| requestBody    | varchar(1024)       | YES  |       |       | 请求体                                    |
| responseHeaders| varchar(1024)       | YES  |       |       | 响应头                                    |
| responseBody   | varchar(1024)       | YES  |       |       | 响应体                                    |
| protocol       | varchar(1024)       | YES  |       |       | 请求协议（HTTP/HTTPS）                    |
| method         | varchar(1024)       | YES  |       |       | 请求方法（GET/POST）                      |
| content-type   | varchar(1024)       | YES  |       |       | 响应体的 content-type（例如，text/html） |
