FROM node:22-alpine AS builder

# Create app directory
WORKDIR /opt/app

# Install app dependencies
COPY package*.json ./
COPY ./.env ./.env
COPY ./dist ./dist

RUN npm ci --omit=dev

FROM node:22-alpine

# Create app directory
WORKDIR /opt/app

COPY --from=builder /opt/app ./

CMD [ "NODE_ENV=production", "node", "./dist/main.js" ]