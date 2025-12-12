# -*- coding: utf-8 -*-
# author: NhanDD3 <hp.duongducnhan@gmail.com>


import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from umongo.frameworks import MotorAsyncIOInstance


def new_umongo_instance(mongo_uri: str, db_name: str):
    """
    Create an instance of mongo db to register model
    mongo-uri example:
        "mongodb://user:pass@host01:port01,host02:port02,host03:port03/DbName?replicaSet=rs0&authSource=admin",


    Args:
        mongo_uri (str): MongoDb URI for connection.
        db_name (str): Name of the database will be used.

    Returns:
        MotorAsyncIOInstance: implementation for motor-asyncio
    """

    motor_client = AsyncIOMotorClient(mongo_uri)[db_name]
    motor_client.get_io_loop = asyncio.get_running_loop
    instance = MotorAsyncIOInstance(motor_client)
    return instance
