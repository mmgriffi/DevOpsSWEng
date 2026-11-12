FROM python:3.12-slim
# Set working directory
WORKDIR /app
# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    nano \
    && rm -rf /var/lib/apt/lists/*
# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
RUN ls -lart
RUN SECRET_KEY="django-insecure-bhr)ic%a6xvd#m#kjik6%1@o(_-asrt2g-u^bceumz0is!6j3m"
RUN pwd
# Copy the Django project
COPY . .
# Collect static files
#RUN python manage.py collectstatic --noinput
# Expose port for Django/Gunicorn
EXPOSE 8000
# Run Gunicorn as the app server. The config is the folder that contains wsgi.py and settings.py
CMD ["gunicorn", "--chdir", "my_tennis_club", "my_tennis_club.wsgi:application", "--bind", "0.0.0.0:8000"]

#CMD ["/bin/sh", "-c", "bash"]