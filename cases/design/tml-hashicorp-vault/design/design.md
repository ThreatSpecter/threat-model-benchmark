# hashicorp-vault

HashiCorp Vault — HashiCorp Vault is a secrets management system that provides secure storage, access control, dynamic credentials, cryptographic operations (Transit), and secret leasing/renewal. A typical deployment consists of Vault clients (applications, CI/CD, operators) communicating over TLS with one or more Vault server nodes. Vault enforces authentication (e.g., AppRole, AWS/GCP/IAM, OIDC/JWT, Kubernetes), issues scoped tokens bound to policies, and gates all operations through its HTTP API. The server maintains an encrypted storage barrier and persists data in a backend - the integrated Storage/Raft deployment is the one in scope. Clusters are commonly configured in HA mode with an active leader and standby nodes. Core security properties include encryption at rest within the barrier, mutual TLS on all control/data paths, least-privilege policies, response wrapping, and short-lived dynamic secrets. Operational workflows cover initialization and sealing (Shamir key shares), unsealing, rotation of root keys and encryption keys, audit device configuration (e.g., file/socket/syslog), mount-by-mount secrets engine hardening, and strict network segmentation—especially between clients, Vault nodes, and the storage backend. Misconfigurations to consider include over-permissive policies, exposed Raft/Consul ports, weak auth method constraints, disabled audit logging, and long-lived tokens. This threat model involves an AWS deployment with k8s and a load balancer Enterprise secrets management and cryptographic services for applications and operators.

## Components
- Client Application (App 1)
- VPN Gateway
- AWS Load Balancer
- Amazon EKS Cluster
- Kubernetes Service: vault-internal
- Vault HA Deployment (StatefulSet)
- Vault Authentication Methods
- Vault Secret Engines
- Vault Audit Devices
- Vault CLI / API Client
- Vault Auto-Unseal (Cloud KMS Integration)
- Vault API
- Vault Integrated Storage (Raft)
- Vault Audit Logs
- Cloud KMS for Auto-Unseal

## Data flows
- developer → vault-cli
- platform-engineer → vault-cli
- app-user → client-app-1
- client-app-1 → aws-lb
- vault-cli → vpn-gateway
- vpn-gateway → aws-lb
- aws-lb → eks-cluster
- k8s-service-vault-internal → vault-ha-statefulset
- eks-cluster → k8s-service-vault-internal
- vault-ha-statefulset → vault-api
- vault-api → vault-auth-methods
- vault-api → vault-secret-engines
- vault-api → vault-audit-devices
- vault-ha-statefulset → vault-raft-storage
- vault-ha-statefulset → vault-auto-unseal
- vault-audit-devices → vault-audit-logs
- vault-auto-unseal → cloud-kms
- developer → vpn-gateway
- platform-engineer → vpn-gateway
- vault-audit-devices → vault-audit-logs
- vault-audit-logs → developer
- vault-audit-logs → platform-engineer
- vault-raft-storage → developer
- vault-raft-storage → platform-engineer

## Trust zones
- Public Internet Zone
- Internal AWS VPC
- EKS Cluster Zone
- Vault Kubernetes Namespace