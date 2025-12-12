# -*- coding: utf-8 -*-
import logging
import os
import io
from pathlib import Path
from typing import Iterator

import grpc
from nuclei_server import nuclei_pb2, nuclei_pb2_grpc
from nuclei_server.auth import AuthManager
from nuclei_server.executor import CommandExecutor
from nuclei_server.distributed import MasterNode
from nuclei_server.web_ui import run_web_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NucleiServicer(nuclei_pb2_grpc.AuthServicer,
                     nuclei_pb2_grpc.NucleiExecutorServicer,
                     nuclei_pb2_grpc.FileTransferServicer,
                     nuclei_pb2_grpc.DiscoveryServicer):
    """Implements all gRPC services"""
    
    def __init__(self, auth_manager: AuthManager, executor: CommandExecutor, upload_dir: str, master_node: 'MasterNode' = None):
        self.auth_manager = auth_manager
        self.executor = executor
        self.upload_dir = upload_dir
        self.master_node = master_node
        
        # Create upload directory if it doesn't exist
        os.makedirs(upload_dir, exist_ok=True)
    
    # ==================== Auth Service ====================
    
    def Login(self, request: nuclei_pb2.LoginRequest, context):
        """Authenticate user and return token"""
        logger.info(f"Login attempt for user: {request.username}")
        
        token = self.auth_manager.authenticate(request.username, request.password)
        if not token:
            return nuclei_pb2.LoginResponse(
                success=False,
                message="Invalid credentials"
            )
        
        logger.info(f"Login successful for user: {request.username}")
        return nuclei_pb2.LoginResponse(
            success=True,
            token=token,
            message="Login successful"
        )
    
    def Validate(self, request: nuclei_pb2.ValidateRequest, context):
        """Validate authentication token"""
        username = self.auth_manager.validate_token(request.token)
        if not username:
            return nuclei_pb2.ValidateResponse(valid=False)
        
        return nuclei_pb2.ValidateResponse(valid=True, username=username)
    
    # ==================== Nuclei Executor Service ====================
    
    def ExecuteCommand(self, request: nuclei_pb2.ExecuteRequest, context) -> Iterator[nuclei_pb2.ExecuteResponse]:
        """Execute command and stream results"""
        # Validate token
        username = self.auth_manager.validate_token(request.token)
        if not username:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
        
        logger.info(f"User {username} executing command: {request.command}")
        
        try:
            for output, error, exit_code in self.executor.execute(request.command, dict(request.env_vars)):
                yield nuclei_pb2.ExecuteResponse(
                    output=output,
                    error=error,
                    exit_code=exit_code,
                    completed=(exit_code != 0 or (not output and not error))
                )
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    # ==================== File Transfer Service ====================
    
    def UploadFile(self, request_iterator: Iterator[nuclei_pb2.UploadRequest], context) -> nuclei_pb2.UploadResponse:
        """Upload file from client"""
        filename = ""
        file_data = io.BytesIO()
        token = ""
        
        try:
            for request in request_iterator:
                # Validate token on first request
                if not token:
                    token = request.token
                    username = self.auth_manager.validate_token(token)
                    if not username:
                        context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
                    logger.info(f"User {username} uploading file: {request.filename}")
                
                if not filename:
                    filename = request.filename
                
                file_data.write(request.data)
            
            # Save file
            file_path = os.path.join(self.upload_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(file_data.getvalue())
            
            logger.info(f"File uploaded successfully: {file_path}")
            return nuclei_pb2.UploadResponse(
                success=True,
                message="File uploaded successfully",
                file_path=file_path
            )
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            return nuclei_pb2.UploadResponse(
                success=False,
                message=str(e)
            )
    
    def DownloadFile(self, request: nuclei_pb2.DownloadRequest, context) -> Iterator[nuclei_pb2.DownloadResponse]:
        """Download file to client"""
        # Validate token
        username = self.auth_manager.validate_token(request.token)
        if not username:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
        
        logger.info(f"User {username} downloading file: {request.filename}")
        
        try:
            # Prevent directory traversal
            file_path = os.path.normpath(os.path.join(self.upload_dir, request.filename))
            if not file_path.startswith(os.path.normpath(self.upload_dir)):
                context.abort(grpc.StatusCode.PERMISSION_DENIED, "Access denied")
            
            if not os.path.exists(file_path):
                context.abort(grpc.StatusCode.NOT_FOUND, "File not found")
            
            # Stream file in chunks
            chunk_size = 64 * 1024  # 64KB chunks
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    
                    yield nuclei_pb2.DownloadResponse(
                        data=chunk,
                        filename=request.filename,
                        completed=False
                    )
            
            # Final message
            yield nuclei_pb2.DownloadResponse(
                data=b'',
                filename=request.filename,
                completed=True
            )
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    def ListFiles(self, request: nuclei_pb2.ListFilesRequest, context) -> nuclei_pb2.ListFilesResponse:
        """List files in directory"""
        # Validate token
        username = self.auth_manager.validate_token(request.token)
        if not username:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
        
        try:
            dir_path = self.upload_dir
            if request.directory:
                dir_path = os.path.join(self.upload_dir, request.directory)
            
            if not os.path.exists(dir_path):
                context.abort(grpc.StatusCode.NOT_FOUND, "Directory not found")
            
            files = []
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                stat = os.stat(item_path)
                
                files.append(nuclei_pb2.FileInfo(
                    name=item,
                    size=stat.st_size,
                    is_dir=os.path.isdir(item_path),
                    modified_time=int(stat.st_mtime)
                ))
            
            return nuclei_pb2.ListFilesResponse(files=files)
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            context.abort(grpc.StatusCode.INTERNAL, str(e))
    
    # ==================== Discovery Service ====================
    
    def RegisterChild(self, request: nuclei_pb2.RegisterRequest, context):
        """Register child node with master"""
        if not self.master_node:
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, "This is not a master node")
        
        success = self.master_node.register_child(request.node_id, request.host, request.port)
        return nuclei_pb2.RegisterResponse(
            success=success,
            message="Registration successful" if success else "Node already registered"
        )
    
    def Heartbeat(self, request: nuclei_pb2.HeartbeatRequest, context):
        """Receive heartbeat from child node"""
        if not self.master_node:
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, "This is not a master node")
        
        success = self.master_node.heartbeat(
            request.node_id,
            request.status,
            request.cpu_usage,
            request.memory_usage,
            request.active_connections,
            request.uptime_seconds
        )
        return nuclei_pb2.HeartbeatResponse(
            received=success,
            message="Heartbeat received" if success else "Unknown node"
        )


