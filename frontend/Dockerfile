# Production Dockerfile for Frontend Runtime Environment
FROM node:18-alpine

WORKDIR /app

# Copy package descriptors first for layer caching
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application files
COPY . .

# Expose server port
EXPOSE 3000

# Default environment variables
ENV PORT=3000
ENV API_URL=http://localhost:8000

# Start server runtime
CMD ["node", "server.js"]
