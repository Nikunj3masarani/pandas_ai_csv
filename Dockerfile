FROM python:3.11-slim-bookworm

# Set the Current Working Directory inside the container.
WORKDIR /app


# Upgrading pip.
RUN pip install --upgrade pip

# Download all dependencies.
COPY requirements.txt /app/

# Install all dependencies.
RUN pip install -r /app/requirements.txt --no-cache-dir

# Copy current directory into working directory.
COPY . /app

EXPOSE 8051

CMD ["streamlit", "run", "--server.address", "0.0.0.0","--server.port", "8051", "app.py"]



