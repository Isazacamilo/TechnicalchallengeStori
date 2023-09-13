from environs import Env 

env = Env()
env.read_env()

RECIPIENT = env.str("RECIPIENT")
FILE = env.str("FILE")
LOGO = env.str("LOGO")
PASSWORD = env.str("PASSWORD")
SMTP_USERNAME = env.str("SMTP_USERNAME")
FROM = env.str("FROM")
TO = env.str("TO")
DB_URL = env.str("DB_URL", None)
