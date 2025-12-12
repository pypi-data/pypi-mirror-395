# -*- coding: utf-8 -*-
import threading
import time
import logging
import socket
import psutil
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

class ChildMode:
    """Child node that reports to master"""
    def __init__(self, node_id: str, master_host: str, master_port: int, local_port: int = 50051):
        self.node_id = node_id
        self.master_host = master_host
        self.master_port = master_port
        self.local_port = local_port
        self.local_host = self._get_local_ip()
        self.running = False
        self.heartbeat_thread = None
        self.start_time = datetime.now()
        logger.info(f"Child mode initialized: {node_id}")
        logger.info(f"  Master: {master_host}:{master_port}")
        logger.info(f"  Local: {self.local_host}:{local_port}")

    def _get_local_ip(self) -> str:
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def _get_system_stats(self) -> tuple:
        """Get CPU, memory, and connection stats"""
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory().percent
            connections = len(psutil.net_connections())
            return cpu, memory, connections
        except:
            return 0.0, 0.0, 0

    def _get_uptime(self) -> int:
        """Get uptime in seconds"""
        return int((datetime.now() - self.start_time).total_seconds())

    def start_heartbeat(self, interval: int = 5):
        """Start sending heartbeats to master"""
        self.running = True
        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            args=(interval,),
            daemon=True
        )
        self.heartbeat_thread.start()
        logger.info(f"Heartbeat started with {interval}s interval")

    def _heartbeat_loop(self, interval: int):
        """Send periodic heartbeats to master"""
        registered = False
        
        while self.running:
            try:
                import grpc
                from nuclei_server import nuclei_pb2, nuclei_pb2_grpc
                
                # First time: register with master
                if not registered:
                    channel = grpc.insecure_channel(f"{self.master_host}:{self.master_port}")
                    stub = nuclei_pb2_grpc.DiscoveryStub(channel)
                    
                    try:
                        response = stub.RegisterChild(nuclei_pb2.RegisterRequest(
                            node_id=self.node_id,
                            host=self.local_host,
                            port=self.local_port
                        ))
                        
                        if response.success:
                            logger.info(f"Registered with master: {response.message}")
                            registered = True
                        else:
                            logger.error(f"Registration failed: {response.message}")
                    except Exception as e:
                        logger.warning(f"Failed to register with master: {e}")
                    
                    channel.close()
                
                # Send heartbeat
                if registered:
                    channel = grpc.insecure_channel(f"{self.master_host}:{self.master_port}")
                    stub = nuclei_pb2_grpc.DiscoveryStub(channel)
                    
                    cpu, memory, connections = self._get_system_stats()
                    uptime = self._get_uptime()
                    
                    try:
                        response = stub.Heartbeat(nuclei_pb2.HeartbeatRequest(
                            node_id=self.node_id,
                            status="healthy",
                            cpu_usage=cpu,
                            memory_usage=memory,
                            active_connections=connections,
                            uptime_seconds=uptime
                        ))
                        
                        if response.received:
                            logger.debug(f"Heartbeat sent to master")
                        else:
                            logger.warning(f"Master rejected heartbeat: {response.message}")
                    except Exception as e:
                        logger.warning(f"Failed to send heartbeat: {e}")
                        registered = False
                    
                    channel.close()
                
                time.sleep(interval)
            
            except Exception as e:
                logger.error(f"Heartbeat loop error: {e}")
                time.sleep(interval)

    def stop(self):
        """Stop heartbeat"""
        self.running = False
        if self.heartbeat_thread and self.heartbeat_thread.is_alive():
            self.heartbeat_thread.join(timeout=2)
        logger.info("Child mode stopped")
