from __future__ import annotations
import socket
import time
import asyncio
from fastapi import FastAPI, WebSocket, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

HOST = "127.0.0.1"
PORT = 5050

def receive_text(conn:socket.socket):
    if not conn:
        return
    buffer = ""
    while "\n" not in buffer:
        data = conn.recv(1024).decode("utf-8")
        if not data:
            return buffer
        buffer += data
    return buffer.strip("\n")

html_content = """<!-- static/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>RPi Log Stream</title>
    <style>
        body { font-family: monospace; margin: 20px; }
        #log { background: black; color: lime; padding: 10px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>Raspberry Pi Log Stream</h1>
    <div id="log">Connecting to WebSocket...</div>

    <script>
        const logDiv = document.getElementById("log");
        const maxLines = 40; // Keep only the latest 20 lines
        let logLines = [];   // Store lines in an array
        const ws = new WebSocket(`ws://${window.location.hostname}:8000/ws`);
        
        function updateLog() {
            logDiv.innerHTML = logLines.join("\\n");
            logDiv.scrollTop = logDiv.scrollHeight; // Auto-scroll
        }

        ws.onopen = () => {
            logLines.push("Connected!");
            updateLog();
        };

        ws.onmessage = (event) => {
            logLines.push(event.data); // Add new line
            if (logLines.length > maxLines) {
                logLines.shift(); // Remove oldest line if exceeding limit
            }
            updateLog();
        };

        ws.onerror = (error) => {
            logLines.push(`Error: ${error}`);
            updateLog();
        };

        ws.onclose = () => {
            logLines.push("Disconnected.");
            updateLog();
        };
    </script>
</body>
</html>
"""

def listenSocket(address: tuple):
    _, port = address
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(address)
            s.listen()
            print(f"Listening on port {port}...")

            while True:
                time.sleep(0.5)
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        result = receive_text(conn=conn)
                        if result is None:
                            conn.close()
                            break
                        print(result)
        except KeyboardInterrupt as ke:
            print(f"{repr(ke)}")
            return


app = FastAPI()
# serve templates from package directory
# templates = Jinja2Templates(directory="templates")
ADDRESS = (HOST,PORT)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,address=ADDRESS):
    await websocket.accept()
    _, port = address
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(address)
        s.listen()
        print(f"Listening on port {port}...")
        while True:
            await asyncio.sleep(1.0)
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    result = receive_text(conn=conn) 
                    if result is None:
                        conn.close()
                        break
                    await websocket.send_text(result)


@app.get("/")
async def get_homepage(request: Request):
    return HTMLResponse(content=html_content, status_code=200)
    # return templates.TemplateResponse(request=request,context={},name="index.html")
