# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Add the required library for LightGBM
RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the app
CMD ["python", "application.py"]



