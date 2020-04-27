Create Table itubuser(
 	u_id		CHAR(16) 	Primary Key,
	u_password 	varchar(16) 	not null,
 	u_name		CHAR(8) 		not null,
 	u_gender		TINYINT(1) 	not null,
 	u_age		DATE 		not null,
 	u_job 		VARCHAR(12) 	not null,
 	u_address		VARCHAR(108) 	not null,
 	u_phone		INT(11) 		not null
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

Create Table bath(
 	perfumenumber	INT(8) 	PRIMARY KEY,
 	perfume		CHAR(32) 	not null
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

Create Table custom(
 	c_number	 	INT(8),
 	u_id	CHAR(16) 	REFERENCES itubuser(u_id),
 	PRIMARY KEY(k_number, u_id),
 	perfum_ck	INT(1) 	not null,
 	perfumenumber	INT(8) 	 REFERENCES Bath(perfumenumber),
 	temperature	decimal(2) 	default null,
 	b_starttime	TIME 	default null,
 	b_time 		TIME 	default null
)ENGINE=InnoDB DEFAULT CHARSET=utf8;