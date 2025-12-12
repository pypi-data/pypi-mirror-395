# LM Cloud Sync - Terraform Modules

Terraform modules for managing LogicMonitor cloud integrations.

**Current Version:** v2.0.0 - Published to PyPI
**Package:** `pip install lm-cloud-sync`

## Available Modules

| Module | Description | Status |
|--------|-------------|--------|
| [gcp](./modules/gcp) | GCP project integrations | ✅ Available (v2.0.0) |
| [aws](./modules/aws) | AWS account integrations | 🚧 In Development (v2.1.0) |
| [azure](./modules/azure) | Azure subscription integrations | 🚧 In Development (v2.2.0) |

## GCP Module

Creates LogicMonitor device groups for GCP projects.

### Usage

```hcl
module "gcp_integrations" {
  source = "github.com/ryanmat/lm-cloud-sync//terraform/modules/gcp"

  lm_company                   = "your-company"
  lm_bearer_token              = var.lm_bearer_token
  gcp_service_account_key_path = "/path/to/service-account.json"

  # Option 1: Define projects inline
  projects = [
    {
      project_id   = "my-project-1"
      display_name = "My Project 1"
    },
    {
      project_id   = "my-project-2"
      display_name = "My Project 2"
    },
  ]

  # Option 2: Load from YAML file
  # projects_file = "projects.yaml"
}
```

### Variables

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| `lm_company` | LogicMonitor portal name | string | - | Yes |
| `lm_bearer_token` | LogicMonitor Bearer token | string | - | Yes |
| `gcp_service_account_key_path` | Path to GCP SA key JSON | string | - | Yes |
| `lm_parent_group_id` | Parent group ID | number | 1 | No |
| `projects` | List of projects to integrate | list | [] | No* |
| `projects_file` | Path to YAML file with projects | string | "" | No* |
| `python_command` | Python command to use | string | "python3" | No |

*Either `projects` or `projects_file` must be provided.

### Projects YAML Format

```yaml
projects:
  - project_id: my-gcp-project-1
    display_name: "Production Project"
  - project_id: my-gcp-project-2
    display_name: "Development Project"
```

### Outputs

| Name | Description |
|------|-------------|
| `managed_projects` | List of managed GCP project IDs |
| `project_count` | Number of managed projects |

## AWS Module

Creates LogicMonitor device groups for AWS accounts.

### Prerequisites

Before using this module, you must:

1. Create an IAM role in each AWS account with a trust policy allowing LogicMonitor to assume the role
2. The trust policy must include the external ID from LogicMonitor

### Usage

```hcl
module "aws_integrations" {
  source = "github.com/ryanmat/lm-cloud-sync//terraform/modules/aws"

  lm_company      = "your-company"
  lm_bearer_token = var.lm_bearer_token
  aws_role_name   = "LogicMonitorRole"

  # Option 1: Define accounts inline
  accounts = [
    {
      account_id   = "123456789012"
      display_name = "Production Account"
    },
    {
      account_id   = "234567890123"
      display_name = "Development Account"
    },
  ]

  # Option 2: Load from YAML file
  # accounts_file = "accounts.yaml"
}
```

### Variables

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| `lm_company` | LogicMonitor portal name | string | - | Yes |
| `lm_bearer_token` | LogicMonitor Bearer token | string | - | Yes |
| `aws_role_name` | IAM role name to assume | string | "LogicMonitorRole" | No |
| `lm_parent_group_id` | Parent group ID | number | 1 | No |
| `accounts` | List of AWS accounts | list | [] | No* |
| `accounts_file` | Path to YAML file with accounts | string | "" | No* |
| `auto_discover` | Use Organizations API | bool | false | No |
| `python_command` | Python command to use | string | "python3" | No |

*Either `accounts` or `accounts_file` must be provided (unless using auto_discover).

### Accounts YAML Format

```yaml
accounts:
  - account_id: "123456789012"
    display_name: "Production Account"
  - account_id: "234567890123"
    display_name: "Development Account"
```

### Outputs

| Name | Description |
|------|-------------|
| `managed_accounts` | List of managed AWS account IDs |
| `account_count` | Number of managed accounts |

### IAM Role Setup

Each AWS account needs an IAM role that LogicMonitor can assume:

1. Get the external ID from LogicMonitor: `lm-cloud-sync aws discover --auto-discover` (requires setup first)
2. Create an IAM role with the following trust policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::282028653949:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "YOUR_EXTERNAL_ID"
        }
      }
    }
  ]
}
```

3. Attach a policy with read-only permissions for the AWS services you want to monitor.

## Prerequisites

1. **lm-cloud-sync installed**:
   ```bash
   pip install lm-cloud-sync
   # or
   uv tool install lm-cloud-sync
   ```

2. **Cloud Provider Credentials**:
   - GCP: Service Account with Viewer role
   - AWS: IAM role with cross-account trust policy

3. **LogicMonitor API credentials** (Bearer token or LMv1)

## Examples

See the [examples](./examples) directory:

- [gcp-only](./examples/gcp-only) - Basic GCP integration

## How It Works

The modules use Terraform's `null_resource` with `local-exec` provisioners to:

1. **On Apply**: Runs `create_integration.py` to create LM device groups
2. **On Destroy**: Runs `delete_integration.py` to remove LM device groups

This approach allows Terraform to manage the lifecycle of LogicMonitor integrations while leveraging the lm-cloud-sync library for API communication.
