import random


art_styles = ['Photorealism', 'Classicism', 'Land Art', 'Realism', 'modernist']
resolutions = ['unreal engine', 'sharp focus', '8k', 'vray']
lighting = ['cinematic', 'dark', 'sunlight', 'god rays']
required_colors = ['light salmon', 'pale turquoise', 'royal blue']
locations = ['urban', 'countryside', 'beach', 'mountain', 'forest']
landscapes = ['cityscape', 'seascape', 'mountainscape', 'countryscape', 'sunset']
activities = ['sport', 'work', 'relaxation', 'travel', 'entertainment', 'meditation', 'exploration', 'buisness']
attributes = ['mobile phone', 'coffee', 'book',  'car', 'house']


def generate_prompt(age: int = 30, sex: str = '', product: str = 'people', custom_prompt: str = '') -> str:
    """
    Generate a prompt for the ML model.
    
    Parameters
    ----------
    age : int
        The age of the subject.
    sex : str
        The sex of the subject ('male' or 'female' or '').
    product : str
        The product category for generation ('people', 'car', 'house', 'credit card').
    custom_prompt : str
        Custom words to include in the generation prompt.
    
    Returns
    -------
    str
        The generated prompt.
    """
    age_group = ''
    if 'people' in product and sex:
        gender = f"a well dressed {sex.lower()}"
        if age < 11:
            age_group = 'child'
        elif age < 18:
            age_group = 'teenager'
        elif age < 26:
            age_group = 'young adult'
        elif age < 51:
            age_group = 'adult'
        else:
            age_group = 'senior'
    else:
        gender = "an object"
        age_group = ""

    if 'card' in product:
        attribute = "a payment card without digits"
        activity = "being used"
    elif 'house' in product:
        attribute = "a building"
        activity = "inhabited"
    elif 'car' in product:
        attribute = "a vehicle"
        activity = "parked"
    else:
        attribute = random.choice(attributes)
        activity = random.choice(activities)

    prompt = f"The image must include the colors {', '.join(required_colors)}.{custom_prompt} Depict {gender} {age_group} involved in {activity} with {attribute}."
    prompt += f" The scene should be in a {random.choice(locations)} setting, rendered in {random.choice(resolutions)} resolution."
    prompt += f" Ensure the use of {random.choice(lighting)} lighting and {random.choice(art_styles)} style."

    return prompt


def generate_negative_prompt(product: str = 'people') -> str:
    """
    Generate a negative prompt for the ML model.
    
    Parameters
    ----------
    product : str
        The category for generation.
    
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
    if 'people' in product:
        negative_prompt = "avoid any depiction of animals objects." + negative_prompt
    elif 'people' not in product:
        negative_prompt = "avoid any depiction of digits and letters.avoid plates with letters and numbers.avoid any depiction of humans or human-like figures." + negative_prompt
        
    return negative_prompt
