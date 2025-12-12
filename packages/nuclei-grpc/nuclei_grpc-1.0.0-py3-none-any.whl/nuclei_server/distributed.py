# -*- coding: utf-8 -*-
import threading
import time
import logging
from datetime import datetime
from typing import Dict, Tuple
import socket

logger = logging.getLogger(__name__)

class ChildNode:
    """Represents a child node connected to master"""
    def __init__(self, node_id: str, host: str, port: int):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.ip_address = host
        self.last_heartbeat = datetime.now()
        self.status = "unknown"
        self.available = True
        self.cpu_usage = 0.0
        self.memory_usage = 0.0
        self.active_connections = 0
        self.total_commands = 0
        self.uptime_seconds = 0
        self.connections = 0

    def update_heartbeat(self, status: str, cpu: float, memory: float, connections: int):
        """Update child node status from heartbeat"""
        self.last_heartbeat = datetime.now()
        self.status = status
        self.cpu_usage = cpu
        self.memory_usage = memory
        self.active_connections = connections
        self.connections = connections
        self.available = True

    def is_stale(self, timeout_seconds: int = 30) -> bool:
        """Check if node hasn't reported in timeout period"""
        elapsed = (datetime.now() - self.last_heartbeat).total_seconds()
        return elapsed > timeout_seconds

    def is_healthy(self) -> bool:
        """Check if node is healthy (available and not stale)"""
        return self.available and not self.is_stale()

    @property
    def uptime(self) -> str:
        """Return formatted uptime string"""
        hours = self.uptime_seconds // 3600
        minutes = (self.uptime_seconds % 3600) // 60
        return f"{hours}h {minutes}m"

    def __str__(self):
        uptime_str = f"{self.uptime_seconds // 3600}h {(self.uptime_seconds % 3600) // 60}m"
        return (
            f"Node: {self.node_id:<15} | "
            f"Address: {self.host}:{self.port} | "
            f"Status: {self.status:<8} | "
            f"Available: {'✓' if self.available else '✗'} | "
            f"CPU: {self.cpu_usage:>5.1f}% | "
            f"Memory: {self.memory_usage:>6.1f}% | "
            f"Connections: {self.active_connections:>2} | "
            f"Uptime: {uptime_str}"
        )


class MasterNode:
    """Master node that tracks and monitors child nodes"""
    def __init__(self, host: str = "0.0.0.0", port: int = 50052):
        self.host = host
        self.port = port
        self.children: Dict[str, ChildNode] = {}
        self.lock = threading.RLock()
        self.running = False
        self.display_thread = None
        logger.info(f"Master initialized on {host}:{port}")

    def register_child(self, node_id: str, host: str, port: int) -> bool:
        """Register a new child node"""
        with self.lock:
            if node_id in self.children:
                logger.warning(f"Child {node_id} already registered")
                return False
            
            child = ChildNode(node_id, host, port)
            self.children[node_id] = child
            logger.info(f"Child node registered: {node_id} at {host}:{port}")
            return True

    def heartbeat(self, node_id: str, status: str, cpu: float, memory: float, connections: int, uptime: int) -> bool:
        """Receive heartbeat from child node"""
        with self.lock:
            if node_id not in self.children:
                logger.warning(f"Heartbeat from unknown child: {node_id}")
                return False
            
            child = self.children[node_id]
            child.update_heartbeat(status, cpu, memory, connections)
            child.uptime_seconds = uptime
            child.total_commands += 1
            return True

    def check_stale_nodes(self, timeout: int = 30):
        """Mark nodes as unavailable if they haven't reported recently"""
        with self.lock:
            for node_id, child in self.children.items():
                if child.is_stale(timeout):
                    if child.available:
                        child.available = False
                        logger.warning(f"Node {node_id} marked as unavailable (no heartbeat for {timeout}s)")

    def get_children_status(self) -> str:
        """Get formatted status of all children"""
        with self.lock:
            if not self.children:
                return "No child nodes registered yet"
            
            output = []
            output.append("\n" + "=" * 180)
            output.append(f"Master Node Status - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            output.append("=" * 180)
            output.append(f"Total Children: {len(self.children)} | Available: {sum(1 for c in self.children.values() if c.available)}")
            output.append("-" * 180)
            
            for node_id, child in sorted(self.children.items()):
                output.append(str(child))
            
            output.append("=" * 180)
            return "\n".join(output)

    def start_display_loop(self, refresh_interval: int = 5):
        """Start continuous display of child status"""
        self.running = True
        self.display_thread = threading.Thread(target=self._display_loop, args=(refresh_interval,), daemon=True)
        self.display_thread.start()

    def _display_loop(self, refresh_interval: int):
        """Continuously display status"""
        try:
            while self.running:
                # Check for stale nodes
                self.check_stale_nodes()
                
                # Clear screen and print status
                import os
                os.system('clear' if os.name != 'nt' else 'cls')
                print(self.get_children_status())
                
                time.sleep(refresh_interval)
        except KeyboardInterrupt:
            logger.info("Display loop interrupted")
            self.stop()

    def stop(self):
        """Stop the master"""
        self.running = False
        if self.display_thread and self.display_thread.is_alive():
            self.display_thread.join(timeout=2)

    def get_available_children(self) -> list:
        """Get list of available child nodes"""
        with self.lock:
            return [child for child in self.children.values() if child.available]

    def get_child_by_id(self, node_id: str) -> ChildNode:
        """Get specific child node"""
        with self.lock:
            return self.children.get(node_id)
