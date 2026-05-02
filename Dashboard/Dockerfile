FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Build application
RUN npm run build

# Expose default Nitro port. Render will provide PORT at runtime.
EXPOSE 3000

# Start production server
CMD ["npm", "run", "start"]
