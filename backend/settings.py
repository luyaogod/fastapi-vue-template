#DATABASES
TORTOISE_ORM = {
        'connections': {
            'default': {
                'engine': 'tortoise.backends.mysql',
                'credentials': {
                    'host': '127.0.0.1',
                    'port': '3306',
                    'user': 'root',
                    'password': 'maluyao123',
                    'database': 'fastapi-vue-template',
                }
            },
        },
        'apps': {
            'models': {
                #aerich配置
                'models': ['models.models','aerich.models'],
                'default_connection': 'default',
            }
        }
    }

#JWT配置
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#跨域
ALLOWHOSTS = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
]