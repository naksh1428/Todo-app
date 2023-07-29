FROM python:3.10

WORKDIR /app

COPY requirement.txt .

# Install dependencies
RUN pip install -r requirement.txt

# Copy the rest of the project files to the container
COPY . .

# Expose the port
#EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]