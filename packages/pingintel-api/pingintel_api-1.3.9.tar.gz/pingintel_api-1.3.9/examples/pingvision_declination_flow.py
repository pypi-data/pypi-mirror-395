import datetime
import pathlib
import random
from pprint import pprint
import time

from pingintel_api.utils import set_verbosity
from pingintel_api.pingvision import types as t
from pingintel_api import PingVisionAPIClient


SCRIPT_DIR = pathlib.Path(__file__).parent
set_verbosity(2)

api_client = PingVisionAPIClient(environment="local", api_url="http://localhost:8002")
# api_client = PingVisionAPIClient(environment="dev")

global _cursor_id
_cursor_id = None


def get_persisted_cursor() -> str | None:
    # This function retrieves the cursor ID from a file or database...
    return _cursor_id


def persist_cursor_forever(cursor_id: str):
    # This function would save the cursor ID to a file or database...
    global _cursor_id
    cursor_id = cursor_id


def make_up_a_funny_name():
    syllables = [
        "foo",
        "bar",
        "baz",
        "qux",
        "corge",
        "grault",
        "garply",
        "waldo",
        "fre",
        "plugh",
        "xyzzy",
        "thud",
        "blat",
        "snarf",
        "glorp",
    ]

    num_words = random.randint(1, 3)

    name = " ".join("".join(random.choice(syllables) for _ in range(random.randint(3, 5))) for _ in range(num_words))

    return name.capitalize()


def find_key_identifiers():
    ret = api_client.list_teams()

    print("TEAMS: ")
    for team in ret:
        print(f"* {team['team_name']} ({team['team_uuid']})")

    for team in ret:
        if team["team_name"] == "WKFC":
            break
    else:
        raise ValueError("WKFC team not found")

    TEAM_UUID = team["team_uuid"]
    DIVISION_UUID = team["division_uuid"]

    print()
    statuses = api_client.list_submission_statuses(division=DIVISION_UUID)
    print("Submission statuses:")
    for status in statuses:
        print(f"* {status['name']} ({status['uuid']})")

    WORKFLOW_STATUS_PLEASE_SCRUB = next(_["uuid"] for _ in statuses if _["name"] == "Data Entry")
    WORKFLOW_STATUS_DECLINE = next(_["uuid"] for _ in statuses if _["name"] == "Declined")
    WORKFLOW_STATUS_APPROVE = next(_["uuid"] for _ in statuses if _["name"] == "Approved")

    return {
        "team_uuid": TEAM_UUID,
        "division_uuid": DIVISION_UUID,
        "workflow_status_please_scrub": WORKFLOW_STATUS_PLEASE_SCRUB,
        "workflow_status_decline": WORKFLOW_STATUS_DECLINE,
        "workflow_status_approve": WORKFLOW_STATUS_APPROVE,
    }


def generate_some_test_data(settings):
    current_time = datetime.datetime.now()
    ret = api_client.create_submission(
        filepaths=[SCRIPT_DIR / "test_sov.xlsx"],
        team_uuid=settings["team_uuid"],
        client_ref="test_client_ref",
        insured_name=make_up_a_funny_name(),
        inception_date=current_time + datetime.timedelta(days=random.randint(1, 60)),
        expiration_date=current_time + datetime.timedelta(days=random.randint(361, 600)),
    )
    pingid = ret["id"]
    url = ret["url"]

    print(f"pingid: {ret['id']}")


def start_listening(as_of_time: datetime.datetime | None, settings):
    cursor_id = get_persisted_cursor()
    start = as_of_time

    while True:
        ret = api_client.list_submission_events(
            page_size=10, team=settings["team_uuid"], cursor_id=cursor_id, start=start
        )
        cursor_id = ret["cursor_id"]

        for event in ret["results"]:
            event_date = datetime.datetime.fromisoformat(event["created_time"]).strftime("%Y-%m-%d %H:%M:%S")
            event_type = event["event_type"]
            new_value = event["new_value"]
            event_message = event["message"]
            pingid = event["pingid"]

            print(f"* Found event: {event_date} {pingid} {event_type}: {event_message}")

            if (
                event_type == t.SUBMISSION_EVENT_LOG_TYPE.SUBMISSION_STATUS_CHANGE
                and new_value == settings["workflow_status_please_scrub"]
            ):
                try:
                    perform_declination_logic(event["pingid"], settings)
                except Exception as e:
                    print(f"Error processing event for pingid {event['pingid']}: {e}")
                    continue

        time.sleep(1.0)

        persist_cursor_forever(cursor_id)


def perform_declination_logic(pingid: str, settings):
    submission_detail = api_client.list_submission_activity(pingid=pingid)
    submission_ret = submission_detail["results"][0]

    for document in submission_ret["documents"]:
        if document["document_type"] == "SOVFIXER_JSON":
            filename = document["filename"]
            document_url = document["url"]
            break
    else:
        raise ValueError(f"No JSON document found for pingid {pingid}, skipping...")

    output_filename = "downloaded-" + filename
    api_client.download_document(output_filename, document_url=document_url)

    print(f"Downloaded file to {output_filename}")

    print("Here, you should read that JSON and do something with it...")

    print("Valid actions:")
    pprint(submission_ret["actions"]["transition_to"])

    api_client.add_data_items(
        pingid,
        t.DATA_ITEM_ACTIONS.UPSERT,
        {
            "uw_declination_reason": "test reason",
            "broker_declination_reason": "test reason 2",
            "should_run_cytora": True,
        },
    )

    if random.choice([True, False]):
        print("Declining...")
        api_client.change_status(pingid=pingid, workflow_status_id=settings["workflow_status_decline"])
    else:
        print("Not declining...")
        api_client.change_status(pingid=pingid, workflow_status_id=settings["workflow_status_approve"])


settings = find_key_identifiers()


def generate_test_data_periodically():
    while True:
        generate_some_test_data(settings)
        time.sleep(30)


# import threading; threading.Thread(target=generate_test_data_periodically).start()
now = datetime.datetime.today()
start_listening(now, settings)
