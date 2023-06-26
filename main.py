import time

import requests
from telebot import TeleBot, types
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from config import config
from init_db import DataController


dev_config = config.get("development")
base_config = config.get("base")

# Create a database table
dev_config.Base.metadata.create_all(dev_config.engine)


class Scraper:
    def __init__(self) -> None:
        self.bot = TeleBot(base_config.BOT_TOKEN)
        self.ua = UserAgent()
        self.db = DataController()

    def start(self):
        print("Started...")

        while True:
            # Make a response by search url
            response1 = requests.get(
                dev_config.search_url, headers={"user-agent": self.ua.random}
            )
            soup = BeautifulSoup(response1.content, "html.parser")

            sections = soup.find_all("section", class_="ticket-item")

            # List of url from the website
            car_urls = [
                s.find("div", class_="ticket-title").find("a").get("href")
                for s in sections
            ]

            # Check if car was sold
            # Go through the database of all cars
            for _car in self.db.get_all_cars():
                # Check whether the url of this car is not in the list of urls from the website
                if _car.url not in car_urls:
                    self.bot.send_message(
                        base_config.CHANNEL_ID,
                        dev_config.sold_car_text.format(_car.url, _car.title),
                        parse_mode="html",
                        reply_to_message_id=_car.message_id,
                        disable_web_page_preview=True,
                    )

                    # Delete this car by message_id in telegram channel from database
                    self.db.delete_car(_car.message_id)

            # Go through the database of all cars on the website
            for section in sections:
                media_group = []

                car_url = (
                    section.find("div", class_="ticket-title").find("a").get("href")
                )

                # Get car by url from database
                car = self.db.get_car_by("url", car_url)

                price = (
                    section.find("div", class_="price-ticket").text.split("   ")[1]
                    + " $"
                )

                # Formatting string "price" to int to compare with the price in the database
                formatted_price = int(price.split(" $")[0].replace(" ", ""))

                # If car by url not in our database
                if not car:
                    title = section.find("div", class_="ticket-title").text.strip()
                    mileage = (
                        section.find("div", class_="definition-data")
                        .find("ul")
                        .find("li")
                        .text
                    )
                    location = (
                        section.find("div", class_="definition-data")
                        .find("ul")
                        .find("li", class_="view-location")
                        .text.strip()
                        .split(" ")[0]
                    )

                    # Make a new response to take a some photos of car
                    response2 = requests.get(
                        car_url, headers={"user-agent": self.ua.random}
                    )
                    soup2 = BeautifulSoup(response2.content, "html.parser")

                    photo_urls = [
                        soup2.find("div", class_="carousel-inner")
                        .find_all("div")[i]
                        .find("img")
                        .get("src")
                        for i in range(3)
                    ]

                    for i, url in enumerate(photo_urls):
                        if i == 0:
                            # Add caption to the first photo
                            media_group.append(
                                types.InputMediaPhoto(
                                    media=url,
                                    caption=dev_config.caption.format(
                                        car_url, title, price, mileage, location
                                    ),
                                    parse_mode="html",
                                )
                            )
                        else:
                            media_group.append(
                                types.InputMediaPhoto(media=url, parse_mode="html")
                            )

                    # Send the media group
                    msg = self.bot.send_media_group(
                        chat_id=base_config.CHANNEL_ID, media=media_group
                    )

                    # Add new car to our database
                    self.db.add_new_car(
                        msg[0].id,
                        title,
                        formatted_price,
                        car_url,
                    )

                # If car price was edited on web site
                elif car.price != formatted_price:
                    # Edit car price in our database
                    self.db.edit_car_price(car.message_id, formatted_price)

                    self.bot.send_message(
                        base_config.CHANNEL_ID,
                        dev_config.new_price_text.format(
                            car_url, car.title, formatted_price
                        ),
                        parse_mode="html",
                        reply_to_message_id=car.message_id,
                        disable_web_page_preview=True,
                    )

            time.sleep(600)


scraper = Scraper()
scraper.start()
