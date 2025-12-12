# django-aws-storage-28814

AWS configuration utilities for Python applications.

## Installation

```bash
pip install django-aws-storage-28814
```

## Usage

```python
from django_aws_storage_28814 import get_config, get_client

# Get AWS configuration
config = get_config()

# Get S3 client
s3 = get_client('s3')
```

## License

MIT
