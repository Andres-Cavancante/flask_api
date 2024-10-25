FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# wait for the mysql database
# CMD ["sh", "-c", "sleep 20 && python src/db_populator/populate.py && tail -f /dev/null"]

# RUN echo "Dependencies installed and tables populated."
# CMD ["python", "main.py"]