def serve(mode: str = "standalone", master_addr: str = None, node_id: str = None):
    """Start the gRPC server
    
    Args:
        mode: "standalone", "master", or "child"
        master_addr: "host:port" for child mode
        node_id: unique identifier for child node
    """
    from concurrent import futures
    
    # Initialize authentication and executor
    auth_manager = AuthManager()
    auth_manager.add_user("admin", "admin123")
    auth_manager.add_user("user", "user123")
    
    executor = CommandExecutor("/tmp")
    
    master_node = None
    child_mode = None
    
    # Create server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    if mode == "master":
        # Master mode: listen for child heartbeats
        logger.info("=" * 70)
        logger.info("MASTER MODE - Listening for child nodes")
        logger.info("=" * 70)
        master_node = MasterNode("0.0.0.0", 50052)
        servicer = NucleiServicer(auth_manager, executor, "/tmp/uploads", master_node)
        
        nuclei_pb2_grpc.add_AuthServicer_to_server(servicer, server)
        nuclei_pb2_grpc.add_NucleiExecutorServicer_to_server(servicer, server)
        nuclei_pb2_grpc.add_FileTransferServicer_to_server(servicer, server)
        nuclei_pb2_grpc.add_DiscoveryServicer_to_server(servicer, server)
        
        server.add_insecure_port("[::]:50052")
        logger.info("Master listening on port 50052 for child connections")
        logger.info("Master will display child status updates below:")
        
        server.start()
        
        # Start web UI server
        logger.info("Starting web UI on http://0.0.0.0:5000")
        logger.info("Credentials: admin / avis12345")
        run_web_server(master_node, port=5000)
        
        # Start master display loop
        master_node.start_display_loop(refresh_interval=5)
        
        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            logger.info("Master shutting down...")
            master_node.stop()
            server.stop(0)
    
    elif mode == "child":
        # Child mode: connect to master and report status
        if not master_addr or not node_id:
            raise ValueError("Child mode requires --master and --node-id arguments")
        
        try:
            master_host, master_port = master_addr.split(":")
            master_port = int(master_port)
        except:
            raise ValueError(f"Invalid master address format: {master_addr} (use host:port)")
        
        logger.info("=" * 70)
        logger.info("CHILD MODE - Connecting to master")
        logger.info("=" * 70)
        logger.info(f"Node ID: {node_id}")
        logger.info(f"Master: {master_host}:{master_port}")
        logger.info("=" * 70)
        
        from nuclei_server.child_mode import ChildMode
        
        # Start child mode
        child_mode = ChildMode(node_id, master_host, master_port, 50051)
        child_mode.start_heartbeat(interval=5)
        
        # Start server (still serves gRPC for commands)
        servicer = NucleiServicer(auth_manager, executor, "/tmp/uploads")
        nuclei_pb2_grpc.add_AuthServicer_to_server(servicer, server)
        nuclei_pb2_grpc.add_NucleiExecutorServicer_to_server(servicer, server)
        nuclei_pb2_grpc.add_FileTransferServicer_to_server(servicer, server)
        nuclei_pb2_grpc.add_DiscoveryServicer_to_server(servicer, server)
        
        server.add_insecure_port("[::]:50051")
        logger.info("Child node gRPC server listening on port 50051")
        
        server.start()
        
        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            logger.info("Child node shutting down...")
            child_mode.stop()
            server.stop(0)
    
    else:
        # Standalone mode (default)
        servicer = NucleiServicer(auth_manager, executor, "/tmp/uploads")
        nuclei_pb2_grpc.add_AuthServicer_to_server(servicer, server)
        nuclei_pb2_grpc.add_NucleiExecutorServicer_to_server(servicer, server)
        nuclei_pb2_grpc.add_FileTransferServicer_to_server(servicer, server)
        nuclei_pb2_grpc.add_DiscoveryServicer_to_server(servicer, server)
        
        server.add_insecure_port("[::]:50051")
        
        logger.info("Nuclei gRPC Server starting in STANDALONE mode on port 50051")
        logger.info("Default credentials: admin/admin123 or user/user123")
        
        server.start()
        server.wait_for_termination()


def main():
    """Entry point for console script"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Nuclei gRPC Server")
    parser.add_argument("--mode", choices=["standalone", "master", "child"], 
                       default="standalone",
                       help="Server mode (default: standalone)")
    parser.add_argument("--master", dest="master_addr",
                       help="Master address (host:port) for child mode")
    parser.add_argument("--node-id",
                       help="Node ID for child mode")
    
    args = parser.parse_args()
    
    serve(mode=args.mode, master_addr=args.master_addr, node_id=args.node_id)


if __name__ == "__main__":
    main()
