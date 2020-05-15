Create Table user_db(
	s_num INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	s_date DATE NOT NULL,
	s_age INT NOT NULL,
	s_gender INT NOT NULL,
    s_temperature INT NOT NULL,
    s_start INT NOT NULL,
    s_during INT NOT NULL,
    s_end INT NOT NULL,
    s_perfume CHAR(32) NOT NULL,
	s_job VARCHAR(80) NOT NULL,
    s_weather INT NOT NULL
);