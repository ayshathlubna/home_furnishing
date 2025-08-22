# user_app/utils.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from product_app.models import Products

# ------------------------------
# Load product embeddings
# ------------------------------
data = np.load("user_app/product_data.npy", allow_pickle=True).item()
product_embeddings = np.array(data["embeddings"])
product_ids = np.array(data["ids"])  # ensure it's a NumPy array


# ------------------------------
# Helper: Get index of product
# ------------------------------
def get_product_index(product_id):
    """Return the index of a product in embeddings based on product_id."""
    idx_list = np.where(product_ids == product_id)[0]
    return idx_list[0] if len(idx_list) > 0 else None


# ------------------------------
# Image similarity
# ------------------------------
def get_image_similarity(pid):
    """Return cosine similarity of a product's embedding with all products."""
    idx = get_product_index(pid)
    if idx is None:
        return None
    emb = product_embeddings[idx].reshape(1, -1)
    sims = cosine_similarity(emb, product_embeddings)[0]
    return sims


# ------------------------------
# Category + Brand similarity
# ------------------------------
def get_category_brand_similarity(pid):
    """Return similarity scores based on category & brand."""
    try:
        target = Products.objects.get(p_id=pid)
    except Products.DoesNotExist:
        return None

    sims = []
    for p in Products.objects.all():
        score = 0
        if p.category == target.category:
            score += 0.6
        if p.brand == target.brand:
            score += 0.4
        sims.append(score)

    return np.array(sims)


# ------------------------------
# Hybrid Recommendation
# ------------------------------
def weighted_hybrid_recommendations(request, top_k=6, w_image=0.5, w_catbrand=0.3, w_history=0.2):
    """
    Generate hybrid recommendations using:
    1. Image similarity
    2. Category/Brand similarity
    3. User history (recency boost)
    """
    history = request.session.get("history", [])
    scores = np.zeros(len(product_ids))

    # --- 1. Image similarity ---
    for pid in history:
        img_sims = get_image_similarity(pid)
        if img_sims is not None:
            scores += w_image * img_sims

    # --- 2. Category/Brand similarity ---
    for pid in history:
        catbrand_sims = get_category_brand_similarity(pid)
        if catbrand_sims is not None:
            scores += w_catbrand * catbrand_sims

    # --- 3. History preference (recency boost) ---
    for i, pid in enumerate(history):
        idx = get_product_index(pid)
        if idx is not None:
            scores[idx] += w_history * (1 - i / len(history))  # more recent = higher weight

    # --- Exclude products already viewed/purchased ---
    history_indices = [get_product_index(pid) for pid in history if get_product_index(pid) is not None]
    scores[history_indices] = 0

    # --- Get top-k recommendations ---
    # Get top-k indices
    top_indices = scores.argsort()[::-1]   # sort all in descending order

    # Map to product IDs and ensure uniqueness
    seen = set()
    recommended_ids = []
    for i in top_indices:
        pid = str(product_ids[i])  # ensure string
        if pid not in seen:
            seen.add(pid)
            recommended_ids.append(pid)
        if len(recommended_ids) == top_k:
            break

    return recommended_ids
