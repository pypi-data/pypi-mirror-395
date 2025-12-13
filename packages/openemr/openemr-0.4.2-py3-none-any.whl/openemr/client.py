"""
Core openemr rest api client functionality.
"""

import requests

from openemr import __version__
from openemr.patient import Patient

_USER_AGENT = "OpenEmrApiClientPython/%s" % __version__


class Client(object):
    """Performs requests to the OpenEmr rest API."""

    basic_read_only_scopes = [
        "openid",
        "offline_access",
        "api:oemr",
        "api:fhir",
        "api:port",
        "user/appointment.read",
        "user/facility.read",
        "user/patient.read",
        "user/practitioner.read", 
    ]


    full_access_scopes = [
        "openid",
        "offline_access",
        "api:oemr",
        "api:fhir",
        "api:port",
        "user/appointment.read",
        "user/appointment.write",
        "user/document.read",
        "user/document.write",
        "user/encounter.read",
        "user/encounter.write",
        "user/facility.read",
        "user/facility.write",
        "user/message.write",
        "user/patient.read",
        "user/patient.write",
        "user/practitioner.read",
        "user/practitioner.write"
    ]


    def __init__(
        self,
        username,
        password,
        base_url="https://localhost",
        client_scope=basic_read_only_scopes,
        client_id=None,
        client_secret=None,
    ):
        """Base OpenEmr api client."""

        self.base_url = base_url
        self.client_scope = client_scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.session = requests.Session()
        self._login()

    def _login(self):
        """Log in to the OpenEMR API."""

        if "refresh_token" in self.__dict__:
            # Use refresh token to fetch new access token
            payload = {
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": self.refresh_token,
            }
            del self.refresh_token
        else:
            payload = {
                "grant_type": "password",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "username": self.username,
                "password": self.password,
                "scope": " ".join(self.client_scope),
                "user_role": "users",
            }

        print(f"Authenticating with {payload['grant_type']} grant type")

        self.session.headers.update(
            {
                "User-Agent": _USER_AGENT,
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )

        token_response = self.session.post(
            url=self.base_url + "/oauth2/default/token", data=payload
        )

        try:
            json_token_response = token_response.json()
        except:
            raise Exception(
                f"Failed to authenticate: {token_response.status_code} {token_response.text}"
            )

        if token_response.status_code != 200:
            raise Exception(
                f"Failed to authenticate: {token_response.status_code} {token_response.text}"
            )

        self.access_token = json_token_response["access_token"]
        self.refresh_token = json_token_response["refresh_token"]

        self.session.headers.update(
            {
                "User-Agent": _USER_AGENT,
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.access_token,
            }
        )

        self.api_url = f"{self.base_url}/apis/default/api"

        # test the connection
        try:
            self.api_version = self._get(self.api_url + "/version")
            print(
                f"Connected to OpenEMR API {self.base_url} version: {self.api_version}"
            )
        except Exception as e:
            if "refresh_token" in self.__dict__:
                print(
                    "Failed to connect to OpenEMR API, trying login without refresh token"
                )
                del self.refresh_token
                self._login()
            else:
                raise Exception("Failed to connect to OpenEMR API: " + str(e))

    def response_handler(self, response):
        """Handle API responses, returning JSON or text."""
        if response.status_code == 404:
            return None
        if response.status_code not in range(200, 399):
            raise Exception(f"Failed to get {response.url}: {response.status_code} {response.text}")
        try:
            return response.json()
        except:
            return response.text

    def _post(self, url, payload=None):
        """Performs HTTP POST with credentials, returning the body as JSON."""

        response = self.session.post(url, data=payload)
        if response.status_code == 401:
            self._login()
            response = self.session.post(url, data=payload)
        return self.response_handler(response)

    def _post_json(self, url, payload=None):
        """Performs HTTP POST with credentials, returning the body as JSON."""

        response = self.session.post(url, json=payload)
        if response.status_code == 401:
            self._login()
            response = self.session.post(url, json=payload)
        return self.response_handler(response)

    def _put(self, url, payload=None):
        """Performs HTTP PUT with credentials, returning the body as JSON."""

        response = self.session.put(url, json=payload)
        if response.status_code == 401:
            self._login()
            response = self.session.put(url, json=payload)
        return self.response_handler(response)

    def _get(self, url, payload=None):
        """Performs HTTP GET with credentials, returning the body as JSON."""

        response = self.session.get(url)
        if response.status_code == 401:
            self._login()
            response = self.session.get(url)
        return self.response_handler(response)

    def patient(self, uuid):
        """Patient info by uuid"""

        r = self._get(self.api_url + "/patient/" + str(uuid))
        try:
            return Patient(self, r['data'])
        except:
            raise Exception(f"Failed to get patient {uuid}: {r}")

    def patient_search(self, exact=False, **kwargs) -> list:
        """lookup patients, if no search terms given returns all patients"""

        print("Searching for patients with kwargs: ", kwargs)

        # might crash on too many search results, for reliable all patient search use get_patients()
        # use keyword arguments as search terms like lname fname dob etc.
        searchterms = ""
        if kwargs is not None:
            for key, value in kwargs.items():
                searchterms = searchterms + "&%s=%s" % (key, value)
        else:
            return self.get_patients()

        results = self._get(self.api_url + "/patient" + searchterms)['data']
        if not results:
            return []
        
        # if exact is True, filter results with kwargs
        if exact:
            results = [r for r in results if all(k in r and r[k] == v for k, v in kwargs.items())]
        
        return [Patient(self, patient_data) for patient_data in results]

    def _patient_search(self, **kwargs):
        """lookup patients, if no search terms given returns all patients"""

        # might crash on too many search results, for reliable all patient search use get_patients()
        # use keyword arguments as search terms like lname fname dob etc.
        searchterms = ""
        if kwargs is not None:
            for key, value in kwargs.items():
                searchterms = searchterms + "&%s=%s" % (key, value)
        else:
            return self.get_patients()

        patients_results = self._get(self.api_url + "/patient" + searchterms)['data']
        if not patients_results:
            return []
        
        return [Patient(self, patient_data) for patient_data in patients_results]

    def _appointment(self):
        """list al appointments"""

        return self._get(self.api_url + "/appointment")

    def _new_patient(self, payload=None):
        """Create new patient"""

        # Check required fields
        try:
            city = payload["city"]
            country_code = payload["country_code"]
            dob = payload["dob"]
            ethnicity = payload["ethnicity"]
            fname = payload["fname"]
            lname = payload["lname"]
            mname = payload["mname"]
            phone_contact = payload["phone_contact"]
            postal_code = payload["postal_code"]
            race = payload["race"]
            sex = payload["sex"]
            state = payload["state"]
            street = payload["street"]
            title = payload["title"]
        except:
            print("not all fields are filled!")
            return None

        pid = str(int(self._patient_search()[-1]["pid"]) + 1)
        exists = self._patient(pid=pid)
        if exists:
            print(
                "The pid I suggested already exists, this is strange check openemr class."
            )
            return None

        # on success will return: {'pid': '5970'} use pid with newPid = class._new_patient(payload=payload)['pid']
        return self._post_json(self.api_url + "/patient", payload=payload)

    def create_patient(self, patient_data):
        """Create new patient"""
        required_fields = ["fname", "lname", "DOB", "sex"]
        for field in required_fields:
            if field not in patient_data:
                raise ValueError(f"Missing required field: {field}")

        return self._post_json(self.api_url + "/patient", payload=patient_data)

    def get_patients(self) -> list:
        """Get all patients with pagination"""

        page_size = 200
        page = 0
        patients = []

        # page_size - 1 is used to make sure we get page size number of patients
        # otherwise emr returns one more patient
        result_data = self._get(self.api_url + "/patient" + f"?_limit={page_size - 1}")[
            "data"
        ]
        while result_data:
            print(f"Page {page} of {page_size}")
            patients.extend(result_data)
            page += 1
            result_data = self._get(
                self.api_url
                + "/patient"
                + f"?_limit={page_size - 1}&_offset={page * page_size}"
            )["data"]

        return [Patient(self, patient_data) for patient_data in patients]
