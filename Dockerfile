# Minimal Dockerfile for n8n - No GitHub cloning, just workflow JSON
# Uses official n8n approach but copies workflow directly
FROM node:20-alpine

# Install n8n globally (official n8n image is distroless, so we build our own minimal version)
RUN npm install -g n8n

# Create n8n directories
WORKDIR /home/node
RUN mkdir -p /home/node/.n8n/workflows && chown -R node:node /home/node

# Copy ONLY the workflow JSON file (no Python scripts, no requirements.txt)
COPY workflow.json /home/node/.n8n/workflows/

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

# Start n8n (workflow will be available in UI to import manually)
CMD ["n8n", "start"]
