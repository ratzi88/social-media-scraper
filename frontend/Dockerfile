# Step 1: Build the React app
FROM node:16 AS build
WORKDIR /app
COPY package.json package-lock.json ./  
RUN npm install                
COPY . .                        
RUN npm run build

# Step 2: Serve the app with NGINX
FROM nginx:alpine
WORKDIR /usr/share/nginx/html
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
