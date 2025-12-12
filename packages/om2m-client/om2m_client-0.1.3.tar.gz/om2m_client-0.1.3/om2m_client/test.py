#!/usr/bin/env python3
#File name: test.py

import json
from om2m_client import (
    OM2MClient, 
    AE, 
    Container, 
    ContentInstance, 
    Subscription, 
    OM2MRequestError
)

def main():
    # -------------------------------------------------------------------------
    # 1) Instantiate the OM2MClient
    # -------------------------------------------------------------------------
    client = OM2MClient(
        base_url="http://localhost:8282",
        cse_id="mn-cse",
        cse_name="mn-name",
        username="admin",
        password="admin",
        use_json=True
    )

    # -------------------------------------------------------------------------
    # 2) [Optional] Create an AE (Application Entity) for testing
    #    If you already have your device(s), skip this step.
    # -------------------------------------------------------------------------
    test_ae = AE(
        rn="myTestAE", 
        api="test-api", 
        rr=False, 
        lbl=["python-test"]
    )
    try:
        ae_location = client.create_ae(test_ae)
        print(f"[CREATE AE] myTestAE => {ae_location}")
    except OM2MRequestError as e:
        print(f"[ERROR] Failed to create AE: {e}")

    # -------------------------------------------------------------------------
    # 3) [Optional] Create a Container under the newly created AE
    #    e.g., "myTestAE/DATA"
    # -------------------------------------------------------------------------
    container_path = f"{client.cse_id}/{client.cse_name}/myTestAE"
    test_container = Container(
        rn="DATA", 
        lbl=["Category/sensorData"]
    )
    try:
        cnt_location = client.create_container(container_path, test_container)
        print(f"[CREATE CNT] myTestAE/DATA => {cnt_location}")
    except OM2MRequestError as e:
        print(f"[ERROR] Failed to create Container: {e}")

    # -------------------------------------------------------------------------
    # 4) [Optional] Create a ContentInstance (sensor reading) in that container
    # -------------------------------------------------------------------------
    cin_path = f"{client.cse_id}/{client.cse_name}/myTestAE/DATA"
    test_cin = ContentInstance(
        cnf="application/json",
        con=json.dumps({"temperature": 42})
    )
    try:
        cin_location = client.create_content_instance(cin_path, test_cin)
        print(f"[CREATE CIN] => {cin_location}")
    except OM2MRequestError as e:
        print(f"[ERROR] Failed to create ContentInstance: {e}")

    # -------------------------------------------------------------------------
    # 5) Retrieve the latest data from each registered AE (device)
    # -------------------------------------------------------------------------
    print("\n[GET ALL DEVICES' LATEST DATA]")
    try:
        latest_data_list = client.get_all_devices_latest_data()
        for device_info in latest_data_list:
            print(json.dumps(device_info, indent=2))
    except OM2MRequestError as e:
        print(f"[ERROR] Failed to fetch latest data for all devices: {e}")

    # -------------------------------------------------------------------------
    # 6) Retrieve ALL data (ContentInstances) for a specific device, e.g. 'device10'
    #    Then display the minimal JSON structure.
    # -------------------------------------------------------------------------
    device_name = "device10"  # change if needed
    print(f"\n[GET ALL DATA FOR '{device_name}' - MINIMAL JSON]")
    try:
        all_data_device10 = client.retrieve_all_content_instances_minimal(device_name)
        print(json.dumps(all_data_device10, indent=2))
    except OM2MRequestError as e:
        print(f"[ERROR] Failed to fetch all data from '{device_name}': {e}")


    target_client = OM2MClient(
        base_url="http://localhost:8282",
        cse_id="mn-cse",
        cse_name="mn-name",
        username="admin",
        password="admin",
        use_json=True
    )

    client.replicate_ae_data_from_minimal(all_data_device10, target_client, container_name="DATA2")


if __name__ == "__main__":
    main()
