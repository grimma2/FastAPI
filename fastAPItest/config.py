import sqlalchemy
import databases
from starlette.templating import Jinja2Templates
from fastapi import FastAPI
from ormar import ModelMeta


app = FastAPI()
metadata = sqlalchemy.MetaData()
database = databases.Database('sqlite:///test.db')
engine = sqlalchemy.create_engine('sqlite:///test.db')
templates = Jinja2Templates(directory='templates')


class MainMeta(ModelMeta):
    metadata = metadata
    database = database
