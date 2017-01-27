import pymysql

"your SweetIQ provided authentication information"
api_email = 'email'
api_password = 'password'


"""the db object is the connection to your database.
   This is a Mysql example but you can use any driver for any
   database.
"""
db = pymysql.connect(host='localhost',
                     user='user',
                     passwd="password",
                     db="database")



"""This is the interval of time in minutes between two pushes.
   Use '0' to kill the process after the data is sent (Not Recommended)
"""
restart_interval = 60
