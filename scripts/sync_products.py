import os, pathlib, datetime, subprocess, json, requests

# Diretório onde os arquivos de produto serão criados
PRODUCTS_DIR = pathlib.Path('_products')
PRODUCTS_DIR.mkdir(exist_ok=True)

# -------------------------------------------------------------------
# Função de fetch real – exemplo usando a API DSers (AliExpress)
# Requer duas variáveis de ambiente:
#   DSERS_API_KEY   – token da conta DSers
#   DSERS_SUPPLIER_ID – ID do fornecedor (ex.: 123456)
# -------------------------------------------------------------------
def fetch_products():
    api_key = os.getenv('DSERS_API_KEY')
    supplier_id = os.getenv('DSERS_SUPPLIER_ID')
    if not api_key or not supplier_id:
        raise RuntimeError('Variáveis DSERS_API_KEY e DSERS_SUPPLIER_ID não configuradas')

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    page = 1
    per_page = 50  # máximo permitido pela DSers
    products = []
    while True:
        url = f'https://openapi.dsers.com/api/v2.0/supplier/{supplier_id}/products?page={page}&limit={per_page}'
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        batch = data.get('data', [])
        if not batch:
            break
        products.extend(batch)
        if len(batch) < per_page:
            break
        page += 1
    return products


def write_product_md(product):
    # O objeto retornado pela DSers possui campos como:
    #   id, title, price (dictionary with sale_price), main_image_url, sku, description
    slug = product['title'].lower().replace(' ', '-')
    filename = PRODUCTS_DIR / f"{slug}-{product['id']}.md"
    front_matter = f"""---
layout: product
title: \"{product['title']}\"
price: {product['price']['sale_price']}
image: \"{product['main_image_url']}\"
sku: \"{product['sku']}\"
---
"""
    body = product.get('description') or 'Sem descrição disponível.'
    filename.write_text(front_matter + "\n" + body, encoding='utf-8')


def main():
    products = fetch_products()
    for p in products:
        write_product_md(p)
    # Commit e push das alterações
    subprocess.run(['git', 'add', '_products/'], check=True)
    msg = f"Sync catalog {datetime.datetime.utcnow().isoformat()}"
    subprocess.run(['git', 'commit', '-m', msg], check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)

if __name__ == '__main__':
    main()
