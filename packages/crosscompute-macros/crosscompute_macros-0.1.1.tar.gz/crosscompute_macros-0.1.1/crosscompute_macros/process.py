import asyncio
import subprocess


async def run_process(args, cwd=None, env=None, text=None, check=False):
    p = await asyncio.create_subprocess_exec(
        *args,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    return_code = await p.wait()
    if check and return_code:
        stdout = await p.stdout.read()
        stderr = await p.stderr.read()
        raise subprocess.CalledProcessError(
            returncode=return_code,
            cmd=args,
            output=stdout.decode() if text else stdout,
            stderr=stderr.decode() if text else stderr)
    return p
