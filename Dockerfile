# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first
COPY script/requirements.txt .

# Install the necessary packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY script/test_suite.py .

# Set the default command to run the Python script
CMD ["python", "test_suite.py"]
