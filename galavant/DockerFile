# Use an official Python image as a base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port 8000 for the app
EXPOSE 8000

# Run the command to start the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]