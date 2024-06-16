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
    
