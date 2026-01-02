# Dockerfile for n8n with Python video production support
FROM n8nio/n8n:latest

# Install Python and dependencies
USER root

RUN apk add --no-cache --update \
    python3 \
    py3-pip \
    ffmpeg \
    imagemagick \
    && pip3 install --upgrade pip

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

# Switch back to node user
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
