import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from product_app.models import Products
from cart_app.models import Cart,Wishlist
from order_app.models import Order  # if you track purchases
import os

# ------------------------------
# Load product embeddings
# ------------------------------
from django.conf import settings

file_path = os.path.join(settings.BASE_DIR, "user_app", "product_data.npy")
data = np.load(file_path, allow_pickle=True).item()

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
    target = Products.objects.get(p_id=pid)
    sims = []
    for db_pid in product_ids:  # loop over embeddings list
        try:
            p = Products.objects.get(p_id=db_pid)
        except Products.DoesNotExist:
            sims.append(0)
            continue

        score = 0
        if p.category == target.category:
            score += 0.6
        if p.brand == target.brand:
            score += 0.4
        sims.append(score)

    return np.array(sims)


# ------------------------------
# User preference similarity
# ------------------------------
def get_user_preference_similarity(user):
    """Return similarity scores based on user's wishlist, cart, orders."""
    prefs = {}

    # Wishlist (assuming it has FK to Products)
    for w in Wishlist.objects.filter(user=user):
        product = getattr(w, "product", None)
        if not product and hasattr(w, "p_id"):
            try:
                product = Products.objects.get(p_id=w.p_id)
            except Products.DoesNotExist:
                continue
        if product:
            key = (product.category, product.brand)
            prefs[key] = prefs.get(key, 0) + 1

    # Cart
    for c in Cart.objects.filter(user=user):
        product = getattr(c, "product", None)
        if not product and hasattr(c, "p_id"):
            try:
                product = Products.objects.get(p_id=c.p_id)
            except Products.DoesNotExist:
                continue
        if product:
            key = (product.category, product.brand)
            prefs[key] = prefs.get(key, 0) + 2  # cart stronger weight

    # Orders
    for o in Order.objects.filter(user=user):
        product = getattr(o, "product", None)
        if not product and hasattr(o, "p_id"):
            try:
                product = Products.objects.get(p_id=o.p_id)
            except Products.DoesNotExist:
                continue
        if product:
            key = (product.category, product.brand)
            prefs[key] = prefs.get(key, 0) + 3  # purchases = strongest

    # Build vector over all products
    sims = []
    for db_pid in product_ids:
        try:
            p = Products.objects.get(p_id=db_pid)
        except Products.DoesNotExist:
            sims.append(0)
            continue

        sims.append(prefs.get((p.category, p.brand), 0))

    return np.array(sims)


# ------------------------------
# Hybrid Recommendation
# ------------------------------
def weighted_hybrid_recommendations(request, top_k=6,
                                    w_image=0.4, w_catbrand=0.2, w_history=0.2, w_user=0.2):
    """
    Generate hybrid recommendations using:
    1. Image similarity
    2. Category/Brand similarity
    3. User history (recency boost)
    4. User preferences (wishlist/cart/orders)
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

    # --- 4. User preference signals ---
    if request.user.is_authenticated:
        user_sims = get_user_preference_similarity(request.user)
        scores += w_user * user_sims

    # --- Exclude already viewed ---
    history_indices = [get_product_index(pid) for pid in history if get_product_index(pid) is not None]
    scores[history_indices] = -np.inf

    # --- Get top-k recommendations ---
    top_indices = np.argsort(scores)[::-1]
    recommended_ids = []
    seen = set()
    for i in top_indices:
        if i < 0 or i >= len(product_ids):
            continue
        pid = str(product_ids[i])
        if pid not in seen:
            seen.add(pid)
            recommended_ids.append(pid)
        if len(recommended_ids) == top_k:
            break

    return recommended_ids
