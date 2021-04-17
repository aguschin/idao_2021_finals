FROM ubuntu:focal

RUN apt-get update -qq && \
    apt-get install -y unzip locales && \
    apt-get clean && \ 
    rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8 && update-locale

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    libx11-6 \
    gdebi-core \
    libapparmor1  \
    libcurl4-openssl-dev \
    build-essential \
    gnupg2 \
    cmake \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV CONDA_AUTO_UPDATE_CONDA=false
RUN curl -sLo ~/miniconda.sh -O  https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
     chmod +x ~/miniconda.sh && \
     ~/miniconda.sh -b -p /usr/conda && \
     rm ~/miniconda.sh

ENV PATH=/usr/conda/bin:$PATH

RUN conda install -y -c pytorch \
    torchvision \
    numpy scipy pandas scikit-learn joblib tqdm ipython pip cython numba && \
    pip install statsmodels pqdict xlearn ml_metrics tsfresh mlxtend h5py tempita && \
    pip install xgboost lightgbm catboost && \
    pip install tensorflow && \
    pip install keras \
    && conda clean -ya

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt \
    && rm -rf /root/.cache
