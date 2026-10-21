#!/bin/sh
set -eu

Xvfb :0 -screen 0 "${SCREEN_WIDTH}x${SCREEN_HEIGHT}x${SCREEN_DEPTH}" -ac &
XVFB_PID=$!
sleep 2

# Serve noVNC on port 6080; websockify bridges browser WebSocket to VNC.
x11vnc -display :0 -forever -shared -nopw -rfbport 5900 -listen 127.0.0.1 &
VNC_PID=$!
websockify --web=/usr/share/novnc/ 0.0.0.0:6080 127.0.0.1:5900 &
NOVNC_PID=$!

# Start the existing CustomTkinter app. main.py imports app.py and starts mainloop.
python main.py &
APP_PID=$!

cleanup() {
  kill "$APP_PID" "$NOVNC_PID" "$VNC_PID" "$XVFB_PID" 2>/dev/null || true
}
trap cleanup INT TERM EXIT

# Keep container alive while the GUI process is running.
wait "$APP_PID"
