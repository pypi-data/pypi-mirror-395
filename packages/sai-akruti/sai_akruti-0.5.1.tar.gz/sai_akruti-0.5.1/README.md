# sai-akruti

**Centralized, flexible settings loader for Python apps using Pydantic v2.x.**

This library provides a reusable, extensible settings system with built-in support for:
- Multiple `.env` files
- AWS Systems Manager (SSM) Parameter Store
- AWS Secrets Manager
- Standard environment variables and secret files (handled via Pydantic automatically)

It’s designed for clean separation of settings logic and allows each app to define its own settings hierarchy, source priorities, and overrides.

---

## ✅ Features
- Compatible with **Pydantic v2.x** (`pydantic-settings`).
- Automatically loads settings on instantiation — no manual `.load()` needed.
- Supports per-environment configuration (`dev`, `prod`, etc.).
- Easy to extend for other sources (YAML, remote config, etc.).
- Production-safe and future-proof.

---

## ✅ Installation

```bash
pip install sai-akruti
```

--- 

## ✅ AWS Credentials & IAM Permissions (Required)

This library can also use AWS Systems Manager (SSM) Parameter Store and AWS Secrets Manager for secure configuration.
**Required IAM Permissions:**

Ensure your environment (developer machine, Lambda, EC2, ECS, etc.) has the following IAM permissions:

```bash
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParametersByPath",
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "*"
    }
  ]
}
```

**Best Practice**: In production, restrict the "Resource" field to specific parameter/secret ARNs.

✅ **How Credentials Are Provided:**

This library uses boto3's standard credential chain:
- Environment Variables(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, etc.)
- ~/.aws/credentials or configured profiles (via aws configure).
- IAM Role on EC2, Lambda, or ECS (via Instance Metadata Service).
- AWS CLI SSO or other advanced credential providers.

**Usage in Lambda Functions**:

When used in an AWS Lambda function:
- Assign an IAM Role to your Lambda function with the above permissions.
- No manual credential configuration is needed—boto3 automatically uses the Lambda’s IAM Role.
- Example IAM Policy for Lambda:

```bash
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParametersByPath",
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:ssm:REGION:ACCOUNT_ID:parameter/your-prefix/*"
    }
  ]
}
```

**How to retrieve AWS Account ID:**

To retrieve the AWS Account ID in your code:

```python
import boto3
account_id = boto3.client("sts").get_caller_identity()["Account"]
```

**How to release to PyPI manually:**
To release a new version to PyPI, follow these steps:
1. Update the version in `pyproject.toml`.
2. Build the package:
   ```bash
   python -m build
   ```
3. Upload to PyPI:
   ```bash
    python publish
    ```

--------------
*Special Note:*
- For SSM, if the parameter is defined as a String or SecretString and is a dict 
  which has "keyName" as one of its keys, then it will be used as the key for the settings. 
  Otherwise, the dictionary will be unpacked and each key will be used as a setting.

