# Nuclei gRPC Server

A Python-based gRPC server that allows remote execution of Nuclei commands with:
- **Authentication** - Token-based authentication with login/logout
- **Command Execution** - Real-time streaming of command output
- **File Transfer** - Upload/download files with progress streaming
- **Containerized** - Docker image with Nuclei pre-installed

## Features

### Authentication Service
- Login with username/password
- Token validation
- 24-hour token expiry

### Command Executor Service
- Execute arbitrary shell commands remotely
- Stream output line-by-line in real-time
- Environment variable support
- Exit code tracking

### File Transfer Service
- Upload files from client to server
- Download files from server to client
- List files in directories
- Directory traversal protection
- 64KB chunked streaming

## Quick Start

### Prerequisites
- Python 3.11+
- Docker (for containerized deployment)

### Installation

1. **Clone/download the project**
```bash
cd recon_tasks
```

2. **Install dependencies**
```bash
pip3 install -r requirements.txt
```

3. **Generate gRPC code (if not already done)**
```bash
python3 -m grpc_tools.protoc \
    -I./proto \
    --python_out=./nuclei_server \
    --grpc_python_out=./nuclei_server \
    ./proto/nuclei.proto
```

### Running the Server

**Direct execution:**
```bash
python3 -m nuclei_server.server
```

**Docker:**
```bash
docker build -t nuclei-grpc .
docker run -p 50051:50051 nuclei-grpc
```

The server will start on `localhost:50051` with default credentials:
- Username: `admin` | Password: `admin123`
- Username: `user` | Password: `user123`

## Using the Client

### Login
```bash
python3 client.py login admin admin123
```

### Execute Nuclei Command
```bash
python3 client.py exec "nuclei -u https://target.com -t cves/"
python3 client.py exec "nuclei -l targets.txt -t tech-detect" --env TARGET_ENV production
```

### File Operations

**Upload file:**
```bash
python3 client.py upload /path/to/templates.json --as custom-templates.json
```

**Download file:**
```bash
python3 client.py download results.json --to ./local-results.json
```

**List files:**
```bash
python3 client.py list
python3 client.py list --dir /some/subdir
```

### Validate Token
```bash
python3 client.py validate
```

## Project Structure

```
recon_tasks/
├── Dockerfile                 # Multi-stage Docker build
├── requirements.txt           # Python dependencies
├── proto/
│   └── nuclei.proto          # gRPC service definitions
├── nuclei_server/
│   ├── __init__.py
│   ├── auth.py               # Authentication manager
│   ├── executor.py           # Command executor with streaming
│   ├── server.py             # gRPC server implementation
│   ├── nuclei_pb2.py         # Auto-generated (proto messages)
│   └── nuclei_pb2_grpc.py    # Auto-generated (gRPC services)
├── client.py                 # gRPC client CLI
├── generate_proto.sh         # Proto generation script
└── README.md
```

## API Reference

### Auth Service

#### Login
```python
request = LoginRequest(username="admin", password="admin123")
response = stub.Login(request)
# response.token - Use this for subsequent requests
```

#### Validate
```python
request = ValidateRequest(token="<token>")
response = stub.Validate(request)
# response.valid - Token validity
# response.username - Associated username
```

### NucleiExecutor Service

#### ExecuteCommand (Streaming)
```python
request = ExecuteRequest(
    command="nuclei -u https://target.com",
    token="<token>",
    env_vars={"PROXY": "http://proxy:8080"}
)
for response in stub.ExecuteCommand(request):
    print(response.output)  # Streamed output
    print(response.error)   # Streamed errors
    if response.completed:
        print(f"Exit code: {response.exit_code}")
```

### FileTransfer Service

#### UploadFile (Streaming)
```python
def file_generator(filepath, token):
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(64*1024)
            if not chunk:
                break
            yield UploadRequest(
                filename=os.path.basename(filepath),
                data=chunk,
                token=token
            )

response = stub.UploadFile(file_generator("file.txt", token))
```

#### DownloadFile (Streaming)
```python
request = DownloadRequest(filename="results.json", token=token)
with open("results.json", 'wb') as f:
    for response in stub.DownloadFile(request):
        f.write(response.data)
```

#### ListFiles
```python
request = ListFilesRequest(token=token, directory="")
response = stub.ListFiles(request)
for file_info in response.files:
    print(f"{file_info.name}: {file_info.size} bytes")
```

## Security Notes

⚠️ **Development Only**: This implementation uses:
- Insecure gRPC channel (no TLS)
- Simple SHA256 password hashing (use bcrypt in production)
- In-memory token storage (use Redis in production)

For production:
1. Enable TLS/SSL certificates
2. Use bcrypt for password hashing
3. Move to distributed token store
4. Add rate limiting
5. Add audit logging
6. Implement RBAC (Role-Based Access Control)

## Example Workflow

```bash
# Start server
python3 -m nuclei_server.server &

# In another terminal, login
python3 client.py login admin admin123

# Execute nuclei scan
python3 client.py exec "nuclei -u https://example.com -silent"

# Upload templates
python3 client.py upload ./templates/custom.json --as templates.json

# Download results
python3 client.py download results.json --to ./scan-results.json

# List uploaded files
python3 client.py list
```

## Troubleshooting

**Proto files not generated:**
```bash
python3 -m grpc_tools.protoc \
    -I./proto \
    --python_out=./nuclei_server \
    --grpc_python_out=./nuclei_server \
    ./proto/nuclei.proto
```

**Module import errors:**
Ensure you're running from the project root directory and the virtual environment is activated.

**Connection refused:**
- Check server is running: `python3 -m nuclei_server.server`
- Verify port 50051 is open
- Check firewall settings

## License

MIT
