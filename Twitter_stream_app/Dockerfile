FROM continuumio/miniconda3
LABEL maintainer = "karthikkm028@gmail.com"
COPY requirements.txt /tmp/
COPY ./app /app
COPY start.sh /app
COPY two.sh /app
WORKDIR "/app"
RUN conda install -c conda-forge/label/gcc7 dash-html-components 
RUN conda install -c conda-forge/label/gcc7 dash-core-components
RUN conda install -c conda-forge/label/gcc7 sqlalchemy-utils
RUN conda install -c conda-forge dash
RUN conda install -c conda-forge tweepy
RUN conda install --file /tmp/requirements.txt
RUN conda clean -afy
ENV CONSUMER_KEY hello
ENV CONSUMER_SECRET hello
ENV ACCESS_TOKEN hello
ENV ACCESS_TOKEN_SECRET hello
EXPOSE 80
RUN ls -al
ENTRYPOINT ["/app/two.sh"]