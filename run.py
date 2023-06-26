from config import config
from app import ScraperApp


dev_config = config.get("development")

# Create a database table
dev_config.Base.metadata.create_all(dev_config.engine)

app = ScraperApp()
app.start()