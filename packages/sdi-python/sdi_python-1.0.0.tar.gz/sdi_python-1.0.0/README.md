# SDI Python SDK

Synthetic Digital Immunity SDK for Python - AI-powered cybersecurity for microservices.

## Installation

```bash
pip install sdi-python
```

## Quick Start

```python
from sdi import SdiClient

client = SdiClient(api_key=os.getenv('SDI_API_KEY'))

analysis = client.analyze(
    method='GET',
    path='/api/users/123',
    headers={},
    service_id='my-service'
)

if analysis['anomaly_detected']:
    print(f'Anomaly detected: {analysis["anomaly_score"]}')
```

## Documentation

Full documentation: https://github.com/skesani/sdi

## License

Apache-2.0

