# API with Redis Caching

This is an API built using Flask and data is cached using Redis

This API is deployed on AWS and has four endpoints

Python Script `store_latest_data.py` parses the CSV file and stores the latest data of device against Device ID in Redis

## API Reference

#### Get Raw Data

```http
  GET http://ec2-3-110-225-0.ap-south-1.compute.amazonaws.com/get_raw_data
```
Retrieves the raw data from file and converts to JSON

No Caching

#### Get Latest Information

```http
  GET http://ec2-3-110-225-0.ap-south-1.compute.amazonaws.com/get_latest_info/25029
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `device_fk_id`      | `int` | **Required**. Device Id to fetch latest information |


Gets the latest information of the device id provided

Data is cached with no expiry

#### Get the Start and End Location

```http
  GET http://ec2-3-110-225-0.ap-south-1.compute.amazonaws.com/get_start_end_location/25029
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `device_fk_id`      | `int` | **Required**. Device Id to fetch the start and end location |


Gets the start and end location of provided device id

Data is cached for 5 minutes since last API call for the device id

#### Get All the Locations

```http
  GET http://ec2-3-110-225-0.ap-south-1.compute.amazonaws.com/get_all_locations/25029/2021-10-23T12:30:03Z/2021-10-23T12:30:04Z
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `device_fk_id`      | `int` | **Required**. Device Id to fetch all locations |
| `start_time`      | `int` | **Required**. Start time required for filtering the location list |
| `end_time`      | `int` | **Required**. End time required for filtering the location list |


Gets all the locations along with the timestamp of provided device id with start time and end time

Data is cached for 5 minutes since the last API call for the device id, start time, end time combination

## Deployment

This project is deployed on AWS by creating an EC2 instance of Linux Ubuntu.

The project was cloned from the main branch into the instance, created venv and installed required libraries from requirements.txt.

Used nginx, gunicorn and supervisor for deployment.


## Screenshots

### Latest Info (Always Cached)
![Latest Info (Always Cached)](/screens/get_latest_info.png)

### Get Start End Location (Cache Miss)
![Get Start End Location (Cache Miss)](/screens/get_start_end_location_cache_miss.png)

### Get Start End Location (Cache Hit)
![Get Start End Location (Cache Hit)](/screens/get_start_end_location_cache_hit.png)

### Get All Locations (Cache Miss)
![Get All Locations (Cache Miss)](/screens/get_all_location_cache_miss.png)

### Get All Locations (Cache Hit)
![Get All Locations (Cache Hit)](/screens/get_all_location_cache_hit.png)

### Latest Info (Redis Cache Keys)
![Latest Info (Redis Cache Keys)](/screens/latest_info_redis_cache_keys.png)

### Temporary Cache (Expires after 5 mins)
![Temporary Cache (Expires after 5 mins)](/screens/temporary_cache.png)


