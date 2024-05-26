FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 5000

# CMD ["python", "populate.py"]
# CMD ["python", "main.py"]
CMD ["bash", "-c", "sleep 15 && python src/populate.py && python main.py"]
# CMD ["bash", "-c", "sleep 15 && python src/populate.py"]

# -rmv marketing.csv

# docker build -t test .
# docker run -p 5000:5000  test