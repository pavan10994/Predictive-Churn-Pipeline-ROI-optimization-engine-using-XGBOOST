# 1. Start with a lightweight version of Python
FROM python:3.9-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy ONLY the requirements file first (this makes Docker build much faster)
COPY requirements.txt .

# 4. Install the exact tools needed
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your project into the container
COPY . /app

# 6. Tell the container which port the API will use
EXPOSE 8000

# 7. Start the server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]