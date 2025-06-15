from repository import get_product, create_order, reduce_product_stock

def place_order(user_id, product_id, quantity):
    product = get_product(product_id)
    if not product or product.stock < quantity:
        return None, "Product not available or insufficient stock."
    if not reduce_product_stock(product_id, quantity):
        return None, "Failed to update stock."
    order = create_order(user_id, product_id, quantity)
    return order, None
