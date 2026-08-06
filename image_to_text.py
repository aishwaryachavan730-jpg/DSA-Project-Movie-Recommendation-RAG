from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Load model only once
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

def image_caption(uploaded_file):

    if uploaded_file is None:
        return "No image uploaded."

    try:
        image = Image.open(uploaded_file).convert("RGB")

        inputs = processor(image, return_tensors="pt")

        output = model.generate(**inputs)

        caption = processor.decode(
            output[0],
            skip_special_tokens=True
        )

        return caption

    except Exception as e:
        return f"Error: {e}"