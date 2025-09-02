from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from product_app.models import Products
import json
from .nlp_utils import parse_user_message
from django.db.models import Q

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        parsed = parse_user_message(user_message)
        min_price = parsed["min_price"]
        max_price = parsed["max_price"]
        keywords = parsed["keywords"]

        # If no filters provided, return a text response
        if not min_price and not max_price and not keywords:
            return JsonResponse({
                "type": "text",
                "response": "Please enter some search values like price range, category, or brand to find products."
            })

        products = Products.objects.all()
        query = Q()

        # Apply price filters
        if min_price is not None:
            query &= Q(price__gte=min_price)
        if max_price is not None:
            query &= Q(price__lte=max_price)

        # Apply keyword filters dynamically
        if keywords:
            q_kw = Q()
            for kw in keywords:
                q_kw |= (
                    Q(p_name__icontains=kw) |
                    Q(description__icontains=kw) |
                    Q(category__category_name__icontains=kw) |
                    Q(sub_category__sub_cat_name__icontains=kw) |
                    Q(brand__icontains=kw) |
                    Q(color__icontains=kw)
                )
            query &= q_kw

        products = products.filter(query).distinct()

        if products.exists():
            product_list = [
                {
                    "id": p.p_id,
                    "name": p.p_name,
                    "price": p.price,
                    "brand": p.brand,
                    "category": p.category.category_name if p.category else None,
                    "sub_category": p.sub_category.sub_cat_name if p.sub_category else None,
                    "color": p.color,
                    "url": f"/product_details/{p.p_id}/"
                }
                for p in products[:10]  # return max 10
            ]

            return JsonResponse({"type": "products", "products": product_list})

        return JsonResponse({"type": "text", "response": "I couldn’t find matching products."})
