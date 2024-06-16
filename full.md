
Creating a decision-making process for such a complex project requires a detailed breakdown of requirements, components, and constraints. Here's how we can approach this task step-by-step:

1. **Understanding Requirements**: The core requirements include generating images in various formats and aspect ratios, adhering to Gazprombank's corporate standards, using open-source models for image generation, and ensuring intellectual property rights. The system must also accommodate multiple user inputs, including user IDs, user data, product data, channel data, and desired image size.

2. **Designing Components**: We need to design four main components:
   - An ML model component that handles image generation based on input parameters.
   - A REST API component for handling requests and responses.
   - A storage component for keeping track of dialogues and responses.
   - A web interface component for user interaction.

3. **API Design**: The API should accept headers with base authentication and handle arrays of client data. It should return user IDs, generated images, and offer clustering capabilities.

4. **Docker Implementation**: The entire system should be containerized using Docker to facilitate deployment and scalability.

5. **Testing**: Unit tests and contract tests should be implemented to ensure the reliability and correctness of the system.

6. **Web Interface**: This includes both frontend and backend components, providing users with a visual interface for interacting with the system, viewing history, and marking successful or unsuccessful results.

7. **User Experience**: An intuitive interface for monitoring requests, results, and feedback is essential. Administrative functionalities should also be included for managing users.

Given these guidelines, we can start by outlining the architecture using Python as the primary programming language and PostgreSQL as the database management system. Here's a high-level view of how the components might interact:

- **ML Model Component**: This will be responsible for generating images based on input parameters. It could use libraries like TensorFlow or PyTorch for implementing the image generation model. The model should be open-source and capable of being retrained based on user feedback.

- **REST API Component**: This will serve as the main entry point for external requests. It should validate incoming requests, pass them to the ML model component, and return the generated images along with metadata. Security measures, such as base authentication, should be implemented here.

- **Storage Component**: This component will store all interactions, including requests and responses. PostgreSQL can be used to maintain a structured record of these interactions, which can later be analyzed for system improvements.

- **Web Interface Component**: This will provide a graphical user interface for users to interact with the system. It should allow users to input parameters, view generated images, and mark results for further analysis or retraining of the model.

By breaking down the project into these components and addressing each requirement individually, we can develop a robust and scalable system that meets the specified criteria. Testing and iterative development will be crucial to ensure that the system performs as expected and can be continuously improved over time.

To create a project structure and generate Docker files for the project described, we will organize the project into distinct components, each serving a specific purpose. Below is the proposed project structure, followed by the Docker file configurations for each component:

### Project Structure
logo-generation/
|   |-- ml_model_service/
|   |   |-- data/
|   |   |-- src/
|   |   |   |-- __init__.py
|   |   |   |-- main.py
|   |   |   |-- model.py
|   |   |   |-- config.py
|   |   |-- Dockerfile
|   |   |-- requirements.txt
|   |-- rest_api_service/
|   |   |-- src/
|   |   |   |-- __init__.py
|   |   |   |-- main.py
|   |   |   |-- api.py
|   |   |   |-- config.py
|   |   |-- Dockerfile
|   |   |-- requirements.txt
|   |-- storage_service/
|   |   |-- data/
|   |   |-- src/
|   |   |   |-- __init__.py
|   |   |   |-- main.py
|   |   |   |-- db.py
|   |   |   |-- config.py
|   |   |-- Dockerfile
|   |   |-- requirements.txt
|   |-- web_interface_service/
|   |   |-- src/
|   |   |   |-- __init__.py
|   |   |   |-- main.py
|   |   |   |-- interface.py
|   |   |   |-- config.py
|   |   |-- Dockerfile
|   |   |-- requirements.txt
|   |-- docker-compose.yml
|   |-- README.md


### Docker Files

#### 1. Dockerfile (logo_generation/ml_model_service/Dockerfile)
```Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . .

ENV "HF_HOME"="/data/.cache"  

RUN apt-get update && apt-get install -y gcc python3-dev \
    && apt-get install -y git-lfs  && git lfs install && pip install -r requirements.txt

CMD ["python", "-m", "src.main"]
```

#### 2. Dockerfile (logo_generation/rest_api_service/Dockerfile)
```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-m", "src.main"]
```

#### 3. Dockerfile (logo_generation/storage_service/Dockerfile)
```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-m", "src.main"]
```

