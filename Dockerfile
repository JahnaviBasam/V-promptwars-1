# Use a lightweight python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the static HTML file into a static directory for Flask
RUN mkdir -p static
COPY index.html static/index.html

# Copy the backend server
COPY server.py .

# Cloud Run defaults to port 8080, expose it
EXPOSE 8080

# Serve the application through Flask
CMD ["python", "server.py"]
