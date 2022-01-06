FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./


RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./run.py", "--keyword", "test", "--pytest-args", "-–html=report.html"]