#### 4. Dockerfile (logo_generation/web_interface_service/Dockerfile)
```Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-m", "src.main"]
```

#### 5. docker-compose.yml
```yaml
services:
  ml_model_service:
    build: ./ml_model_service
    networks:
      - logo-network
    ports:
      - "5001:5001"
    expose:
      - "5001"

  rest_api_service:
    build: ./rest_api_service
    networks:
      - logo-network
    ports:
      - "5000:5000"
    expose:
      - "5000"

  storage_db:
    image: postgres:14.7
    networks:
      - logo-network
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: logo_storage
    volumes:
      - ./storage_service/data:/var/lib/postgresql/data

  storage_service:
    build: ./storage_service
    networks:
      - logo-network
    depends_on:
      - storage_db
    ports:
      - "5432:5432"
    expose:
      - "5432"

  web_interface_service:
    build: ./web_interface_service
    networks:
      - logo-network
    ports:
      - "7860:7860"
    expose:
      - "7860"

networks:
  logo-network:
    driver: bridge
```

This project structure and Docker files configuration ensure that each component is developed independently while allowing seamless integration through Docker Compose. Each component is containerized for ease of deployment and scalability, adhering to the microservices architecture principles.

I'll answer as a world-famous software engineer specializing in full-stack web development with expertise in React and Python, recognized for delivering high-quality, user-centric applications.

To address the requirements for the web interface, we'll focus on developing two key features: a history viewer and an administrative interface. The history viewer will display past requests and their outcomes, allowing users to mark results as successful or failed. This feedback will be crucial for improving the model's accuracy over time. The administrative interface will enable managing user accounts and settings.

### logo_generation/ml_model_service/src

`config.py`
```python
SERVICE_PORT = 5001
MODEL_DATA_PATH = './data'
DB_CONFIG = {
    'host': 'storage_db',
    'database': 'logo_storage',
    'user': 'user',
    'password': 'password'
}
NUM_INFERENCE_STEPS: int = 25
STRENGTH_LOW: float = 0.7
STRENGTH_HIGH: float = 0.9
GUIDANCE_SCALE_LOW: int = 10
GUIDANCE_SCALE_HIGH: int = 15
```

`main.py`
```python
from flask import Flask, request, jsonify
from pathlib import Path
import psycopg2
import json
import base64
from datetime import datetime
import random

from .utils import generate_prompt, generate_negative_prompt
from . import config
from .model import txt2img_model


app = Flask(__name__)

IMAGE_DIR = Path(config.MODEL_DATA_PATH) / 'images'
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def image_generator(path_to_image: Path, metadata: dict) -> tuple[bytes, dict]:
    """
    Generate an image using the ML model service.

    Parameters
    ----------
    path_to_image : Path
        Filepath to save the image to (ending in .png).
    metadata : dict
        The metadata for the image generation request.

    Returns
    -------
    tuple[bytes, dict]
        Image bytes and metadata
    """
    sd_llm_prompt = generate_prompt(int(metadata['age']))

    negative_prompt = generate_negative_prompt()
    strength = round(random.uniform(config.STRENGTH_LOW, config.STRENGTH_HIGH), 2) 
    guidance_scale = int(random.uniform(config.GUIDANCE_SCALE_LOW, config.GUIDANCE_SCALE_HIGH))
    
    metadata['prompt'] = sd_llm_prompt
    metadata['negative_prompt'] = negative_prompt
    metadata['strength'] = strength
    metadata['guidance_scale'] = guidance_scale
    
    
    img = txt2img_model(
        prompt=sd_llm_prompt, 
        negative_prompt=negative_prompt,
        strength=strength, 
        guidance_scale=guidance_scale, 
        num_inference_steps=config.NUM_INFERENCE_STEPS,
        height=metadata['height'], width=metadata['width']
    ).images[0]
    img.save(path_to_image)

    with open(path_to_image, 'rb') as f:
        image_bytes = f.read()
    return image_bytes, metadata
    

    
def store_image_path_in_database(user_id: str, image_path: str, metadata: dict):
    """
    Store the image path in the database.

    Parameters
    ----------
    user_id : str
        The user ID associated with the image.
    image_path : str
        The path to the image.
    metadata : dict
        The metadata associated with the image.
    """ 
    conn = psycopg2.connect(**config.DB_CONFIG)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO interactions (user_id, image_url, metadata) VALUES (%s, %s, %s)", (user_id, str(image_path), json.dumps(metadata)))
        conn.commit()
    except Exception as e:
        print(f"Failed to store image path in database: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


@app.route('/generate_image', methods=['POST'])
def generate_image() -> tuple[str, int]:
    """
    Generate an image using the ML model service.

    Parameters
    ----------
    path_to_image : Path
        Filepath to save the image to (ending in .png).
    metadata : dict
        The metadata for the image generation request.

    Returns
    -------
    tuple[str, int]
        Image path and status code (200 if successful, 500 if not).
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        metadata = data.get('metadata')
        unique_id = datetime.now().strftime("%d.%m.%Y_%H:%M:%S")
        image_filename = f'image_{user_id}_{unique_id}.jpg'
        image_path = IMAGE_DIR / image_filename
        img, metadata = image_generator(image_path, metadata)

        image_base64 = base64.b64encode(img).decode('utf-8')
        store_image_path_in_database(user_id, str(image_path), metadata)
        
        return jsonify({'image_path': str(image_path), 'image': image_base64})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.SERVICE_PORT)
```

