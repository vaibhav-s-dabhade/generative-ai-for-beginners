from openai import AzureOpenAI
import os
import requests
from PIL import Image
import dotenv
import json
import uuid

# import dotenv
dotenv.load_dotenv()

 

# Assign the API version (DALL-E is currently supported for the 2023-06-01-preview API version only)
client = AzureOpenAI(
  api_key=os.environ['AZURE_OPENAI_KEY'],  # this is also the default, it can be omitted
  api_version = "2023-12-01-preview",
  azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'] 
  )

model = os.environ['AZURE_OPENAI_IMAGEGEN_DEPLOYMENT']


try:
    # Create an image by using the image generation API
    #prompt = "A bunny on a horse, holding a lollipop, on a foggy meadow where daffodils grow. The bunny says 'hello'."  # Enter your prompt text here
    prompt = "lady of age around 30, celebrating birthday of her daughter with family inside house"  # Enter your prompt text here
    result = client.images.generate(
        model=model,
        prompt=prompt,
        size='1024x1024',
        n=1
    )

    generation_response = json.loads(result.model_dump_json())
    # Set the directory for the stored image
    image_dir = os.path.join(os.curdir, 'images')

    # If the directory doesn't exist, create it
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # Initialize the image path (note the filetype should be png)
    #image_path = os.path.join(image_dir, 'generated-image.png')
    
    # Generate a unique filename
    filename = f'vaibhav_{uuid.uuid4()}.png'
    image_path = os.path.join(image_dir, filename)

    # Retrieve the generated image
    image_url = generation_response["data"][0]["url"]  # extract image URL from response
    generated_image = requests.get(image_url).content  # download the image
    with open(image_path, "wb") as image_file:
        image_file.write(generated_image)

    # Display the image in the default image viewer
    image = Image.open(image_path)
    image.show()

# catch exceptions
#except client.error.InvalidRequestError as err:
#    print(err)

finally:
    print("completed!")
# ---creating variation below---


# response = client.Image.create_variation(
#   image=open(image_path, "rb"),
#   n=1,
#   size="1024x1024"
# )

