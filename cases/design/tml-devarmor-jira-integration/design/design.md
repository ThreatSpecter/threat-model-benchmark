# devarmor-jira-integration

DevArmor-Forge App Integration — The scope is the integration of the Forge-based Jira Cloud application that lets developers request secure design reviews and synchronizes tenant metadata with the DevArmor backend. The DevArmor Forge App extends Jira Cloud so customers' product teams can raise security review requests without leaving their workflow. Forge UI modules and remote handlers run on Atlassian premises, issue short-lived installation tokens, and invoke a DevArmor backend in AWS through an API Gateway protected by a custom authorizer. The DevArmor backend stores external organization metadata in PostgreSQL and caches Atlassian access tokens in Secrets Manager before calling the Jira REST API to push status updates.

## Components
- Jira Cloud UI
- Jira REST API
- Confluence API
- Forge App
- Forge Remote Handler
- Forge Scheduler
- API Gateway with custom authorizer
- FastAPI service
- Jira Cloud data store
- AWS Secrets Manager
- Postgres metadata database

## Data flows
- jira-developer → jira-cloud-ui
- jira-cloud-ui → jira-rest-api
- jira-developer → forge-app
- jira-rest-api → forge-remote-handler
- forge-app → api-gateway-authorizer
- forge-remote-handler → api-gateway-authorizer
- forge-scheduler → api-gateway-authorizer
- api-gateway-authorizer → fastapi-service
- fastapi-service → postgres-core-db
- fastapi-service → secrets-manager-store
- fastapi-service → jira-rest-api

## Trust zones
- Public Internet
- Atlassian SaaS
- DevArmor Backend