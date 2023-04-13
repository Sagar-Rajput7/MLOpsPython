# Base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .
# Install the required packages
RUN pip install -v -r requirements.txt

# Copy the application code to the container
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV LISTEN_PORT=5000


# Expose port 6002 for the Flask app
EXPOSE 5000

# Start the Flask app when the container starts
CMD ["python3", "app.py"]
