import json
import redis
import pandas as pd


def parse_and_cache_data():
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    data = pd.read_csv("api_package/data/raw_data.csv")
    data = data.sort_values('sts')
    for _, series in data.iterrows():
        row = series.to_dict()
        device_id = row.pop('device_fk_id')
        redis_client.set(device_id, json.dumps(row))


if __name__ == "__main__":
    parse_and_cache_data()