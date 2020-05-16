FROM python:3.7
RUN pip3 install pandas
RUN pip3 install --no-cache-dir -U scikit-learn
WORKDIR /app
ADD ./dataset/ dataset/
ADD ./train.py .
RUN mkdir model
ENTRYPOINT ["python3","-u","./train.py"]
