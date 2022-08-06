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