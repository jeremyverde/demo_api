from uuid import UUID, uuid4
from datetime import datetime
import json

from src.users.schemas import User
from src.orders.schemas import Order
from src.logger import logger

USERS = []
ORDERS = []


def load_data_from_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


user_table = load_data_from_json("src/data/users.json")
order_table = load_data_from_json("src/data/orders.json")


def load_users():
    global USERS
    USERS = [User(**user) for user in user_table]


def load_orders():
    global ORDERS
    ORDERS = [Order(**order) for order in order_table]


def init_db():
    load_users()
    load_orders()
    logger.info("loaded users and orders")
