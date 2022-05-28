FROM continuumio/miniconda3

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
RUN echo "conda activate qgel" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]
