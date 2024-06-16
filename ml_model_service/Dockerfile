FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime

WORKDIR /app

# Copy the requirements file and install Python packages
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    curl \
    git-lfs \
    && pip install -r requirements.txt 

# Install Git LFS
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
    && apt-get install -y git-lfs

# Set environment variables
ENV HF_HOME=/app/data/cache

# Create cache directory
RUN mkdir -p $HF_HOME

# Download model and tokenizer
RUN python3 -c 'from huggingface_hub import snapshot_download; snapshot_download(repo_id="lykon/dreamshaper-xl-v2-turbo", token="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", cache_dir="/app/data/cache", local_dir="/app/data/cache")'

# Copy the rest of the application files
COPY . .

# Run the application
CMD ["python", "-m", "src.main"]