FROM numenta/nupic:latest

WORKDIR /home/docker
RUN git clone https://github.com/antsago/3rdYearProject.git

WORKDIR /home/docker/3rdYearProject
