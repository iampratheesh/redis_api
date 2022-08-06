import json
import os
import pandas as pd
from flask import jsonify
from api_package import app, redis_client

@app.route("/get_latest_info/<int:device_id>")
def get_latest_info(device_id):
    info = redis_client.get(device_id)
    if info is  None:
        print("Cache Miss")
        df = pd.read_csv(os.path.join(app.root_path, "data/raw_data.csv"))
        df = df.sort_values('sts')
        df = df.groupby('device_fk_id', as_index=False).last()
        df = df.loc[df['device_fk_id'] == int(device_id)].squeeze()
        row = df.to_dict()
        device_id = row.pop('device_fk_id')
        info = row
        redis_client.set(device_id, json.dumps(row))
    else:
        print("Cache Hit")
        info = json.loads(info)
        print(info)
    return jsonify(info)


@app.route("/get_start_end_location/<int:device_id>")
def get_start_end_location(device_id):
    info = redis_client.get(str(device_id) + "_location")
    if info is  None:
        print("Cache Miss")
        df = pd.read_csv(os.path.join(app.root_path, "data/raw_data.csv"))
        df = df.sort_values('sts')
        df_last = df.groupby('device_fk_id', as_index=False).last()
        df_last = df_last.loc[df_last['device_fk_id'] == int(device_id)].squeeze()
        row_last = df_last.to_dict()
        df_first = df.groupby('device_fk_id', as_index=False).first()
        df_first = df_first.loc[df_first['device_fk_id'] == int(device_id)].squeeze()
        row_first = df_first.to_dict()
        device_id = row_first.pop('device_fk_id')
        info = {
            "start_location": (row_first.pop('latitude'),row_first.pop('longitude')),
            "end_location": (row_last.pop('latitude'),row_last.pop('longitude'))
        }
        redis_client.set(str(device_id) + "_location", json.dumps(info))
    else:
        print("Cache Hit")
        info = json.loads(info)
    return jsonify(info)