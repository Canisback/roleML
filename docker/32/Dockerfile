FROM clinstid/i386-python
RUN apt-get update && \
    apt-get -y install python python-dev
RUN apt-get -y install curl && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py
RUN pip install --no-cache-dir -U scikit-learn
RUN pip install pandas
WORKDIR /app
ADD ./dataset/ dataset/
ADD ./train.py .
RUN mkdir model
ENTRYPOINT ["python3","-u","./train.py"]
