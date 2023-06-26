import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class BaseConfig:
    """Base configuration."""

    BOT_TOKEN = os.environ.get("TOKEN")
    CHANNEL_ID = os.environ.get("CHANNEL_ID")


class DevelopmentConfig:
    """Development configuration."""

    Base = declarative_base()
    Session = sessionmaker()
    engine = create_engine("sqlite:///database.db?check_same_thread=False")

    search_url = (
        "https://auto.ria.com/uk/search/?indexName=auto,order_auto,"
        "newauto_search&categories.main.id=1&brand.id[0]=79&model.id[0]=2104"
        "&damage.not=0&country.import.usa.not=0&page=0"
    )

    caption = """🚘 <b><a href="{0}">{1}</a></b>
💸 <b>Ціна:</b> {2}
⚙️ <b>Пробіг:</b> {3}
📍 <i>{4}</i>"""

    new_price_text = """🚘 Ціна на авто <b><a href="{0}">{1}</a></b> змінилась!
💸 <b>Нова ціна:</b> {2}"""

    sold_car_text = """🚘 Авто <b><a href="{0}">{1}</a></b> було продано!"""


config = dict(base=BaseConfig, development=DevelopmentConfig)
