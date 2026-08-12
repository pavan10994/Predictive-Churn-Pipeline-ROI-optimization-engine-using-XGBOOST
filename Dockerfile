# 1. Start with a lightweight version of Python
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your project files into the container
COPY . /app

# 4. Install your project dependencies
RUN pip install --no-cache-dir -e .

# 5. Tell the container which port the API will use
EXPOSE 8000

# 6. The command to start the FastAPI server when the container turns on
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]