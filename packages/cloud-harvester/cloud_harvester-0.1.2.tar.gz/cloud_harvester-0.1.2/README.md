## Cloud Harvester

Cloud-agnostic harvesting for AWS and Azure inventories. The `collect()` entry point fans out to built-in collectors across compute, containers/serverless, networking and edge, storage, databases, identity/security, and observability; limit scope with `providers` or inject your own boto3/Azure clients.

Every record is normalized into a `Resource` dataclass with fields like `id`, `provider`, `kind`, `resource` (service), `name`, `region`, `status`, `network_id`, `subnetwork_id`, `tags`, and the raw source payload for downstream use.

### Quickstart

```python
import boto3
from azure.identity import ClientSecretCredential
from cloud_harvester import collect

# AWS: static credentials (replace with real values)
aws_session = boto3.Session(
    aws_access_key_id="FAKEAWSACCESSKEY123",
    aws_secret_access_key="FAKEAWSSECRETKEY456",
    region_name="us-east-1",
)

# Azure: service principal credentials (replace with real values)
azure_credential = ClientSecretCredential(
    tenant_id="00000000-0000-0000-0000-000000000000",
    client_id="11111111-1111-1111-1111-111111111111",
    client_secret="fake-azure-client-secret",
)
azure_subscription_id = "22222222-2222-2222-2222-222222222222"

# Collect from both providers with injected sessions/credentials
resources = collect(
    providers=["aws", "azure"],
    aws_session=aws_session,
    azure_credential=azure_credential,
    azure_subscription_id=azure_subscription_id,
)

for res in resources:
    print(res.to_dict())
```

### Credentials

- **AWS**: In the AWS console, create or reuse an IAM role/user with read permissions. Minimum managed policies to attach:
  - `ReadOnlyAccess`
  - `AmazonEC2ReadOnlyAccess`
  - `AmazonEKSMCPReadOnlyAccess`
  Generate access keys, then either:
  - Export `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` (if temporary credentials), or
  - Store them in an `AWS_PROFILE` and point `AWS_PROFILE`/`CLOUD_HARVESTER_AWS_PROFILE` at it.
  Optionally set `AWS_REGION`/`CLOUD_HARVESTER_AWS_REGION` to control default regions.

- **Azure**: Create an App Registration (service principal) in Microsoft Entra ID and assign it the required RBAC roles on your subscription (Reader, Security Reader, Key Vault Reader). Capture:
  - `tenant_id`, `client_id`, `client_secret` from the service principal
  - `subscription_id` for the target subscription
  If Azure AD collectors are needed, add Microsoft Graph app permissions (e.g., `Directory.Read.All`) and have an admin grant consent.  
  Either set `AZURE_SUBSCRIPTION_ID` / `AZURE_TENANT_ID` (or `CLOUD_HARVESTER_*`) or pass a `ClientSecretCredential` created from these values.
