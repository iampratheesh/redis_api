import redis
from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "7891628bb0b13ce0c676dfde280ba245"
redis_client = redis.Redis(host="localhost", port=6379, db=0)

from api_package import routes