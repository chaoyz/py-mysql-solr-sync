# coding:utf8

# mysql connect set
'''
host: mysql host
port: mysql connect port default 3306
user: mysql connect login name
password: mysql connect login password
charset: mysql connect charset default utf8
db: database name
'''
mysql_config = {"host":"127.0.0.1", "port":3306, "user":"root", "passwd":"123456", "charset": 'utf8', "db":"test"}

# sync table name
'''
table: the table we want sync row data.
'''
table = "test"

# local service is a slave, need specify a slave server id.
mysql_server_id = 111

# binlog record
'''
mysql_binlog_info_file: binlog file name.
'''
mysql_binlog_info_file = "mysql-bin.log"

# solr
'''
schema: http or https
host: solr host
port: solr port 
path: connect url path, solr core path
'''
solr_config = {"schema":"http", "host":"127.0.0.1", "port":8081, "path":"/solr/core0"}

# log file
file_path = "logger.log"

# mysql columns map solr fields, "mysql colum":"solr field".
mysql_column_solr_index_mapping = {
    "id":"id",
    "name":"name"
}
