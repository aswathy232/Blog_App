# Use the official Python image
FROM python:3.9-buster
ENV PYTHONBUFFERED=1
# Set the working directory
WORKDIR /django

# Copy the requirements file
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .



# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
