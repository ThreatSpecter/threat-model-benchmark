# Vehicle registration feature

**Notes:** _This is one of several examples demonstrating how you might use Threat Composer when working through AWS' Threat Modeling for Builders training. It is intentionally incomplete and is only used as a reference starting point. You may have different perspectives on the assumptions, threats and mitigations. This is OK, and could be used to start conversations with your team if you are taking the Threat Modeling Builders training as a group._

### System Summary

The vehicle registration feature is the decomposed portion of a fictitious AWS Connected Vehicle Solution. This feature aims to address the user story:

**“As a vehicle fleet manager, I want to register an existing IoT connected vehicle to bring it into service.”** 

This feature builds on top of features that have already been threat modeled and deployed - namely the web front end hosted on AWS Amplify and user authentication through Amazon Cognito.

## Architecture


Our vehicle registration feature builds on top of features that have already been threat modeled and deployed - namely the web front end hosted on AWS Amplify and user authentication through Amazon Cognito.

### Included in the architecture

- The existing AWS Amplify deployment for the required static assets to render the webpage (HTML, JavaScript, and CSS); and
 - The existing Amazon Cognito integration for user pool authentication.

### API Information
The vehicle registration feature will support the following APIs configured in Amazon API Gateway and serviced from Lambda functions:

**ListVehicles**

- Returns information for all available IoT connected vehicles.
- No parameters are taken as inputs.
- Response includes `HTTP response code`, `vehicle_id` (STRING - GUID) and `vehicle_registered` (BOOLEAN).

**RegisterVehicle**

- Registers an existing IoT connected vehicle to bring it into service.
- Items including `vehicle_id` (STRING - GUID), `vehicle_type` (STRING), `vehicle_registration_number` (STRING) and PDF version of the vehicle registration document (Bytes) are taken as inputs.
- The existing DynamoDB table record is updated with vehicle_type and vehicle_registration_number. vehicle_registered is set to true.
- The vehicle registration document (PDF) is written as a blob of bytes to Amazon S3 (prefix: `\vehicle_registration_documents\.pdf`).
- Response includes `HTTP response code` and vehicle attributes, including `vehicle_id` (GUID), `vehicle_registered` (BOOLEAN)

**Deregister vehicle**

- Deregisters an existing registered IoT connected vehicle to bring out of service.
- `vehicle_id` (STRING - GUID) is taken as an input.
- The existing DynamoDB table record fields `vehicle_type` and `vehicle_registration_number` will be deleted, and `vehicle_registered` set to `false`.
- The vehicle registration document (PDF) will be deleted from Amazon S3 (prefix: `\vehicle_registration_documents\.pdf`).
- Response includes `HTTP response code` and vehicle attributes, including `vehicle_id` (GUID), `vehicle_registered` (BOOLEAN)

**DescribeVehicle**

- Returns information for a specific IoT connected vehicle - including pre-signed URL to the vehicle registration document (if registered).
- `vehicle_id` (STRING - GUID) is taken as an input.
- The existing DynamoDB table record will be queried, and the Lambda function code will generate a pre-signed URL  for vehicle registration document Amazon S3 object.
- Response includes `HTTP Response Code` and `vehicle attributes`, including `vehicle_id` (GUID), `vehicle_registered` (BOOLEAN), `vehicle_type` (STRING), `vehicle_registration_number` (STRING), `vehicle_registration_expiry_date` (STRING) and `vehicle_registration_document_url` (STRING)

## Data flow

For simplicity, the reference data flow diagram solely covers the data/request plane of the vehicle registration feature and ignores the control/administrative plane . When threat modeling real systems, it is worthwhile to analyze all planes of operations, possibly using separate diagrams for each plane. The existing data flows of the frontend on AWS Amplify and authentication with Amazon Cognito are included for context, but are not specifically part of the exercises as they have been threat modeled prior to them being deployed.
