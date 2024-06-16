from flask import Flask, request, jsonify, send_file
import os
import zipfile
from io import BytesIO
import psycopg2
import requests
from . import config

app = Flask(__name__)


# Add this function to handle downloading all images by user_id
@app.route('/api/download/images/<user_id>', methods=['GET'])
def download_images(user_id: str):
    # Retrieve all image paths for the given user_id from the database
    conn = psycopg2.connect(**config.DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT image_url FROM interactions WHERE user_id = %s", (user_id,))
    image_paths = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()

    # Prepare the zip file response
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for image_path in image_paths:
            zipf.write(image_path, arcname=os.path.basename(image_path))

    # Set the headers for file download
    memory_file.seek(0)
    return send_file(memory_file, as_attachment=True, attachment_filename=f"{user_id}_images.zip", mimetype='application/zip')


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
    