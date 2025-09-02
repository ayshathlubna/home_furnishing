import os
import django
import numpy as np
import torch
from torchvision import models, transforms
from PIL import Image

import os
import sys
import django

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home_project.settings")
django.setup()

from product_app.models import Products
import json
import numpy as np
from torchvision import models, transforms
from PIL import Image

# --- Prepare feature extractor ---
resnet = models.resnet18(pretrained=True)
resnet.eval()
feature_extractor = torch.nn.Sequential(*list(resnet.children())[:-1])

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
])

# --- Function to get embedding from image ---
def get_embedding(image_path):
    img = Image.open(image_path).convert("RGB")
    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        emb = feature_extractor(img_tensor).squeeze().numpy()
    return emb

# --- Prepare data lists ---
product_data = []
embeddings = []

for product in Products.objects.all():
    data = {
        "p_id": product.p_id,
        "name": product.p_name,
        "price": float(product.price),  # numeric
        "image": product.product_image_set.first().image.url if product.product_image_set.exists() else None
    }
    product_data.append(data)
    
    # embedding
    if product.product_image_set.exists():
        img_path = product.product_image_set.first().image.path
        emb = get_embedding(img_path)
        embeddings.append(emb)
    else:
        embeddings.append(np.zeros(512))  # fallback embedding if no image

# --- Save files ---
np.save("embeddings.npy", np.array(embeddings))
import json
with open("products.json", "w") as f:
    json.dump(product_data, f, indent=4)

print("✅ products.json and embeddings.npy generated successfully!")
