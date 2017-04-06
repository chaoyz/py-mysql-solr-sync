# coding:utf8

mysql_config = {"host":"127.0.0.1", "port":3306, "user":"ekpapi", "passwd":"ekpapi", "charset": 'utf8', "db":"xserver"}

table = "test"

mysql_server_id = 1

mysql_binlog_info_file = "binlog_record.log"

solr_config = {"schema":"http", "host":"127.0.0.1", "port":8081, "path":"/solr/core0"}

file_path = "logger.log"

mysql_column_solr_index_mapping = {
    "id":"id",
    "name":"name"
}
