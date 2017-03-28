# coding:utf8

mysql_config = {"host":"127.0.0.1", "port":3306, "user":"ekpapi", "password":"ekpapi", "database":"xserver", "tables":["test"]}

solr_config = {"schema":"http", "host":"127.0.0.1", "port":8081, "path":"/solr/fileindex"}

file_path = "./logger.log"

solr_index_mysql_key_mapping = {
    "name":"test.name",
    "id":"test.id",
    "order":"test.order"
}