`model.py`
```python
import torch
from diffusers import StableDiffusionXLPipeline, AutoPipelineForText2Image
from diffusers import DPMSolverMultistepScheduler


def get_model() -> AutoPipelineForText2Image:
    """
    Get the ML model.

    Returns
    -------
    AutoPipelineForText2Image
        The ML model.
    """
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "RunDiffusion/Juggernaut-X-Hyper",
        torch_dtype=torch.float16
    )
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

    pipe.enable_sequential_cpu_offload()

    txt2img = AutoPipelineForText2Image.from_pipe(pipe)
    
    return txt2img


txt2img_model = get_model()
```
`utils.py`
```python
import random


genders = ['well dressed male', 'well dressed female', "image"]
art_styles = ['Photorealism', 'Classicism', 'Land Art', 'Realism', 'modernist']
resolutions = ['unreal engine', 'sharp focus', '8k', 'vray']
lighting = ['cinematic', 'dark', 'sunlight', 'god rays']
required_colors = ['light salmon', 'pale turquoise', 'royal blue']
locations = ['urban', 'countryside', 'beach', 'mountain', 'forest']
landscapes = ['cityscape', 'seascape', 'mountainscape', 'countryscape', 'sunset']
activities = ['sport', 'work', 'relaxation', 'travel', 'entertainment']
attributes = ['mobile phone', 'coffee', 'book',  'car', 'house']


def generate_prompt(age: int = 30) -> str:
    """
    Generate a prompt for the ML model.
    
    Parameters
    ----------
    age : int
        The age of the person.
    
    Returns
    -------
    str
        The generated prompt.
    """
    if age < 11:
        age_group = '0-10'
    elif age < 18:
        age_group = '10-17'
    elif age < 26:
        age_group = '17-25'
    elif age < 51:
        age_group = '25-45'
    else:
        age_group = '45-65'
    
    gender = random.choice(genders)
    art_style = random.choice(art_styles)
    resolution = random.choice(resolutions)
    lighting_style = random.choice(lighting)
    location = random.choice(locations)
    landscape = random.choice(landscapes)
    activity = random.choice(activities)
    attribute = random.choice(attributes)

    prompt = f"""The image must include the colors {', '.join(required_colors)} :Depict a {gender} in their {age_group} engaging in {activity} activities, 
    such as {activity} in a {location} {landscape} with a {attribute}, using a {art_style} visual style. 
    The artwork should be rendered in {resolution} and {lighting_style} lighting. 
    """

    return prompt


def generate_negative_prompt() -> str:
    """
    Generate a negative prompt for the ML model.
    
    Returns
    -------
    str
        The generated negative prompt.
    """
    negative_prompt = """
    The artwork avoids the pitfalls of bad art, such as ugly and deformed eyes and faces, poorly drawn, blurry, and disfigured bodies with extra limbs and close-ups that look weird. 
    It also avoids other common issues such as watermarking, text errors, missing fingers or digits, cropping, poor quality, and JPEG artifacts. 
    The artwork is free of signature or watermark and avoids framing issues. The hands are not deformed, 
    the eyes are not disfigured, and there are no extra bodies or limbs. 
    The artwork is not blurry, out of focus, or poorly drawn, and the proportions are not bad or deformed. 
    There are no mutations, missing limbs, or floating or disconnected limbs. 
    The hands and neck are not malformed, and there are no extra heads or out-of-frame elements. 
    The artwork is not low-res or disgusting and is a well-drawn, highly detailed, and beautiful rendering.
    """
    return negative_prompt

```

