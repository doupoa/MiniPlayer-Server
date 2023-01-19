from logging import INFO, WARN, DEBUG,ERROR

# Global configuration. All configurations should be modified here

# Database related configuration
db_host = '127.0.0.1'
db_port = 3306
db_user = 'root'
db_pwd = '123456'
db_database = 'miniplayer'

#Logging related configuration
LOGGING_LEVEL = DEBUG
LOG_PATH = "api.log"
LOG_SIZE = 100*1024  #Bytes

# Security related configuration
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 2
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "test123" # RSA
ALGORITHM= 'HS256'

# register
AllowRegistration = True

# Login
AllowLogin = True
