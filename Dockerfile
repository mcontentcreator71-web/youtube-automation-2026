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
    && pip3 install --upgrade pip \
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

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Create videos directory
RUN mkdir -p /home/node/videos && chown -R node:node /home/node

# Switch to node user
USER node

# Set environment variables
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV NODE_ENV=production

# Expose n8n port
EXPOSE 5678

# Start n8n
CMD ["n8n", "start"]
