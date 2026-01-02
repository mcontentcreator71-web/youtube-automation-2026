# Dockerfile for n8n with Python video production support
# Use Node.js Debian-based image for better Python package compatibility
FROM node:20-slim

# Install Python, FFmpeg, ImageMagick, and build dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    ffmpeg \
    imagemagick \
    build-essential \
    python3-dev \
    && pip3 install --upgrade pip --break-system-packages \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install n8n globally
RUN npm install -g n8n

# Copy Python scripts
WORKDIR /home/node
COPY requirements.txt .
COPY video_production.py .
COPY run_video_production.py .
COPY youtube_upload.py .

# Install Python dependencies and clean up in one layer to reduce image size
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages \
    && apt-get remove -y build-essential python3-dev \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /root/.cache/pip \
    && find /usr/local/lib/python3.*/dist-packages -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true \
    && find /usr/local/lib/python3.*/dist-packages -name "*.pyc" -delete

# Create videos directory
RUN mkdir -p /home/node/videos && chown -R node:node /home/node

# Switch to node user
USER node

# Set environment variables
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV NODE_ENV=production
ENV N8N_USER_FOLDER=/home/node/.n8n

# Expose n8n port
EXPOSE 5678

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:5678/healthz', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start n8n
CMD ["n8n", "start"]
