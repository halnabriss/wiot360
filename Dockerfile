FROM python:3.9-slim

# Install dependencies
RUN pip install flask mysql-connector-python

# Copy the app code
COPY app.py /app/app.py

# Expose the app port
EXPOSE 3000

# Run the app
CMD ["python", "/app/app.py"]
