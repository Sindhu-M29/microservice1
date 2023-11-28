# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5003 for the Flask application
EXPOSE 5003

# Define environment variable for Flask to run in production mode
ENV FLASK_ENV=production

# Command to run your application
CMD ["python", "flightbooking.py"]
