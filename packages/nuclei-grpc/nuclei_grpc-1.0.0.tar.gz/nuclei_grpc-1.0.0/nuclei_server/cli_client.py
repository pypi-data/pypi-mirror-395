#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI Client for Nuclei gRPC Server
Entry point for nuclei-client console script
"""

import argparse
import sys
import os
from pathlib import Path

import grpc
from nuclei_server import nuclei_pb2, nuclei_pb2_grpc


class NucleiClient:
    def __init__(self, host: str, port: int):
        self.channel = grpc.aio.secure_channel(
            f"{host}:{port}",
            grpc.ssl_channel_credentials()
        ) if False else grpc.insecure_channel(f"{host}:{port}")
        
        self.auth_stub = nuclei_pb2_grpc.AuthStub(self.channel)
        self.executor_stub = nuclei_pb2_grpc.NucleiExecutorStub(self.channel)
        self.file_stub = nuclei_pb2_grpc.FileTransferStub(self.channel)
        self.token = None
    
    def login(self, username: str, password: str) -> bool:
        """Login and obtain token"""
        try:
            response = self.auth_stub.Login(
                nuclei_pb2.LoginRequest(username=username, password=password)
            )
            
            if response.success:
                self.token = response.token
                print(f"✓ Login successful for user: {username}")
                return True
            else:
                print(f"✗ Login failed: {response.message}")
                return False
        except grpc.RpcError as e:
            print(f"✗ Error: {e.details()}")
            return False
    
    def validate_token(self) -> bool:
        """Validate current token"""
        if not self.token:
            print("✗ No token available")
            return False
        
        try:
            response = self.auth_stub.Validate(nuclei_pb2.ValidateRequest(token=self.token))
            if response.valid:
                print(f"✓ Token valid for user: {response.username}")
                return True
            else:
                print("✗ Token invalid or expired")
                return False
        except grpc.RpcError as e:
            print(f"✗ Error: {e.details()}")
            return False
    
    def execute_command(self, command: str, env_vars: dict = None):
        """Execute command on remote server"""
        if not self.token:
            print("✗ Not authenticated. Run 'login' first.")
            return
        
        try:
            env_vars = env_vars or {}
            responses = self.executor_stub.ExecuteCommand(
                nuclei_pb2.ExecuteRequest(
                    token=self.token,
                    command=command,
                    env_vars=env_vars
                )
            )
            
            print(f"$ {command}\n")
            for response in responses:
                if response.output:
                    print(response.output, end="")
                if response.error:
                    print(f"[ERROR] {response.error}", end="")
            
            print(f"\n[Exit Code: {response.exit_code}]")
        except grpc.RpcError as e:
            print(f"✗ Error: {e.details()}")
    
    def upload_file(self, local_path: str, remote_name: str = None):
        """Upload file to server"""
        if not self.token:
            print("✗ Not authenticated")
            return
        
        if not os.path.exists(local_path):
            print(f"✗ File not found: {local_path}")
            return
        
        remote_name = remote_name or os.path.basename(local_path)
        
        try:
            def upload_generator():
                with open(local_path, "rb") as f:
                    # Send metadata first
                    yield nuclei_pb2.UploadRequest(
                        token=self.token,
                        filename=remote_name
                    )
                    
                    # Send file chunks
                    while True:
                        chunk = f.read(65536)  # 64KB chunks
                        if not chunk:
                            break
                        yield nuclei_pb2.UploadRequest(data=chunk)
            
            response = self.file_stub.UploadFile(upload_generator())
            if response.success:
                print(f"✓ File uploaded: {remote_name} ({response.size} bytes)")
            else:
                print(f"✗ Upload failed: {response.message}")
        except grpc.RpcError as e:
            print(f"✗ Error: {e.details()}")
    
    def download_file(self, remote_path: str, local_path: str = None):
        """Download file from server"""
        if not self.token:
            print("✗ Not authenticated")
            return
        
        local_path = local_path or os.path.basename(remote_path)
        
        try:
            responses = self.file_stub.DownloadFile(
                nuclei_pb2.DownloadRequest(token=self.token, file_path=remote_path)
            )
            
            with open(local_path, "wb") as f:
                total_size = 0
                for response in responses:
                    f.write(response.data)
                    total_size += len(response.data)
            
            print(f"✓ File downloaded: {local_path} ({total_size} bytes)")
        except grpc.RpcError as e:
            print(f"✗ Error: {e.details()}")
    
    def list_files(self, directory: str = ""):
        """List files in directory"""
        if not self.token:
            print("✗ Not authenticated")
            return
        
        try:
            response = self.file_stub.ListFiles(
                nuclei_pb2.ListRequest(token=self.token, directory=directory)
            )
            
            print(f"\nDirectory: {directory or '/'}\n")
            for file_info in response.files:
                file_type = "DIR " if file_info.is_directory else "FILE"
                print(f"{file_type} {file_info.name:<50} {file_info.size:>10} bytes")
        except grpc.RpcError as e:
            print(f"✗ Error: {e.details()}")
    
    def close(self):
        """Close connection"""
        self.channel.close()


def main():
    """Main entry point for CLI"""
    parser = argparse.ArgumentParser(description="Nuclei gRPC Client")
    parser.add_argument("--host", default="localhost", help="Server host (default: localhost)")
    parser.add_argument("--port", type=int, default=50051, help="Server port (default: 50051)")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Login command
    login_parser = subparsers.add_parser("login", help="Login to server")
    login_parser.add_argument("-u", "--username", required=True, help="Username")
    login_parser.add_argument("-p", "--password", required=True, help="Password")
    
    # Validate command
    subparsers.add_parser("validate", help="Validate token")
    
    # Execute command
    exec_parser = subparsers.add_parser("exec", help="Execute command")
    exec_parser.add_argument("--cmd", required=True, help="Command to execute")
    exec_parser.add_argument("--env", nargs=2, action="append", help="Environment variables (key value)")
    
    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload file")
    upload_parser.add_argument("--file", required=True, help="Local file path")
    upload_parser.add_argument("--as", dest="remote_name", help="Remote file name")
    
    # Download command
    download_parser = subparsers.add_parser("download", help="Download file")
    download_parser.add_argument("file", help="Remote file name")
    download_parser.add_argument("--to", dest="local_path", help="Local file path")
    
    # List files command
    list_parser = subparsers.add_parser("list", help="List files")
    list_parser.add_argument("--dir", default="", help="Directory to list")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    client = NucleiClient(args.host, args.port)
    
    try:
        if args.command == "login":
            client.login(args.username, args.password)
        
        elif args.command == "validate":
            client.validate_token()
        
        elif args.command == "exec":
            env_vars = {}
            if args.env:
                for key, value in args.env:
                    env_vars[key] = value
            client.execute_command(args.cmd, env_vars)
        
        elif args.command == "upload":
            client.upload_file(args.file, args.remote_name)
        
        elif args.command == "download":
            client.download_file(args.file, args.local_path)
        
        elif args.command == "list":
            client.list_files(args.dir)
    
    finally:
        client.close()


if __name__ == "__main__":
    main()
