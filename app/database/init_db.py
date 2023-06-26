from config import config
from app.models.car_model import CarsModel


dev_config = config.get("development")
session = dev_config.Session(bind=dev_config.engine)


class DataController:
    def add_new_car(self, message_id, title, price, url):
        new_car = CarsModel(
            message_id=message_id,
            title=title,
            price=price,
            url=url,
        )
        session.add(new_car)
        session.commit()

    def get_car_by(self, param, value):
        column = getattr(CarsModel, param)
        return session.query(CarsModel).filter(column == value).first()

    def edit_car_price(self, message_id, value):
        car = session.query(CarsModel).filter_by(message_id=message_id).first()
        car.price = value
        session.commit()

    def get_all_cars(self):
        return session.query(CarsModel).all()

    def delete_car(self, message_id):
        session.query(CarsModel).filter_by(message_id=message_id).delete()
        session.commit()
