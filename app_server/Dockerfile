FROM python:3.5
ADD . /code
WORKDIR /code
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade -r requirements.txt
EXPOSE 5000
CMD ["python", "-u", "application.py"]