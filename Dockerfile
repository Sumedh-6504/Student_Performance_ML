# Use a lightweight Python base image
FROM python:3.14-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Command to run the application
CMD["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]