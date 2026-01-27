FROM node:20-alpine

WORKDIR /app
COPY package.json package-lock.json ck.yaml /app/
RUN npm ci || npm install

COPY . /app
EXPOSE 5173
CMD ["npm", "run", "dev"]
