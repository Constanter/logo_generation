import gradio as gr
import requests
from PIL import Image
from io import BytesIO
import base64
import pandas as pd
import psycopg2
import logging
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
            logging.info("Database is available.")
            break
        except Exception as e:
            logging.info(f"Database not available yet, waiting... Error: {e}")
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
    metadata_input = gr.Textbox(label="Metadata", value="{'age': 20, 'sex': 'male', 'product': 'people', 'custom_prompt': '', 'height': 720, 'width': 720}")
    output_data = gr.Image()
    mark_result_button = gr.Button("Send Mark image to database")
    history_viewer = gr.Dataframe(headers=["id", "image_url", "metadata", "user_id"], datatype=["str", "str", "str", "str"])
    get_history_button = gr.Button("Get History by user ID")
    
    get_history_button.click(get_history, inputs=input_data, outputs=history_viewer)
    mark_result_button.click(mark_image, inputs=[input_data, gr.Checkbox(label="Mark As Good Image")], outputs=None)



    interface = gr.Interface(
        fn=generate_image,
        inputs=[input_data, metadata_input],
        outputs=[output_data],
        live=False
    )
    gr.Markdown(
            """
            # Инструкция по использованию сервиса:
            
            ## Принцип генерации изображения
                Для генерации изображения будут использованы парамертры заданные в метаданных. Под капотом метаданные обогащаются промптом. Все изображеиня генерятся в одной цветовой гамме (трех цветах банка - 'светло-лососевый', 'бледно-бирюзовый', 'королевский синий'). Есть возможность задать категорию продукта. Это могут быть либо генерация продающих изображений людей, либо генерации под продукты(машины, дома, кредитные карты). Если задана категория продукта `product` - `people`, то изображения будут генерироваться только с людьми. Можно обогащать промпт с помощью метаданных `custom_prompt`(то что должно еще присутсвовать на изображение).
            
            ## Идентификатор пользователя
                - `user_id`: Идентификатор пользователя. Например `Test user`. Может быть любым.


            ## Метаданные
            Метаданные могут содержать следующие поля:

            - `sex`: Пол пользователя. Может быть либо 'male' либо 'female' можно оставить пустым.
            - `age`: Возраст пользователя. число.
            - `product`: Категория продукта. Может быть либо 'people', либо 'car', либо 'house', либо 'credit card' можно оставить пустым.
            - `custom_prompt`: Пользовательский промпт. Может быть либо строкой либо пустым. Добавит на генерацию предметы или свойства предметов.
            - `height`: Высота изображения. Число. (сумма высоты и ширины должна быть не больше 3500, из-за использования слабой видеокарты.)
            - `width`: Ширина изображения. Число. (сумма высоты и ширины должна быть не больше 3500, из-за использования слабой видеокарты.)
            
            ## Пример метаданных:
            1) 
            ```
            {
                "sex": "male",
                "age": 20,
                "product": "car",
                "custom_prompt": "engaging in driving",
                "height": 720,
                "width": 720
            }
            ```
            2) 
            ```
            {
                "sex": "male",
                "age": 20,
                "height": 480,
                "width": 1160
            }
            ```
            3) 
            ```
            {
                "product": "house",
                "custom_prompt": "beautiful country house",
                "height": 1080,
                "width": 1080
            }
            ```

            ## Генерация изображения
            
            Для генерации изображения необходимо ввести метаданные в поле `metadata` и имя пользователя в поле `user_id` и нажать на кнопку `Generate Image`.
            
            ## Разметка изображения
            
            Для разметки изображения необходимо ввести метаданные в поле `metadata` и нажать на кнопку `Generate Image`. После если изображение хоршее и понравилось нажать на кнопку `Mark As Good Image`(выставляется метка True) или оставить чекбокс пустым(False). Отправить изображение в базу данных, нажать на кнопку `Send Mark image to database`.
            
            ## Получение истории сгенерированных изображений для пользователя
            
            Ввести в поле `user_id` имя пользователя для которого нужно получить историю и нажать на кнопку `Get History by user ID`. В вверху странице появится таблица с историей сгенерированных изображений для данного пользователя.
            """)

if __name__ == '__main__':
    demo.launch(server_name="0.0.0.0", server_port=config.SERVICE_PORT)
    
