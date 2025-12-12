# -*- coding: utf-8 -*-
import subprocess
import sys
from typing import Generator, Tuple

class CommandExecutor:
    def __init__(self, work_dir: str = "/tmp"):
        self.work_dir = work_dir
    
    def execute(self, command: str, env_vars: dict = None) -> Generator[Tuple[str, str, int], None, None]:
        """
        Execute command and yield output/error line by line
        Yields: (output, error, exit_code)
        """
        if env_vars is None:
            env_vars = {}
        
        import os
        env = os.environ.copy()
        env.update(env_vars)
        
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.work_dir,
                env=env,
                bufsize=1
            )
            
            # Stream stdout
            for line in process.stdout:
                if line:
                    yield (line.rstrip('\n'), "", 0)
            
            # Stream stderr
            for line in process.stderr:
                if line:
                    yield ("", line.rstrip('\n'), 0)
            
            # Wait for process to finish
            exit_code = process.wait()
            
            # Final message with exit code
            yield ("", "", exit_code)
            
        except Exception as e:
            yield ("", str(e), 1)
