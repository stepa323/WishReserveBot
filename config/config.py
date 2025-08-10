from dataclasses import dataclass
from environs import Env
from typing import List, Optional

@dataclass
class DbConfig:
    url: str
    echo: bool = False  # SQL query logging

@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    use_redis: bool = False

@dataclass
class Config:
    bot: TgBot
    db: DbConfig

def load_config(path: Optional[str] = None) -> Config:
    env = Env()
    env.read_env(path, override=True)

    return Config(
        bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMIN_IDS"))),
            use_redis=env.bool("USE_REDIS", False)
        ),
        db=DbConfig(
            url=env.str("DB_URL", "sqlite+aiosqlite:///database.db"),
            echo=env.bool("DB_ECHO", False)
        )
    )
