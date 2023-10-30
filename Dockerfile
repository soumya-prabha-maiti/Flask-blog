# Base image
FROM python:3.11

# Set the working directory 
WORKDIR /app

# Install dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the current directory contents into the container at .
COPY . .

# Create a instance folder for db and set permissions
RUN mkdir -p /app/instance && chmod 777 /app/instance

# Expose port 7680
EXPOSE 7680

# Start the gunicorn server to serve the app
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:7680","run:app"]