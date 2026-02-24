import os, json, requests

# Carregar credenciais do fornecedor (exemplo DSers/Printful)
SUPPLIER_API_KEY = os.getenv('SUPPLIER_API_KEY')
SUPPLIER_ID = os.getenv('SUPPLIER_ID')

def create_supplier_order(sku, quantity, shipping):
    # Exemplo genérico – ajuste para a API real do fornecedor que escolher
    url = f'https://api.example.com/v1/suppliers/{SUPPLIER_ID}/orders'
    payload = {
        'sku': sku,
        'quantity': quantity,
        'shipping': shipping
    }
    headers = {'Authorization': f'Bearer {SUPPLIER_API_KEY}', 'Content-Type': 'application/json'}
    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()

def handler(event, context=None):
    # Stripe envia JSON no corpo da requisição
    data = json.loads(event['body'])
    if data['type'] != 'checkout.session.completed':
        return {'statusCode': 400}
    session = data['data']['object']
    sku = session['metadata']['sku']
    shipping = session.get('shipping', {}).get('address', {})
    order = create_supplier_order(sku, 1, shipping)
    # Aqui você pode enviar e‑mail ao cliente com o número de rastreio
    print('Order created:', order)
    return {'statusCode': 200}
