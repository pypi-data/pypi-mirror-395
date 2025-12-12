# File name: client.py

import sys

# -------------------------------------------------------------------------
# 1) Attempt to import requests/urequests in a MicroPython-friendly manner
# -------------------------------------------------------------------------
try:
    if sys.implementation.name == "micropython":
        import urequests as requests
    else:
        import requests
except ImportError:
    # If MicroPython has "requests" installed as a third-party module, or CPython
    # is missing the 'requests' library, handle accordingly.
    # Typically on MicroPython, you want "urequests".
    raise ImportError("Could not import requests or urequests. Please install appropriately.")

# -------------------------------------------------------------------------
# 2) Attempt to import json/ujson in a MicroPython-friendly manner
# -------------------------------------------------------------------------
try:
    if sys.implementation.name == "micropython":
        import ujson as json
    else:
        import json
except ImportError:
    raise ImportError("Could not import json or ujson. Please install appropriately.")


# -------------------------------------------------------------------------
# Fallback for micropython that lacks advanced traceback chaining:
# We'll define a simple custom exception raising utility.
# -------------------------------------------------------------------------
def raise_request_error(message, original_exc=None):
    # We skip "raise ... from exc" to avoid MicroPython syntax problems.
    raise OM2MRequestError(f"{message}: {original_exc}" if original_exc else message)

# -------------------------------------------------------------------------
# ResourceType (no "enum" usage to keep it MicroPython-friendly)
# -------------------------------------------------------------------------
class ResourceType:
    AE = 2
    CONTAINER = 3
    CONTENT_INSTANCE = 4
    SUBSCRIPTION = 23

# -------------------------------------------------------------------------
# Import your custom exceptions & models
# (If you’re using a package structure in MicroPython, 
#  you may need to adapt these imports.)
# -------------------------------------------------------------------------
from .exceptions import OM2MRequestError
from .models import AE, Container, ContentInstance, Subscription


