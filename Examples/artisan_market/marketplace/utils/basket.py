from marketplace.models import Basket, BasketItem, Product

def get_user_basket(request):
    if request.user.is_authenticated:
        basket, _ = Basket.objects.get_or_create(user=request.user)
        return basket, 'db'
    else:
        basket = request.session.get('basket', {})
        return basket, 'session'

def add_to_basket(request, product_id):
    if request.user.is_authenticated:
        basket, _ = Basket.objects.get_or_create(user=request.user)
        item, created = BasketItem.objects.get_or_create(basket=basket, product_id=product_id)
        if not created:
            item.quantity += 1
            item.save()
    else:
        # Safely get basket from session or initialize if missing
        session_basket = request.session.get('basket')
        if not isinstance(session_basket, dict):
            session_basket = {}
        
        session_basket[str(product_id)] = session_basket.get(str(product_id), 0) + 1
        request.session['basket'] = session_basket

def clear_basket(request):
    if request.user.is_authenticated:
        # Clear the DB basket for logged-in user
        Basket.objects.filter(user=request.user).delete()
    else:
        # Clear session basket for anonymous users
        request.session['basket'] = {}

def remove_from_basket(request, product_id):
    if request.user.is_authenticated:
        BasketItem.objects.filter(basket__user=request.user, product_id=product_id).delete()
    else:
        basket = request.session.get('basket', {})
        basket.pop(str(product_id), None)
        request.session['basket'] = basket

def get_basket_items(request):
    if request.user.is_authenticated:
        try:
            basket = Basket.objects.get(user=request.user)
            return [
                {
                    'product': item.product,
                    'quantity': item.quantity,
                    'total_price': item.product.price * item.quantity
                }
                for item in basket.items.all()
            ]
        except Basket.DoesNotExist:
            return []
    else:
        session_basket = request.session.get('basket', {})
        product_ids = session_basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}
        return [
            {
                'product': product_map[product_id],
                'quantity': quantity,
                'total_price': product_map[product_id].price * quantity
            }
            for product_id, quantity in session_basket.items()
            if product_id in product_map
        ]
def get_basket_total(request):
    items = get_basket_items(request)
    return sum(item['total_price'] for item in items)
