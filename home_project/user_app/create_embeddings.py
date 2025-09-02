# user_app/create_embeddings.py
import numpy as np
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from product_app.models import Product_image

# Load ResNet50 model
model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

product_embeddings = []
product_ids = []

# Loop through all product images
for img_obj in Product_image.objects.all():
    img_path = img_obj.image.path
    img = keras_image.load_img(img_path, target_size=(224, 224))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x).flatten()
    
    product_embeddings.append(features)
    product_ids.append(img_obj.p_id.p_id)


# Save both embeddings and IDs in a single file
data = {"embeddings": np.array(product_embeddings), "ids": np.array(product_ids)}
np.save("user_app/product_data.npy", data)

print("Embeddings and IDs saved in one file!")
