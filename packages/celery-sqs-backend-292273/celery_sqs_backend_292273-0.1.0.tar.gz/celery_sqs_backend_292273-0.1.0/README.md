# celery-sqs-backend-292273

AWS configuration utilities for Python applications.

## Installation

```bash
pip install celery-sqs-backend-292273
```

## Usage

```python
from celery_sqs_backend_292273 import get_config, get_client

# Get AWS configuration
config = get_config()

# Get S3 client
s3 = get_client('s3')
```

## License

MIT
