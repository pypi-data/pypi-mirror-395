# setup.py
from setuptools import setup, find_packages

setup(
    name="SocatLib",
    version="2.0.0",
    description="Async Python library for network communication using socat",
    long_description="""
# SocatLib v2.0.0

Advanced async Python library for network communication using socat.

## Features

- Asynchronous operations (async/await)
- Strong error handling
- Timeout protection (5 seconds default)
- File transfer
- Reverse shell
- Encrypted communication (OpenSSL)
- Easy to integrate into any project

## Installation
```bash
pip install SocatLib
```

## Usage
```python
import asyncio
from SocatLib import sending, listening

async def main():
    server = await listening(4444)
    await asyncio.sleep(1)
    
    result = await sending("Hello", "127.0.0.1", 4444)
    print(result)
    
    server.terminate()

asyncio.run(main())
```

## Functions

1. **sending(msg, ip, port)** - Send message and get response
2. **listening(port)** - Start server on port
3. **send_file(file, ip, port)** - Transfer file
4. **reverse_shell(attacker_ip, attacker_port)** - Reverse shell
5. **encrypted_send(msg, ip, port)** - Send encrypted message
6. **encrypted_listen(port)** - Listen with encryption
7. **receive_file(port, save_path)** - Receive file

## Requirements

- Python 3.6+
- socat

## License

MIT

## Author

ash404.dev
""",
    long_description_content_type="text/markdown",
    author="ash404.dev",
    author_email="momoh70070@gmail.com",
    url="https://github.com/yourname/SocatLib",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
)