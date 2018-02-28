# py-mysql-solr-sync
同步mysql表数据到solr小工具

# 介绍
同步工具模拟mysql主从复制机制，使用mysql-replication库读取binlog文件获取数据库变更，将变更信息同步到solr索引中，项目使用python2.7开发.

# 使用方法
## 安装依赖
进入项目目录执行make，安装python依赖，或者执行pip install -r requirements.txt安装依赖。

## 配置
### 启用mysql binlog功能
需要开启mysql中binlog功能记录，这里以centos为例:
1. 安装好mysql后找到mysql启动配置文件，一般为/etc/my.cnf
2. 保证配置文件中至少有如下几行
```
log-bin=mysql-bin  # 开启mysql的binlog
server-id=222  # mysql server的id，不能与其他的重复，222的位置随意更换
```
### 修改config.py配置文件
打开配置文件按照注释修改config.py文件

##执行
进入项目目录执行：
```
sh run.sh start
```