### logo_generation/rest_api_service/src

`config.py`
```python
SERVICE_PORT = 5000
ML_MODEL_SERVICE_HOST = 'ml_model_service'
ML_MODEL_SERVICE_PORT = 5001
DB_CONFIG = {
    'host': 'storage_db',
    'database': 'logo_storage',
    'user': 'user',
    'password': 'password'
}
MODEL_DATA_PATH = './data'
```

`main.py`
```python
from flask import Flask, request, jsonify
import psycopg2
import requests
from . import config

app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate() -> jsonify:
    """
    Generate an image using the ML model service and return the image path.

    Returns
    -------
    jsonify
        A JSON response containing the image path and base64-encoded image bytes.
    """
    data = request.get_json()
    response = requests.post(f'http://{config.ML_MODEL_SERVICE_HOST}:{config.ML_MODEL_SERVICE_PORT}/generate_image', json=data).json()
    path = response.get('image_path')
    image = response.get('image')
    return jsonify({'image_path': path, 'image': image})

@app.route('/api/interactions/<user_id>', methods=['GET'])
def get_interactions(user_id: str) -> jsonify:
    """
    Get interactions for a given user ID.

    Parameters
    ----------
    user_id : str
        The ID of the user.

    Returns
    -------
    jsonify
        A JSON response containing the interactions for the user.
    """
    conn = psycopg2.connect(**config.DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT * FROM interactions WHERE user_id = %s", (user_id,))
    interactions = cur.fetchall()
    cur.close()
    conn.close()

    interaction_list = []
    for interaction in interactions:
        interaction_list.append({
            'id': interaction[0],
            'user_id': interaction[1],
            'image_url': interaction[2],
            'metadata': interaction[3]  
        })

    return jsonify(interaction_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.SERVICE_PORT)
    
```


### logo_generation/storage_service/src

`config.py`
```python
DB_CONFIG = {
    'host': 'storage_db',
    'database': 'logo_storage',
    'user': 'user',
    'password': 'password'
}
```

`main.py`
```python
from . import db

if __name__ == '__main__':
    db.create_tables()
```

`db.py`
```python
import psycopg2
import time
from .config import DB_CONFIG


def wait_for_db():
    """
    Wait for the database to be available.
    """
    while True:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("Database is available.")
            break
        except Exception as e:
            print(f"Database not available yet, waiting... Error: {e}")
            time.sleep(5)


def create_tables():
    """
    Create the interactions and marked_images tables if they don't exist.
    """
    wait_for_db()
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255),
            image_url VARCHAR(255),
            metadata JSONB  -- Add metadata column with JSONB type
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS marked_images (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255),
            image_url VARCHAR(255),
            result BOOLEAN
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

    
def get_marked_images() -> list[tuple[str, str, bool]]:
    """
    Fetch all marked images from the database.

    Returns
    -------
    list[tuple[str, str, bool]]
        A list of tuples containing the user ID, image URL, and result.
    """
    wait_for_db() 
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT * FROM marked_images")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def store_interaction(user_id: str, image_url: str, metadata: str):
    """
    Store an interaction in the database.
    """
    wait_for_db()
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("INSERT INTO interactions (user_id, image_url, metadata) VALUES (%s, %s, %s)", (user_id, image_url, metadata))
    conn.commit()
    cur.close()
    conn.close()


def mark_image(user_id: str, image_url: str, result: bool):
    """
    Mark an image as marked in the database.
    """
    wait_for_db()  
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("INSERT INTO marked_images (user_id, image_url, result) VALUES (%s, %s, %s)", (user_id, image_url, result))
    conn.commit()
    cur.close()
    conn.close()


def fetch_marked_images() -> list[tuple[str, str, bool]]:
    """
    Fetches marked images from the database.
    
    Returns
    -------
    list[tuple[str, str, bool]]
        A list of tuples containing the user ID, image URL, and result.
    """
    wait_for_db() 
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT * FROM marked_images")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
```


### logo_generation/web_interface_service/src

