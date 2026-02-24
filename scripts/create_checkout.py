import os, json, stripe

# Carrega chave secreta Stripe a partir de variável de ambiente
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def create_session(sku, price_cents, success_url, cancel_url):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': sku,
                },
                'unit_amount': price_cents,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={'sku': sku}
    )
    return session.url

if __name__ == '__main__':
    # Exemplo rápido – substituir pelos parâmetros reais da sua aplicação web
    sku = 'CAN-001'
    price_cents = 1299  # $12.99
    url = create_session(sku, price_cents, 'https://example.com/success', 'https://example.com/cancel')
    print('Checkout URL:', url)
