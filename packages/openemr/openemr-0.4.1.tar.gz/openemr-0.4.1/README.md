OpenEMR api connector in python

## install

```bash
pip install openemr
```

## How to use

### 1. Enable the api

OpenEMR -> Admin -> Config -> Connectors
- Site adress (place your dns name in here)
- Enable the api endpoints
- Enable password grant for user role


### 2. Create oAuth2 client in OpenEMR

The easiest way to create a oAuth2 client in OpenEMR is to use the devtools on the OpenEMR webserver:

```bash
apk add jq
cd /root
wget https://raw.githubusercontent.com/openemr/openemr-devops/refs/heads/master/docker/openemr/flex-3.20/utilities/devtools
chmod +x devtools
./devtools register-oauth2-client
```

This will create a oAuth2 client in OpenEMR and return the client id and client secret.

For reference these are the commands in the devtools script, you can run them manually if you don't have access to the devtools or want to change some of the parameters:

```bash
echo "Registering a oauth2 client to site ${site}"
# collect scopes
scopes=`cat /var/www/localhost/htdocs/openemr/docker/library/api-scope-listing`
returnJson=`curl -X POST -k -H 'Content-Type: application/json' -s https://localhost/oauth2/${site}/registration --data "{
    \"application_type\": \"private\",
    \"redirect_uris\":
        [\"https://localhost:9300/swagger/oauth2-redirect.html\"],
    \"client_name\": \"A Private App\",
    \"token_endpoint_auth_method\": \"client_secret_post\",
    \"contacts\": [\"me@example.org\", \"them@example.org\"],
    \"scope\": \"${scopes}\"
    }"`
clientId=`echo $returnJson | jq '.client_id'`
clientSecret=`echo $returnJson | jq '.client_secret'`
echo "client id: ${clientId}"
echo "client secret: ${clientSecret}"
```

### 3. Enable the client

You need to enable the client in the OpenEMR web interface.

OpenEMR -> Admin -> System -> Api Clients
 - Edit you new client and enable it


### 4. Use the client

The connection to openemr is done by creating a client, there is one this a bit different than the other clients.
It requires a username and password, and a client id and client secret.
This is to authenticate with the client and authorize as the user.

```python
from openemr import Client as OpenEMRClient

config = {
    'base_url': 'https://localhost',
    'username': 'admin',
    'password': 'password',
    'client_id': 'client_id',
    'client_secret': 'client_secret'
}

def connect_to_openemr(config):
    """Create connection to OpenEMR instance"""
    print("Connecting to OpenEMR instance: ", config['base_url'])

    client = OpenEMRClient(
        username=config.get('username'),
        password=config.get('password'),
        base_url=config['base_url'],
        client_id=config.get('client_id'),
        client_secret=config.get('client_secret'),
        # client_scope=my_custom_scope_list,
    )
    return client

client = connect_to_openemr(config)
patients = client.get_patients()

print(len(patients))
```

## Scopes

The scopes are the permissions that the client has been granted.
By default we use the list below, if you want to use different scopes you can pass them as a list to the client constructor.

```python
scopes = [
    "openid",
    "offline_access",
    "api:oemr",
    "api:fhir",
    "api:port",
    "user/appointment.read",
    "user/facility.read",
    "user/patient.read",
    "user/practitioner.read",
    "user/Encounter.read",
    "user/Location.read",
]
```

Full scope list

```python
scopes = [
    'api:fhir',
    'api:oemr',
    'api:port',
    'launch/patient',
    'offline_access',
    'openid',
    'patient/AllergyIntolerance.read',
    'patient/Appointment.read',
    'patient/Binary.read',
    'patient/CarePlan.read',
    'patient/CareTeam.read',
    'patient/Condition.read',
    'patient/Coverage.read',
    'patient/Device.read',
    'patient/DiagnosticReport.read',
    'patient/DocumentReference.$docref',
    'patient/DocumentReference.read',
    'patient/Encounter.read',
    'patient/Goal.read',
    'patient/Immunization.read',
    'patient/Location.read',
    'patient/Medication.read',
    'patient/MedicationRequest.read',
    'patient/Observation.read',
    'patient/Organization.read',
    'patient/Patient.read',
    'patient/Person.read',
    'patient/Practitioner.read',
    'patient/Procedure.read',
    'patient/Provenance.read',
    'patient/appointment.read',
    'patient/encounter.read',
    'patient/patient.read',
    'user/AllergyIntolerance.read',
    'user/CarePlan.read',
    'user/CareTeam.read',
    'user/Condition.read',
    'user/Coverage.read',
    'user/Device.read',
    'user/DiagnosticReport.read',
    'user/DocumentReference.$docref',
    'user/DocumentReference.read',
    'user/Encounter.read',
    'user/Goal.read',
    'user/Immunization.read',
    'user/Location.read',
    'user/Medication.read',
    'user/MedicationRequest.read',
    'user/Observation.read',
    'user/Organization.read',
    'user/Organization.write',
    'user/Patient.read',
    'user/Patient.write',
    'user/Person.read',
    'user/Practitioner.read',
    'user/Practitioner.write',
    'user/PractitionerRole.read',
    'user/Procedure.read',
    'user/Provenance.read',
    'user/allergy.read',
    'user/allergy.write',
    'user/appointment.read',
    'user/appointment.write',
    'user/dental_issue.read',
    'user/dental_issue.write',
    'user/document.read',
    'user/document.write',
    'user/drug.read',
    'user/encounter.read',
    'user/encounter.write',
    'user/facility.read',
    'user/facility.write',
    'user/immunization.read',
    'user/insurance.read',
    'user/insurance.write',
    'user/insurance_company.read',
    'user/insurance_company.write',
    'user/insurance_type.read',
    'user/list.read',
    'user/medical_problem.read',
    'user/medical_problem.write',
    'user/medication.read',
    'user/medication.write',
    'user/message.write',
    'user/patient.read',
    'user/patient.write',
    'user/practitioner.read',
    'user/practitioner.write',
    'user/prescription.read',
    'user/procedure.read',
    'user/soap_note.read',
    'user/soap_note.write',
    'user/surgery.read',
    'user/surgery.write',
    'user/transaction.read',
    'user/transaction.write',
    'user/vital.read',
    'user/vital.write',
]
```
