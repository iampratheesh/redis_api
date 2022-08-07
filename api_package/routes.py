import json
import os
from datetime import timedelta
import pandas as pd
from flask import jsonify
from api_package import app, redis_client


@app.route("/get_latest_info/<int:device_id>")
def get_latest_info(device_id):
    """Gets the latest information of the device id provided

    Args:
        device_id (int): Device ID required to fetch the latest information

    Returns:
        JSON object: Contains latest latitude, longitude, time_stamp, sts and speed
    """
    info = redis_client.get(device_id)
    if info is None:
        print("Cache Miss")
        df = pd.read_csv(os.path.join(app.root_path, "data/raw_data.csv"))
        df = df.sort_values("sts")
        df = df.groupby("device_fk_id", as_index=False).last()
        df = df.loc[df["device_fk_id"] == int(device_id)].squeeze()
        row = df.to_dict()
        device_id = row.pop("device_fk_id")
        info = row
        redis_client.set(device_id, json.dumps(row))
    else:
        print("Cache Hit")
        info = json.loads(info)
        print(info)
    return jsonify(info)


@app.route("/get_start_end_location/<int:device_id>")
def get_start_end_location(device_id):
    """Gets the start and end location of provided device id

    Args:
        device_id (int): Device ID required to fetch the start and end location

    Returns:
        JSON object: Contains the start and end location in (latitude, longitude) pairs
    """
    info = redis_client.get(str(device_id) + "_location")
    if info is None:
        print("Cache Miss")
        df = pd.read_csv(os.path.join(app.root_path, "data/raw_data.csv"))
        df = df.sort_values("sts")
        df_last = df.groupby("device_fk_id", as_index=False).last()
        df_last = df_last.loc[df_last["device_fk_id"] == int(device_id)].squeeze()
        row_last = df_last.to_dict()
        df_first = df.groupby("device_fk_id", as_index=False).first()
        df_first = df_first.loc[df_first["device_fk_id"] == int(device_id)].squeeze()
        row_first = df_first.to_dict()
        device_id = row_first.pop("device_fk_id")
        info = {
            "start_location": (row_first.pop("latitude"), row_first.pop("longitude")),
            "end_location": (row_last.pop("latitude"), row_last.pop("longitude")),
        }
        redis_client.set(str(device_id) + "_location", json.dumps(info))
        redis_client.expire(str(device_id) + "_location", timedelta(minutes=5))
    else:
        print("Cache Hit")
        info = json.loads(info)
    return jsonify(info)


@app.route("/get_all_locations/<int:device_id>/<string:start_time>/<string:end_time>")
def get_all_locations(device_id, start_time, end_time):
    """Gets all the locations along with the timestamp of provided device id with start time and end time

    Args:
        device_id (int): Device ID required to fetc required locations
        start_time (string): Start time required for filtering the location list
        end_time (string): End time required for filtering the location list

    Returns:
        JSON object: Contains the list of locations along with the timestamp based to the parameters provided
    """
    print(device_id, start_time, end_time)
    info = redis_client.get(str(device_id) + start_time + end_time)
    if info is None:
        print("Cache Miss")
        df = pd.read_csv(os.path.join(app.root_path, "data/raw_data.csv"))
        df = df.sort_values("sts")
        df = df.loc[
            (df["device_fk_id"] == device_id)
            & (df["time_stamp"] >= start_time)
            & (df["time_stamp"] <= end_time)
        ].drop(columns=["device_fk_id", "sts", "speed"])
        info = {"location_points": df.values.tolist()}
        if not df.empty:
            redis_client.set(str(device_id) + start_time + end_time, json.dumps(info))
            redis_client.expire(
                str(device_id) + start_time + end_time, timedelta(minutes=5)
            )
    else:
        print("Cache Hit")
        info = json.loads(info)
    return jsonify(info)
