from environs import Env 

env = Env()
env.read_env()

FILE = env.str("FILE")
PASSWORD = env.str("PASSWORD")
SMTP_USERNAME = env.str("SMTP_USERNAME")
FROM = env.str("FROM")
TO = env.str("TO")