class OM2MClient:
    def __init__(
        self,
        base_url: str,
        cse_id: str,
        cse_name: str,
        username: str,
        password: str,
        use_json: bool = True
    ):
        """
        OM2MClient handles CRUD operations in a oneM2M server (OM2M).
        Each method focuses on a single responsibility.
        """
        self.base_url = base_url.rstrip("/")
        self.cse_id = cse_id
        self.cse_name = cse_name
        self.username = username
        self.password = password
        self.use_json = use_json

        self._common_headers = {
            "X-M2M-Origin": f"{self.username}:{self.password}",
        }

    # -------------------------------------------------------------------------
    # Internal Helpers
    # -------------------------------------------------------------------------
    def _make_url(self, relative_path: str) -> str:
        """
        Construct the correct URL from a given resource path.
        For oneM2M, some paths might be prefixed by '~'; if so, adapt accordingly.
        """
        rp = relative_path.strip("/")
        if rp.startswith("~"):
            return f"{self.base_url}/{rp.lstrip('~')}"
        return f"{self.base_url}/~/{rp}"

    def _content_headers(self, resource_type: int):
        """
        Returns the Content-Type and Accept headers based on whether JSON or XML is used,
        as well as the resource type (ty).
        """
        common_headers = self._common_headers.copy()
        if self.use_json:
            content_type = f"application/json;ty={resource_type}"
            accept_type = "application/json"
        else:
            content_type = f"application/xml;ty={resource_type}"
            accept_type = "application/xml"

        headers = common_headers
        headers["Content-Type"] = content_type
        headers["Accept"] = accept_type
        return headers

    def _request(self, method: str, url: str, headers=None, data=None):
        """
        A wrapper around requests or urequests that:
         - Handles exceptions
         - Raises OM2MRequestError on non-2xx responses
        """
        try:
            method = method.lower()
            if method == "get":
                resp = requests.get(url, headers=headers)
            elif method == "post":
                resp = requests.post(url, headers=headers, data=data)
            elif method == "put":
                resp = requests.put(url, headers=headers, data=data)
            elif method == "delete":
                resp = requests.delete(url, headers=headers)
            else:
                raise ValueError("Unsupported HTTP method: {}".format(method))
        except Exception as exc:
            raise_request_error(f"Request to {url} failed", exc)

        if not (200 <= resp.status_code < 300):
            raise OM2MRequestError(
                f"HTTP {resp.status_code} Error for {url}:\n{resp.text}"
            )
        return resp

    # -------------------------------------------------------------------------
    # Basic Retrieval
    # -------------------------------------------------------------------------
    def retrieve_resource(self, resource_path: str) -> str:
        """
        Retrieve a resource (GET operation) from the CSE.
        Returns the raw response text (JSON or XML).
        """
        url = self._make_url(resource_path)
        headers = self._common_headers.copy()
        headers["Accept"] = "application/json" if self.use_json else "application/xml"
        resp = self._request("GET", url, headers=headers)
        return resp.text

    # -------------------------------------------------------------------------
    # Create Resources
    # -------------------------------------------------------------------------
    def create_ae(self, ae: AE) -> str:
        """
        Create an Application Entity (AE) under the CSE.
        Returns the 'Content-Location' of the created resource.
        """
        url = self._make_url(self.cse_id)
        headers = self._content_headers(ResourceType.AE)

        if self.use_json:
            body = {
                "m2m:ae": {
                    "rn": ae.rn,
                    "api": ae.api,
                    "rr": str(ae.rr).lower(),
                    "lbl": ae.lbl
                }
            }
            data = json.dumps(body)
        else:
            # XML not tested frequently in MicroPython, but logically correct
            label_text = " ".join(ae.lbl) if ae.lbl else ""
            data = f"""<m2m:ae xmlns:m2m="http://www.onem2m.org/xml/protocols" rn="{ae.rn}">
    <api>{ae.api}</api>
    <rr>{"true" if ae.rr else "false"}</rr>
    <lbl>{label_text}</lbl>
</m2m:ae>"""

        resp = self._request("POST", url, headers=headers, data=data)
        return resp.headers.get("Content-Location", "")

    def create_container(self, parent_path: str, container: Container) -> str:
        """
        Create a Container resource (CNT) under a given parent path.
        Returns the 'Content-Location' of the created resource.
        """
        url = self._make_url(parent_path)
        headers = self._content_headers(ResourceType.CONTAINER)

        if self.use_json:
            body = {
                "m2m:cnt": {
                    "rn": container.rn,
                    "lbl": container.lbl
                }
            }
            data = json.dumps(body)
        else:
            label_text = " ".join(container.lbl) if container.lbl else ""
            data = f"""<m2m:cnt xmlns:m2m="http://www.onem2m.org/xml/protocols" rn="{container.rn}">
    <lbl>{label_text}</lbl>
</m2m:cnt>"""

        resp = self._request("POST", url, headers=headers, data=data)
        return resp.headers.get("Content-Location", "")

    def create_content_instance(self, parent_path: str, cin: ContentInstance) -> str:
        """
        Create a ContentInstance resource (CIN) under a given parent path.
        Returns the 'Content-Location' of the created resource.
        """
        url = self._make_url(parent_path)
        headers = self._content_headers(ResourceType.CONTENT_INSTANCE)

        if self.use_json:
            body = {
                "m2m:cin": {
                    "cnf": cin.cnf,
                    "con": cin.con
                }
            }
            if cin.rn:
                body["m2m:cin"]["rn"] = cin.rn
            data = json.dumps(body)
        else:
            rn_attr = f' rn="{cin.rn}"' if cin.rn else ""
            data = f"""<m2m:cin xmlns:m2m="http://www.onem2m.org/xml/protocols"{rn_attr}>
    <cnf>{cin.cnf}</cnf>
    <con>{cin.con}</con>
</m2m:cin>"""

        resp = self._request("POST", url, headers=headers, data=data)
        return resp.headers.get("Content-Location", "")

    def create_subscription(self, parent_path: str, subscription: Subscription) -> str:
        """
        Create a Subscription resource (SUB) under a given parent path.
        Returns the 'Content-Location' of the created resource.
        """
        url = self._make_url(parent_path)
        headers = self._content_headers(ResourceType.SUBSCRIPTION)

        if self.use_json:
            body = {
                "m2m:sub": {
                    "rn": subscription.rn,
                    "nu": [subscription.nu],
                    "nct": subscription.nct
                }
            }
            data = json.dumps(body)
        else:
            data = f"""<m2m:sub xmlns:m2m="http://www.onem2m.org/xml/protocols" rn="{subscription.rn}">
    <nu>{subscription.nu}</nu>
    <nct>{subscription.nct}</nct>
</m2m:sub>"""

        resp = self._request("POST", url, headers=headers, data=data)
        return resp.headers.get("Content-Location", "")

    # -------------------------------------------------------------------------
    # Retrieve Latest Data for a Specific Device
    # -------------------------------------------------------------------------
    def retrieve_latest_data(self, device_name: str, container_name: str = "DATA") -> dict:
        """
        Retrieves the latest ContentInstance (la) from the specified container (default: 'DATA')
        for a given device_name (the AE's resourceName).

        Returns a dict with the JSON response.
        Raises OM2MRequestError if the request fails.
        """
        resource_path = f"{self.cse_id}/{self.cse_name}/{device_name}/{container_name}/la"
        resp_text = self.retrieve_resource(resource_path)
        return json.loads(resp_text)

    def get_all_devices_latest_data(self):
        """
        1. Retrieve all devices (AEs)
        2. For each device, retrieve the latest content instance
        """
        devices_json = self.retrieve_resource(f"{self.cse_id}?rcn=4&ty=2")
        data = json.loads(devices_json)
        devices = data["m2m:cb"].get("m2m:ae", [])

        all_devices_data = []
        for device in devices:
            device_name = device["rn"]  # e.g., 'device1'
            try:
                latest_data = self.retrieve_latest_data(device_name=device_name, container_name="DATA")
                cin = latest_data["m2m:cin"]
                content_str = cin.get("con", "")
                parsed_content = {}
                if content_str:
                    try:
                        parsed_content = json.loads(content_str)
                    except Exception:
                        parsed_content = content_str

                all_devices_data.append({
                    "device": device_name,
                    "latest": {
                        "cin_rn": cin.get("rn"),
                        "timestamp": cin.get("ct"),
                        "content": parsed_content
                    }
                })
            except OM2MRequestError as e:
                all_devices_data.append({
                    "device": device_name,
                    "error": str(e)
                })

        return all_devices_data

    # -------------------------------------------------------------------------
    # Retrieve ALL Content Instances for a Single Device (Minimal JSON)
    # -------------------------------------------------------------------------
    def retrieve_all_content_instances_minimal(
        self, device_name: str, container_name: str = "DATA"
    ) -> dict:
        """
        Retrieve ALL ContentInstances (CIN) from 'container_name' for the specified 'device_name'.
        Parse them into a minimal JSON structure containing:
          - AE name
          - Originating MN name
          - A list of {timestamp, parsed content} entries
        """
        resource_path = f"{self.cse_id}/{self.cse_name}/{device_name}/{container_name}?rcn=4"
        resp_text = self.retrieve_resource(resource_path)
        data = json.loads(resp_text)

        cnt = data.get("m2m:cnt", {})
        cin_list = cnt.get("m2m:cin", [])

        instances = []
        for cin in cin_list:
            timestamp = cin.get("ct", "")
            raw_content = cin.get("con", "")
            try:
                parsed_content = json.loads(raw_content)
            except Exception:
                parsed_content = raw_content

            instances.append({
                "timestamp": timestamp,
                "content": parsed_content
            })

        return {
            "AE": device_name,
            "MN": self.cse_name,
            "Instances": instances
        }

    # -------------------------------------------------------------------------
    # Retrieve ALL AEs and ALL Data
    # -------------------------------------------------------------------------
    def retrieve_all_aes_and_data_minimal(self, container_name: str = "DATA") -> list:
        """
        1) Retrieves all AEs (devices) from the CSE.
        2) For each AE, retrieves ALL CIN in the specified 'container_name' (default: 'DATA').
        3) Returns a list of minimal JSON structures.
        """
        resource_path = f"{self.cse_id}?rcn=4&ty=2"
        resp_text = self.retrieve_resource(resource_path)
        data = json.loads(resp_text)

        cb = data.get("m2m:cb", {})
        ae_list = cb.get("m2m:ae", [])

        all_data = []
        for ae in ae_list:
            ae_name = ae.get("rn", "")
            device_data = self.retrieve_all_content_instances_minimal(ae_name, container_name)
            all_data.append(device_data)

        return all_data

    # -------------------------------------------------------------------------
    # Experimental Function: MN Syncing (Disabled for MicroPython)
    # -------------------------------------------------------------------------
    if sys.implementation.name == "micropython":
        def replicate_ae_data_from_minimal(
            self,
            minimal_data: dict,
            target_client: "OM2MClient",
            container_name: str = "DATA"
        ) -> None:
            """
            Disabled for MicroPython. Raises NotImplementedError.
            """
            raise NotImplementedError(
                "The 'replicate_ae_data_from_minimal' function is not available on MicroPython."
            )
    else:
        def replicate_ae_data_from_minimal(
            self,
            minimal_data: dict,
            target_client: "OM2MClient",
            container_name: str = "DATA"
        ) -> None:
            """
            Replicates the AE (and all content) described by 'minimal_data' onto the 'target_client'.

            NOTE: This method is intended for full CPython environments only.
            """
            from .models import AE, Container, ContentInstance

            ae_name = minimal_data["AE"]
            instances = minimal_data["Instances"]

            # 1) Check if AE exists on the target
            try:
                all_ae_resp = target_client.retrieve_resource(f"{target_client.cse_id}?rcn=4&ty=2")
                all_ae_data = json.loads(all_ae_resp)
                ae_list = all_ae_data.get("m2m:cb", {}).get("m2m:ae", [])
            except Exception as exc:
                raise RuntimeError(f"Failed to list AEs on target: {exc}")

            ae_exists = any(a.get("rn") == ae_name for a in ae_list)
            if not ae_exists:
                new_ae = AE(rn=ae_name, api="replicated-app", rr=False, lbl=["replicated"])
                try:
                    target_client.create_ae(new_ae)
                    print(f"[REPLICATE] Created AE '{ae_name}' on target.")
                except Exception as e:
                    raise RuntimeError(f"Failed to create AE {ae_name} on target: {e}")
            else:
                print(f"[REPLICATE] AE '{ae_name}' already exists on target; skipping AE creation.")

            # 2) Check if container exists
            container_parent = f"{target_client.cse_id}/{target_client.cse_name}/{ae_name}"
            try:
                cnt_resp_text = target_client.retrieve_resource(f"{container_parent}?rcn=4&ty=3")
                cnt_json = json.loads(cnt_resp_text)
                cnt_list = cnt_json.get("m2m:ae", {}).get("m2m:cnt", [])
            except OM2MRequestError:
                cnt_list = []

            data_exists = any(c.get("rn") == container_name for c in cnt_list)
            if not data_exists:
                new_container = Container(rn=container_name, lbl=["replicated-data"])
                try:
                    target_client.create_container(container_parent, new_container)
                    print(f"[REPLICATE] Created container '{container_name}' under AE '{ae_name}' on target.")
                except Exception as e:
                    raise RuntimeError(f"Failed to create container {container_name} on target: {e}")
            else:
                print(f"[REPLICATE] Container '{container_name}' already exists under AE '{ae_name}' on target.")

            # 3) Fetch existing CIN on target to see what's already there
            container_path = f"{target_client.cse_id}/{target_client.cse_name}/{ae_name}/{container_name}"
            try:
                full_data_text = target_client.retrieve_resource(f"{container_path}?rcn=4")
                container_json = json.loads(full_data_text)
                existing_cin_list = container_json.get("m2m:cnt", {}).get("m2m:cin", [])
            except OM2MRequestError:
                existing_cin_list = []

            existing_timestamps = set()
            for cin in existing_cin_list:
                existing_rn = cin.get("rn", "")
                existing_timestamps.add(existing_rn)

            # 4) Replicate each instance if not already present
            for inst in instances:
                timestamp = inst["timestamp"]
                content = inst["content"]

                safe_timestamp = timestamp.replace(":", "").replace("-", "").replace("T", "_")
                new_rn = f"cin_{safe_timestamp}"

                if new_rn in existing_timestamps:
                    print(f"[REPLICATE] CIN '{new_rn}' already on target; skipping.")
                    continue

                payload = {
                    "timestamp": timestamp,
                    "content": content
                }

                new_cin = ContentInstance(
                    cnf="application/json",
                    con=json.dumps(payload),
                    rn=new_rn
                )
                try:
                    target_client.create_content_instance(container_path, new_cin)
                    print(f"[REPLICATE] Created new CIN '{new_rn}' on target for timestamp {timestamp}.")
                    existing_timestamps.add(new_rn)
                except Exception as e:
                    print(f"[ERROR] Failed to create CIN '{new_rn}': {e}")
