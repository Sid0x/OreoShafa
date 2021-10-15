FROM python:3.9
WORKDIR /usr/src/app/
COPY constants.py main.py secretConstants.py oreoUtils.py /usr/src/app/

RUN pip install bs4
RUN pip install python_telegram_bot
RUN pip install requests
RUN pip install simplejson
RUN pip install lxml

CMD ["python", "main.py"]