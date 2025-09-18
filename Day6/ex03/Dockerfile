# Use continuumio/miniconda3 as a base image 
FROM continuumio/miniconda3

# Set /Day6 as a working directory
WORKDIR /ex03

# Copy environment.yml
COPY * .

# create an environment using environment.yml
RUN conda env create -f environment.yml -n ex03

# expose port 8501
EXPOSE 8501

CMD ["conda", "run", "--no-capture-output", "-n", "ex03", "streamlit", "run", "main.py", "--server.address", "0.0.0.0"]