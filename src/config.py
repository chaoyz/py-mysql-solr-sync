# coding:utf8

mysql_config = {"host":"192.168.1.241", "port":3306, "user":"ekpapi", "passwd":"ekpapi", "charset": 'utf8', "db":"xserver"}

table = "file"

solr_config = {"schema":"http", "host":"127.0.0.1", "port":8081, "path":"/solr/fileindex"}

file_path = "./logger.log"

mysql_column_solr_index_mapping = {
    "fid":"fid",
    "name":"name"
}
