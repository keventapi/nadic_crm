from .models import Sales, Comissions

def calcular_faturamento(vendas):
    faturamento_total = 0
    faturamento_empresa = 0
    for i in vendas:
        faturamento_total += i.total_product_sale
        faturamento_empresa = i.company_net_earning
    return faturamento_total, faturamento_empresa

def get_latest_comission():
    latest_comissions = Comissions.objects.order_by('-id').first()
    if latest_comissions is None:
        latest_comissions = Comissions(owner_share = 0.9,
                                      company_commission = 0.1)
        latest_comissions.save()
    return latest_comissions

def handle_sales_from_cart(products_list):
    latest_comissions = get_latest_comission()
    for cartitem in products_list:
        sale = Sales(product = cartitem.product,
                 quantity = cartitem.quantity,
                 price_at_sale = cartitem.product.product_price,
                 comissions = latest_comissions,
                 owner_share_at_sale = latest_comissions.owner_share,
                 company_commission_at_sale = latest_comissions.company_commission)
        sale.save()
        
def handle_unique_sells(product, quantity):
    latest_comissions = get_latest_comission()
    sale = Sales(product = product,
                 quantity = quantity,
                 price_at_sale = product.product_price,
                 comissions = latest_comissions,
                 owner_share_at_sale = latest_comissions.owner_share,
                 company_commission_at_sale = latest_comissions.company_commission)
    sale.save()