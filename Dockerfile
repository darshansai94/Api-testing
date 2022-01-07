FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY start.sh /usr/src/app/start.sh
RUN ["chmod", "+x", "/usr/src/app/start.sh"]
ENTRYPOINT ["/usr/src/app/start.sh"]
EXPOSE 7000