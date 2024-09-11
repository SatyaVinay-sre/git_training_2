CREATE USER 'exporter'@'%' IDENTIFIED BY 'wiley123';
GRANT PROCESS, REPLICATION CLIENT ON *.* TO 'exporter'@'%';
GRANT SELECT ON *.* TO 'exporter'@'%';
CREATE USER 'replicator'@'%' IDENTIFIED BY 'wiley123';
GRANT REPLICATION SLAVE ON *.* TO 'replicator'@'%';
