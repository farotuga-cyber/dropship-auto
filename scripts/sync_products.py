import os, pathlib, datetime, subprocess, json

# Diretório onde os arquivos de produto serão criados
PRODUCTS_DIR = pathlib.Path('_products')
PRODUCTS_DIR.mkdir(exist_ok=True)

# -------------------------------------------------------------------
# Função de exemplo que simula a obtenção de produtos de um fornecedor.
# Substitua esta lógica por chamadas à API da AliExpress, Printful, etc.
# -------------------------------------------------------------------
def fetch_products():
    # Exemplo estático – substitua por sua chamada real à API
    return [
        {
            "id": "demo-001",
            "title": "Caneca Personalizada",
            "price": 12.99,
            "image": "https://example.com/caneca.jpg",
            "sku": "CAN-001",
            "description": "Caneca de cerâmica 300ml com impressão sublimada.\nIdeal para presentes."
        },
        {
            "id": "demo-002",
            "title": "Camiseta Unisex",
            "price": 19.90,
            "image": "https://example.com/camiseta.jpg",
            "sku": "CAM-001",
            "description": "Camiseta 100% algodão, várias cores disponíveis."
        }
    ]


def write_product_md(product):
    slug = product["title"].lower().replace(' ', '-')
    filename = PRODUCTS_DIR / f"{slug}-{product['id']}.md"
    front_matter = f"""---
layout: product
title: \"{product['title']}\"
price: {product['price']}
image: \"{product['image']}\"
sku: \"{product['sku']}\"
---
"""
    body = product.get("description", "Sem descrição.")
    filename.write_text(front_matter + "\n" + body, encoding="utf-8")


def main():
    for p in fetch_products():
        write_product_md(p)
    # Commit e push das alterações
    subprocess.run(["git", "add", "_products/"], check=True)
    msg = f"Sync catalog {datetime.datetime.utcnow().isoformat()}"
    subprocess.run(["git", "commit", "-m", msg], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)

if __name__ == "__main__":
    main()
