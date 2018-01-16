# coding:utf8

# mysql
mysql_config = {"host":"127.0.0.1", "port":3306, "user":"root", "passwd":"123456", "charset": 'utf8', "db":"test"}

# mysql table name
table = "test"

# local service is a slave, need specify a slave server id.
mysql_server_id = 1

# binlog record
mysql_binlog_info_file = "binlog_record.log"

# solr
solr_config = {"schema":"http", "host":"127.0.0.1", "port":8081, "path":"/solr/core0"}

# log file
file_path = "logger.log"

# mysql columns map solr fields
mysql_column_solr_index_mapping = {
    "id":"id",
    "name":"name"
}
