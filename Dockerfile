# Python Base Image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy project files into the container
COPY . .

# 4. Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose the default port used by FastAPI (Uvicorn)
EXPOSE 8000

# 6. Run the FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