`config.py`
```python
SERVICE_PORT=7860
ML_MODEL_SERVICE_HOST = 'ml_model_service'
ML_MODEL_SERVICE_PORT = 5001
API_PORT: int = 5000
API_HOST: str = 'rest_api_service'
DB_CONFIG = {
    'host': 'storage_db',
    'database': 'logo_storage',
    'user': 'user',
    'password': 'password'
}
```

`main.py`
```python
from . import interface, config


if __name__ == '__main__':
    interface.demo.launch(server_name="0.0.0.0", server_port=config.SERVICE_PORT)
```

`interface.py`
```python
import gradio as gr
import requests
from PIL import Image
from io import BytesIO
import base64
import pandas as pd
import psycopg2
import time
from . import config

SESION_TEMPORARY_DICT = {}


def wait_for_db():
    """
    Wait for the database to be available.
    """
    while True:
        try:
            conn = psycopg2.connect(**config.DB_CONFIG)
            conn.close()
            print("Database is available.")
            break
        except Exception as e:
            print(f"Database not available yet, waiting... Error: {e}")
            time.sleep(5)

def generate_image(user_id: str, metadata: dict) -> Image:
    """
    Generate an image using the ML model service.
    
    Parameters
    ----------
    user_id : str
        The user ID.
    metadata : dict
        The metadata.
    
    Returns
    -------
    Image
        The generated image.
    """
    data = {'user_id': user_id, 'metadata': metadata}
    
    response = requests.post(f'http://{config.ML_MODEL_SERVICE_HOST}:{config.ML_MODEL_SERVICE_PORT}/generate_image', json=data).json()
    img = Image.open(BytesIO(base64.b64decode(response['image'])))
    
    SESION_TEMPORARY_DICT[user_id] = response['image_path']
    return img

def mark_image(user_id: str, result: bool):
    """
    Mark an image as marked in the database.
    """
    image_url = SESION_TEMPORARY_DICT[user_id]
    wait_for_db()  
    conn = psycopg2.connect(**config.DB_CONFIG)
    cur = conn.cursor()
    cur.execute("INSERT INTO marked_images (user_id, image_url, result) VALUES (%s, %s, %s)", (user_id, image_url, result))
    conn.commit()
    cur.close()
    conn.close()


def get_history(user_id: str) -> pd.DataFrame:
    """
    Fetch the history of interactions for a given user.

    Parameters
    ----------
    user_id : str
        The user ID.

    Returns
    -------
    pd.DataFrame
        The history of interactions.
    """     
    response = requests.get(f"http://{config.API_HOST}:{config.API_PORT}/api/interactions/{user_id}").json()
    df = pd.DataFrame.from_dict(response)

    return df  


with gr.Blocks() as demo:
    input_data = gr.Textbox(label="User ID")
    metadata_input = gr.Textbox(label="Metadata", value="{'age': 20, 'sex': 'male', 'height': 300, 'width': 300}")
    output_data = gr.Image()
    history_viewer = gr.Dataframe(headers=["id", "image_url", "metadata", "user_id"], datatype=["str", "str", "str", "str"])
    get_history_button = gr.Button("Get History by user ID")
    mark_result_button = gr.Button("Mark As Good Image")

    get_history_button.click(get_history, inputs=input_data, outputs=history_viewer)
    mark_result_button.click(mark_image, inputs=[input_data, gr.Checkbox(label="Send Mark image to database")], outputs=None)

    interface = gr.Interface(
        fn=generate_image,
        inputs=[input_data, metadata_input],
        outputs=[output_data],
        live=False
    )

if __name__ == '__main__':
    demo.launch(server_name="0.0.0.0", server_port=config.SERVICE_PORT)
```

### Exmple generation


To generate an image using the API:

1. Send a POST request to `http://localhost:5000/api/generate` with the user ID in the request body. The API will return the image path and the binary image.
```bash
curl -X POST \
  http://localhost:5000/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"user_id": "123", "metadata": { "age": 20, "sex": "male", "height": 512, "width": 512}}'
```

2. Send a GET request "http://localhost:5000/api/interactions/{user_id}" to get users interactions from database.
```bash
curl -X GET "http://localhost:5000/api/interactions/123"
```

### TASK ###
1) Add logic to use this code in production and post this to the global network to get access from another computers
2) Add api to download all images by `user_id`
3) For all fixes write a full script with fixes
8) If You need you can fix code in this example
4) Write a instruction for this project if this will work in static ip 88.19.31.0


