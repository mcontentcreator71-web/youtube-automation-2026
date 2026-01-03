# Dockerfile for n8n with Python video production support
# Use Node.js Alpine base and install n8n (smaller than Debian)
FROM node:20-alpine

# Switch to root user to install system packages
USER root

# Install Python, FFmpeg, ImageMagick, and build dependencies
RUN apk add --update --no-cache \
    python3 \
    py3-pip \
    ffmpeg \
    imagemagick \
    build-base \
    python3-dev \
    && pip3 install --upgrade pip --break-system-packages

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
    && apk del build-base python3-dev \
    && rm -rf /tmp/* \
    && rm -rf /root/.cache/pip \
    && find /usr/lib/python3.*/site-packages -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true \
    && find /usr/lib/python3.*/site-packages -name "*.pyc" -delete

# Create videos directory
RUN mkdir -p /home/node/videos && chown -R node:node /home/node

# Switch back to node user (n8n image uses node user)
USER node

# Set environment variables
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV NODE_ENV=production
ENV N8N_USER_FOLDER=/home/node/.n8n
ENV DB_SQLITE_BUSY_TIMEOUT=30000

# Expose n8n port
EXPOSE 5678

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:5678/healthz', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Start n8n
CMD ["n8n", "start"]
