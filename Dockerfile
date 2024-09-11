FROM arashpy79iran/opengram:latest

# انتقال فایل pygram.py به یک دایرکتوری موقت

COPY requirements.txt /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt --break-system-packages

CMD ["bash", "-c", "if [ ! -f /opengram/pygram.py ]; then cp /app/pygram.py /opengram/; fi && python3 /opengram/pygram.py"]
