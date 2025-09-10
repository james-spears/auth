# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.13

# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip
RUN pip install --upgrade pip 

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . /opt/app

WORKDIR /opt/app

EXPOSE 8000

# runs the production server
ENTRYPOINT ["/opt/app/start.sh"]
# options are app|worker|flower 
CMD ["app"]
