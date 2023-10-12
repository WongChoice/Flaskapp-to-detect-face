# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory to /flaskapp
WORKDIR /flaskapp

# Copy the current directory contents into the container at /flaskapp
COPY . /flaskapp

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5969 available to the world outside this container
EXPOSE 5969

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
