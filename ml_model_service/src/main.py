from flask import Flask, request, jsonify
from pathlib import Path
import psycopg2
import json
import base64
from datetime import datetime
import random
import torch
import ast
import logging

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
    height = metadata['height']
    width = metadata['width']

    height = (height // 8) * 8
    width = (width // 8) * 8
    try:
        img = txt2img_model(
            prompt=sd_llm_prompt, 
            negative_prompt=negative_prompt,
            strength=strength, 
            guidance_scale=guidance_scale, 
            generator=torch.manual_seed(13),
            num_inference_steps=config.NUM_INFERENCE_STEPS,
            height=height, width=width
        ).images[0]
        img.save(path_to_image)

        with open(path_to_image, 'rb') as f:
            image_bytes = f.read()
    except Exception as e:
        logging.error(f"Failed to generate image: {e}")
        image_bytes = None

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
        logging.error(f"Failed to store image path in database: {e}")
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
        metadata = ast.literal_eval(data.get('metadata'))
        unique_id = datetime.now().strftime("%d.%m.%Y_%H:%M:%S")
        image_filename = f'image_{user_id}_{unique_id}.jpg'
        image_path = IMAGE_DIR / image_filename
        img, metadata = image_generator(image_path, metadata)

        image_base64 = base64.b64encode(img).decode('utf-8')
        store_image_path_in_database(user_id, str(image_path), metadata)

        return jsonify({'image_path': str(image_path), 'image': image_base64})

    except Exception as e:
        logging.error(f"Failed to generate image: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.SERVICE_PORT)