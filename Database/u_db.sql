CREATE TABLE u_db (
	u_num INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	u_name VARCHAR(80) NOT NULL,
	u_age INT(11) NOT NULL,
	u_gender INT(11) NOT NULL,
	u_job VARCHAR(80) NOT NULL,
    	u_bathing INT(10) NOT NULL DEFAULT '0',
    	u_water INT(10) NOT NULL DEFAULT '0',
    	u_temperature INT(10) NOT NULL DEFAULT '0',
    	u_time INT(10) NOT NULL DEFAULT '0',
    	u_last TINYINT(1) NOT NULL DEFAULT '0'
);
