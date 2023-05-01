from environs import Env

env = Env()
env.read_env()

ADMINS = env.list("ADMINS")
BOT_TOKEN = env.str("BOT_TOKEN")
IP = env.str("IP")
branches = (
    (41.329181, 69.336226),  # 1-filial
    (41.327364, 69.345305),  # 2-filial
    (41.337543, 69.335965)   # 3-filial
)
