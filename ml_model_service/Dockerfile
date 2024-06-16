FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y gcc python3-dev \
    && apt-get install -y git-lfs  && git lfs install && pip install -r requirements.txt

RUN python3 -c 'from huggingface_hub import snapshot_download; snapshot_download(repo_id="RunDiffusion/Juggernaut-X-Hyper")'

CMD ["python", "-m", "src.main"]
