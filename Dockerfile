FROM continuumio/miniconda3

COPY environment.yml .

RUN conda env create -f environment.yml

RUN echo "conda activate qGEL" >> ~/.bashrc

SHELL ["/bin/bash", "--login", "-c"]
