FROM python:3-alpine
ADD server.py /
RUN pip install requests
CMD [ "python", "./server.py" ]
