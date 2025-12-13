# README.md
# SocatLib v2.0.0

Advanced asynchronous Python library for network communication using socat.

## Installation
```bash
pip install SocatLib
```

## Quick Start
```python
import asyncio
from SocatLib import sending, listening

async def main():
    server = await listening(4444)
    await asyncio.sleep(1)
    
    result = await sending("Hello Server", "127.0.0.1", 4444)
    print(result)
    
    server.terminate()

asyncio.run(main())
```

## Features

- Async/await support
- Error handling with detailed messages
- 5 second timeout on all operations
- File transfer support
- Reverse shell capability
- OpenSSL encryption support
- Easy integration into existing projects

## API Reference

### sending(msg, ip, port)
Send a message to a server and get response.

### listening(port)
Start a listening server on specified port.

### send_file(file, ip, port)
Transfer a file to remote server.

### reverse_shell(attacker_ip, attacker_port)
Create reverse shell connection.

### encrypted_send(msg, ip, port)
Send encrypted message using OpenSSL.

### encrypted_listen(port)
Listen with encryption enabled.

### receive_file(port, save_path)
Receive file on specified port.

## Requirements

- Python 3.6+
- socat installed and in PATH

## Author

ash404.dev

## License

MIT License
