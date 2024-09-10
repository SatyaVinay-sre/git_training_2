CREATE USER IF NOT EXISTS 'replicator'@'%' IDENTIFIED WITH mysql_native_password BY 'wiley123';
GRANT REPLICATION SLAVE ON *.* TO 'replicator'@'%';
