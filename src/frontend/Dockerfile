FROM node:20-slim

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY . .

# Expose Vite port
EXPOSE 5173

# Run development server
# We use --host to ensure it listens on all interfaces (0.0.0.0) inside the container
CMD ["npm", "run", "dev", "--", "--host"]
