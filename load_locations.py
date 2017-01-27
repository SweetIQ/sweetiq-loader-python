#!/usr/bin/env python3
import config
import threading
import sys
import requests
from sweetiq import load_sql
from sweetiq import location_api


def push_data():
    print('starting..')
    locations = load_sql.get_data_from_sql()
    print('pushing ' + str(len(locations)) + ' locations')
    login_data = location_api.login(config.api_email, config.api_password)
    push_response = location_api.push(login_data['id'], {'locations': locations})

    print(push_response.json())

    "if restart_interval is set, we will call ourselves again in 'restart_interval' minutes"
    if config.restart_interval != 0:
        timer = threading.Timer(config.restart_interval * 60, push_data)
        timer.start()

if 'test' in sys.argv:
    print('testing connection')
    try:
        login_data = location_api.login(config.api_email, config.api_password)
        if 'id' in login_data:
            print('connection successful')
        else:
            print('error: ', login_data)
    except Exception as err:
        print(err)
else:
    push_data()
