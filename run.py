from config import config
from app import Scraper


dev_config = config.get("development")

# Create a database table
dev_config.Base.metadata.create_all(dev_config.engine)

scraper = Scraper()
scraper.start()