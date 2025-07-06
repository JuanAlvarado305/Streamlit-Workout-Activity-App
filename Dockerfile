# Use a stable and lightweight Python 3.11 image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies first for better caching
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your application files into the container
COPY . .

# Expose the port that Cloud Run will use (defaults to 8080)
EXPOSE 8080

# This command now uses the $PORT environment variable provided by Cloud Run,
# ensuring your app listens on the correct port.
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
