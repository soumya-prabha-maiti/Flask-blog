# Base image
FROM python:3.11

# Set the working directory 
WORKDIR /app

# Install dependencies
COPY requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the current directory contents into the container at .
COPY . .

# Expose port 7680
EXPOSE 7680

# Start the gunicorn server to serve the app
CMD ["gunicorn", "-b", "0.0.0.0:7680","run:app"]