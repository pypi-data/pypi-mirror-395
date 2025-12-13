import site
import time

from pingintel_api.utils import raise_for_status

site.addsitedir("../src")

""" This example script will page through all activity, starting from the most recent. """

from pingintel_api import SOVFixerAPIClient

api_client = SOVFixerAPIClient(environment="prod")
api_client = SOVFixerAPIClient(environment="prod", auth_token="e52b05812466fe22b2437458c0ea4056bdf467da")

next_cursor_id = None
# next_cursor_id = "s-ma-ping-vjcgkd-r001"
page_size = 1
# page_size = 200

filename = f"sovfixer_list_history_ping_{next_cursor_id}_{page_size}_run2.csv"
# next_cursor_id = "s-no-rsu-ymndbj-r027"
# next_cursor_id = "s-is-ping-23y22j"
cnt = 0
# f = None
f = open(filename, "w", encoding="utf-8")
while True:

    url = api_client.api_url + "/api/v1/sov/history"
    # 20230101130000
    parameters = {"cursor_id": next_cursor_id, "page_size": page_size, "start": "20250601130000"}
    response = api_client.get(url, params=parameters)
    raise_for_status(response)
    response = response.json()

    next_cursor_id = response.get("cursor_id")

    if len(response["results"]) == 0:
        break
    for activity in response["results"]:
        cnt += 1

        if f:
            f.write(f"{cnt},{activity['id']},{activity['record_type']},{activity['completed_time']}\n")
        else:
            print(f"{cnt}: {activity['id']}: {activity['record_type']} {activity['completed_time']}")

    # time.sleep(0.05)
    # break
    if cnt > 100:
        break
    if f:
        print(f"Processed {cnt} activities, next cursor_id: {next_cursor_id}")
        f.flush()

if f:
    f.close()
    print(f"Finished writing {cnt} activities to {filename}")
