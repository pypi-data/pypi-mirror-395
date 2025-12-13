import requests
import mimetypes
import os

class Patient:
    def __init__(self, client, patient_data):
        self.client = client
        self.data = patient_data
        self.id = patient_data.get('pid')
        self.uuid = patient_data.get('uuid')

    def get_documents(self) -> list:
        """Get all documents for this patient, 404 if no documents are found"""
        api_uri = f"{self.client.api_url}/patient/{self.id}/document?path=/MedicalRecord"
        return self.client._get(api_uri)

    def get_document(self, doc_id, local_path):
        """Download a specific document by ID"""
        api_uri = f"{self.client.api_url}/patient/{self.id}/document/{doc_id}"

        try:
            response = self.client.session.get(api_uri, stream=True)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

            # log headers
            print(f"Headers: {response.headers}")

            # Ensure the directory exists
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    # filter out keep-alive new chunks
                    if chunk:
                        f.write(chunk)
            print(f"Document {doc_id} downloaded successfully to {local_path}")
            return local_path

        except requests.exceptions.RequestException as e:
            print(f"Error downloading document {doc_id}: {e}")
            # Re-raise or handle the error as appropriate for your application
            raise
        except IOError as e:
            print(f"Error writing document {doc_id} to {local_path}: {e}")
            # Re-raise or handle the error as appropriate
            raise

    def post_document(self, source_document, document_type=None):
        """Post a document for this patient
        
        Args:
            source_document (str): Path to the document file
            document_type (str, optional): MIME type of the document. If None, it will be inferred from the file extension.
        """
        url = f"{self.client.api_url}/patient/{self.id}/document"

        params = {
            "path": "/MedicalRecord"
        }

        headers = {
            # Authorization header is already set on the session; do NOT
            # pre-set Content-Type so that `requests` can add the correct
            # multipart boundary (this was the root of the 500 error).
            "Accept": "application/json",
            "Authorization": f"Bearer {self.client.access_token}",
        }

        if document_type is None:
            document_type = mimetypes.guess_type(source_document)[0] or "application/octet-stream"

        filename = os.path.basename(source_document)

        with open(source_document, 'rb') as f:
            # Prepare the 'files' dictionary for multipart upload
            # Structure: {form_field_name: (filename, file_object, content_type)}
            files = {
                "document": (filename, f, document_type)
            }
            r = requests.post(url, headers=headers, params=params, files=files)

        if r.status_code != 200:
            raise Exception(f"Failed to post document: {r.status_code} {r.text}")
        return r

    def get_encounters(self) -> list:
        """Get all encounters for this patient"""
        return self.client._get(f"{self.client.api_url}/patient/{self.id}/encounter")

    def get_appointments(self) -> list:
        """Get all appointments for this patient"""
        return self.client._get(f"{self.client.api_url}/patient/{self.id}/appointment")

    def get_appointment(self, id: int) -> dict:
        """Get a specific appointment by ID for this patient"""
        return self.client._get(f"{self.client.api_url}/patient/{self.id}/appointment/{id}")

    def create_appointment(self, appointment_data):
        """Create a new appointment for this patient"""

        # ensure all the required fields are filled in
        required_fields = ["pc_catid", "pc_title", "pc_duration", "pc_hometext", "pc_apptstatus", "pc_eventDate", "pc_startTime", "pc_facility", "pc_billing_location", "pc_aid"]
        for field in required_fields:
            if field not in appointment_data:
                raise ValueError(f"Missing required field: {field}")

        # Example Appointment DATA:
        #   {
        #   pc_catid*	string The category of the appointment.
        #   pc_title*	string The title of the appointment.
        #   pc_duration*	string The duration of the appointment.
        #   pc_hometext*	string Comments for the appointment.
        #   pc_apptstatus*	string use an option from resource=/api/list/apptstat
        #   pc_eventDate*	string The date of the appointment.
        #   pc_startTime*	string The time of the appointment.
        #   pc_facility*	string The facility id of the appointment.
        #   pc_billing_location*	string The billinag location id of the appointment.
        #   pc_aid	string The provider id for the appointment.
        #   }
        #   example: { "pc_catid": "5", "pc_title": "Office Visit", "pc_duration": "900", "pc_hometext": "Test", "pc_apptstatus": "-", "pc_eventDate": "2018-10-19", "pc_startTime": "09:00", "pc_facility": "9", "pc_billing_location": "10", "pc_aid": "1" }

        return self.client._post_json(f"{self.client.api_url}/patient/{self.id}/appointment", appointment_data)

    # Add getter methods to access patient attributes
    def __getattr__(self, name):
        """Allow access to patient data via attributes"""
        if name in self.data:
            return self.data[name]
        raise AttributeError(f"Patient has no attribute '{name}'")