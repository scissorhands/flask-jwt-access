def build_dsn(host, user, password, database):
	return 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(user,password,host,database)