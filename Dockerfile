FROM python:3.9-slim
WORKDIR /app/barn-owl-bagels
COPY . /app/barn-owl-bagels
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
ENV FLASK_APP=bagels.py
CMD ["python", "./bagels.py"]