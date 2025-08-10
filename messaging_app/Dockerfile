# Use Python 3.10 as base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy dependencies first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose Django default port
EXPOSE 8000

# Run Django with port explicitly specified
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000", "-p", "8000"]
