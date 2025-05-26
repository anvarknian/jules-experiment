# Stage 1: Build the Flutter web application
FROM cirrusci/flutter:stable AS build

# Set the working directory
WORKDIR /app

# Copy the Flutter application source code
COPY . .

# Install dependencies
RUN flutter pub get

# Build the web application
RUN flutter build web --release --dart-define=BACKEND_URL=http://backend:8000

# Stage 2: Serve the Flutter web application with Nginx
FROM nginx:alpine

# Copy the built web files from the build stage
COPY --from=build /app/build/web /usr/share/nginx/html

# Custom Nginx configuration to handle SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
