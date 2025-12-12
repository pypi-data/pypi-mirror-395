# async-temp-email

[![PyPI version](https://img.shields.io/pypi/v/async-temp-email.svg)](https://pypi.org/project/async-temp-email/)
[![Python Version](https://img.shields.io/pypi/pyversions/async-temp-email.svg)](https://pypi.org/project/async-temp-email/)

## Overview

`async-temp-email` is an asynchronous Python library for working with temporary email services. It allows you to easily generate disposable email addresses, fetch messages, and poll for incoming emails in real-time.

This library supports a modular design, enabling integration with multiple temporary email providers. Currently supported provider:

- `Emailnator`

## Features

- Asynchronous API for generating temporary email addresses
- Fetch messages for a given mailbox
- Retrieve individual message content
- Real-time polling of incoming emails
- Easy integration with multiple providers via a registry-based client system

## Installation

```bash
pip install async-temp-email
```

## Usage

### Create a client

```python
from async_temp_email import TempEmailClient

# Initialize a provider client
client = TempEmailClient.create("emailnator", timeout=30, retries=3)

async with TempEmailClient.create("emailnator", timeout=30, retries=3) as client: # Recommended
    ...
```

### Generate a temporary email

```python
from pydantic import EmailStr

email: EmailStr = await client.service.get_email()
print(email)
```

### Fetch messages

```python
messages = await client.service.get_messages(email)
for msg in messages:
    print(msg.message_subject, msg.message_content)
```

### Poll for new messages

```python
async with client.polling(email=email, poll_interval=5, skip_existing=False) as poller:
    async for message in poller:
        print(message.message_subject, message.message_content)
```

## License

Code and documentation copyright 2025-2026. Code released under the [MIT License](https://github.com/lionex-ui/async-temp-email/blob/main/LICENSE).

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to fork the repository and submit a pull request.

## Links

- PyPI: [https://pypi.org/project/async-temp-email/](https://pypi.org/project/async-temp-email/)
- Repository: [https://github.com/lionex-ui/async-temp-email](https://github.com/lionex-ui/async-temp-email/)

