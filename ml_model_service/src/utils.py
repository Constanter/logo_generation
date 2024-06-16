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
