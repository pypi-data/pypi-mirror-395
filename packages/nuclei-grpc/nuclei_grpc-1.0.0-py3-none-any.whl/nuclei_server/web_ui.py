import threading
from flask import Flask, render_template, jsonify, request
from functools import wraps
from base64 import b64decode
import json
from datetime import datetime

# Credentials
ADMIN_USER = "admin"
ADMIN_PASS = "avis12345"


def create_web_app(master_node):
    """Create Flask app for web UI"""
    app = Flask(__name__, template_folder=None)
    app.master_node = master_node

    def check_auth(username, password):
        """Check if username/password is correct"""
        return username == ADMIN_USER and password == ADMIN_PASS

    def authenticate():
        """Sends a 401 response for basic auth"""
        return jsonify({"error": "Authentication required"}), 401, {
            "WWW-Authenticate": 'Basic realm="Login Required"'
        }

    def login_required(f):
        """Decorator for routes that require authentication"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return authenticate()
            return f(*args, **kwargs)
        return decorated_function

    @app.route("/")
    @login_required
    def dashboard():
        """Main dashboard HTML page"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Nuclei Master</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { width: 100%; height: 100%; }
        body { 
            font-family: 'Courier New', monospace; 
            background: #000; 
            color: #fff; 
            overflow: hidden;
            letter-spacing: 0.5px;
        }
        .wrapper { 
            display: flex; 
            flex-direction: column; 
            height: 100vh; 
        }
        .header { 
            padding: 16px 24px; 
            border-bottom: 2px solid #fff; 
            background: #000;
        }
        .header h1 { 
            font-size: 18px; 
            font-weight: bold; 
            letter-spacing: 2px;
        }
        .header p { 
            font-size: 11px; 
            color: #888; 
            margin-top: 4px;
        }
        .container { 
            flex: 1; 
            overflow-y: auto; 
            padding: 20px 24px; 
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 16px;
            grid-auto-rows: max-content;
        }
        .container::-webkit-scrollbar { width: 6px; }
        .container::-webkit-scrollbar-track { background: #000; }
        .container::-webkit-scrollbar-thumb { background: #333; }
        .card { 
            background: #000; 
            border: 1px solid #fff; 
            padding: 16px; 
            display: flex;
            flex-direction: column;
        }
        .card-title { 
            font-size: 14px; 
            font-weight: bold; 
            margin-bottom: 12px; 
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .status-badge { 
            display: inline-block; 
            width: 6px; 
            height: 6px; 
            margin: 0;
        }
        .status-badge.online { background: #00ff00; }
        .status-badge.offline { background: #ff0000; }
        .stat { 
            display: flex; 
            justify-content: space-between; 
            padding: 6px 0; 
            font-size: 11px;
            border-bottom: 1px solid #222;
        }
        .stat:last-child { border-bottom: none; }
        .stat-label { color: #888; }
        .stat-value { font-weight: bold; }
        .status-online { color: #00ff00; }
        .status-offline { color: #ff0000; }
        .progress-container { 
            margin: 4px 0 8px 0; 
            display: flex;
            gap: 8px;
            align-items: center;
        }
        .progress-bar { 
            flex: 1;
            height: 4px; 
            background: #222; 
            border: 1px solid #fff;
        }
        .progress-fill { 
            height: 100%; 
            background: #00ff00;
        }
        .progress-label {
            font-size: 11px;
            min-width: 35px;
            text-align: right;
        }
        .empty-state { 
            grid-column: 1 / -1;
            text-align: center; 
            padding: 40px 20px; 
            color: #888; 
            font-size: 12px;
        }
        .footer { 
            border-top: 2px solid #fff;
            padding: 8px 24px; 
            text-align: right; 
            color: #888; 
            font-size: 10px; 
            background: #000;
        }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="header">
            <h1>NUCLEI MASTER</h1>
            <p>distributed scanner control</p>
        </div>
        
        <div class="container" id="children-grid">
            <div class="empty-state">LOADING NODES...</div>
        </div>
        
        <div class="footer">
            <span id="status-text">refreshing...</span>
        </div>
    </div>

    <script>
        async function fetchStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                updateDashboard(data);
                updateFooter(data);
            } catch (error) {
                console.error('Failed to fetch status:', error);
            }
        }

        function updateFooter(data) {
            const online = data.online_count || 0;
            const total = data.total_children || 0;
            const now = new Date().toLocaleTimeString();
            document.getElementById('status-text').textContent = 
                `${online}/${total} online • ${now}`;
        }

        function updateDashboard(data) {
            const grid = document.getElementById('children-grid');
            
            if (!data.children || data.children.length === 0) {
                grid.innerHTML = '<div class="empty-state">NO CHILD NODES CONNECTED</div>';
                return;
            }

            grid.innerHTML = data.children.map(child => {
                const isOnline = child.status === 'online';
                const cpuPercent = Math.min(child.cpu || 0, 100);
                const memPercent = Math.min(child.memory || 0, 100);
                
                return `
                    <div class="card">
                        <div class="card-title">
                            <span class="status-badge ${isOnline ? 'online' : 'offline'}"></span>
                            ${child.node_id}
                        </div>
                        <div class="stat">
                            <span class="stat-label">STATUS</span>
                            <span class="stat-value status-${isOnline ? 'online' : 'offline'}">
                                ${isOnline ? 'ONLINE' : 'OFFLINE'}
                            </span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">IP</span>
                            <span class="stat-value">${child.ip_address || 'N/A'}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">CPU</span>
                        </div>
                        <div class="progress-container">
                            <div class="progress-bar" style="flex: 1">
                                <div class="progress-fill" style="width: ${cpuPercent}%; background: ${cpuPercent > 80 ? '#ff0000' : '#00ff00'}"></div>
                            </div>
                            <div class="progress-label">${cpuPercent.toFixed(0)}%</div>
                        </div>
                        <div class="stat">
                            <span class="stat-label">MEM</span>
                        </div>
                        <div class="progress-container">
                            <div class="progress-bar" style="flex: 1">
                                <div class="progress-fill" style="width: ${memPercent}%; background: ${memPercent > 80 ? '#ff0000' : '#00ff00'}"></div>
                            </div>
                            <div class="progress-label">${memPercent.toFixed(0)}%</div>
                        </div>
                        <div class="stat">
                            <span class="stat-label">UPTIME</span>
                            <span class="stat-value">${child.uptime || 'N/A'}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">HEARTBEAT</span>
                            <span class="stat-value">${new Date(child.last_heartbeat).toLocaleTimeString()}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">CONN</span>
                            <span class="stat-value">${child.connections || 0}</span>
                        </div>
                    </div>
                `;
            }).join('');
        }

        fetchStatus();
        setInterval(fetchStatus, 3000);
    </script>
</body>
</html>
        """

    @app.route("/api/status")
    @login_required
    def api_status():
        """API endpoint for child status"""
        children_data = []
        
        with app.master_node.lock:
            for node_id, child in app.master_node.children.items():
                children_data.append({
                    "node_id": node_id,
                    "status": "online" if child.is_healthy() else "offline",
                    "ip_address": child.ip_address,
                    "cpu": child.cpu_usage,
                    "memory": child.memory_usage,
                    "uptime": child.uptime,
                    "connections": child.connections,
                    "last_heartbeat": child.last_heartbeat.isoformat() if child.last_heartbeat else None,
                })
        
        return jsonify({
            "timestamp": datetime.now().isoformat(),
            "children": children_data,
            "total_children": len(children_data),
            "online_count": sum(1 for c in children_data if c["status"] == "online")
        })

    return app


def run_web_server(master_node, port=5000):
    """Run Flask web server in a background thread"""
    app = create_web_app(master_node)
    
    def run_app():
        app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
    
    thread = threading.Thread(target=run_app, daemon=True)
    thread.start()
    return app
