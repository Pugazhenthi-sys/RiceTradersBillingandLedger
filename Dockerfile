FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:0 \
    SCREEN_WIDTH=1280 \
    SCREEN_HEIGHT=800 \
    SCREEN_DEPTH=24

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
      python3-tk tk libgl1 libglib2.0-0 xvfb x11vnc novnc websockify \
      ca-certificates procps \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY docker/start-gui.sh /usr/local/bin/start-gui.sh
RUN chmod +x /usr/local/bin/start-gui.sh

EXPOSE 6080
CMD ["/usr/local/bin/start-gui.sh"]
