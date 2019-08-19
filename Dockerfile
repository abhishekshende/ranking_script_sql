FROM python:3.6

RUN mkdir -p  /home/python_code/app

WORKDIR /home/python_code/app

COPY requirements.txt /home/python_code/app
RUN pip install --no-cache-dir -r requirements.txt



COPY . /home/python_code/app

EXPOSE 5000

CMD ['python', 'rank_serv.py']