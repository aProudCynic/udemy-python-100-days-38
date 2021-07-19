import json
from datetime import datetime

import requests as requests

from secrets import (
    NUTRONIX_ID,
    NUTRONIX_KEY,
    PERSONAL_DATA,
)

from constants import (
    NUTRONIX_EXERCISE_ENDPOINT,
    SHEETY_ADD_RECORD_ENDPOINT,
)


def _fetch_workouts_from(text):
    headers = {
        "x-app-id": NUTRONIX_ID,
        "x-app-key": NUTRONIX_KEY,
        "Content-Type": "application/json",
    }
    query_data = {
        "query": text,

    }
    unified_data = {**query_data, **PERSONAL_DATA}
    json_data = json.dumps(unified_data)
    response = requests.post(data=json_data, headers=headers, url=NUTRONIX_EXERCISE_ENDPOINT)
    response.raise_for_status()
    response_data = json.loads(response.content)
    return response_data


def _map_to_workout_data(workouts):
    return [
        {
            "date": datetime.today().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "exercise": workout["name"],
            "duration": workout["duration_min"],
            "calories": workout["nf_calories"],
        } for workout in workouts
    ]


def extract_workout_data_from(text):
    response_data = _fetch_workouts_from(text)
    return _map_to_workout_data(response_data['exercises'])


def persist(workout_data):
    for workout in workout_data:
        response = requests.post(data=json.dumps(workout), url=SHEETY_ADD_RECORD_ENDPOINT)
        print(f"Saving workout {workout['exercise']} {'succeeded' if response.status_code == 200 else 'failed'}")


workout_text = input("Please write about your exercise: ")
workout_data = extract_workout_data_from(workout_text)
persist(workout_data)

