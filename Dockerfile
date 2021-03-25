# set base image (host OS)
FROM python:3.7

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY main.py .
COPY predictor.py .

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN git clone https://github.com/facebookresearch/detectron2.git
RUN pip install -e detectron2

# command to run on container start
CMD [ "python", "main.py" ]