import os, subprocess, sys, time

# Este script orquestra o fluxo completo para teste automático
# 1. Sincroniza o catálogo
# 2. Cria uma sessão de checkout para um SKU de teste
# 3. Simula o webhook Stripe enviando o payload ao endpoint Azure Function

def run():
    cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # 1. Sync
    print('--- Sync catalog ---')
    subprocess.check_call([sys.executable, 'scripts\\sync_products.py'], cwd=cwd)
    # 2. Checkout (usa o SKU de exemplo que está no sync – ajuste se necessário)
    print('--- Create Stripe checkout ---')
    checkout_cmd = [sys.executable, 'scripts\\create_checkout.py']
    result = subprocess.check_output(checkout_cmd, cwd=cwd, text=True)
    url = result.split('Checkout URL:')[-1].strip()
    print('Checkout URL:', url)
    # 3. Simular webhook – enviar POST com payload mínimo
    print('--- Simular Stripe webhook ---')
    # Payload simplificado (em produção Stripe enviará muito mais dados)
    payload = {
        "type": "checkout.session.completed",
        "data": {"object": {"metadata": {"sku": "CAN-001"}}}
    }
    import requests, json
    webhook_url = os.getenv('AZURE_FUNCTION_URL')  # ex.: https://<app>.azurewebsites.net/api/FunctionName
    if not webhook_url:
        print('AZURE_FUNCTION_URL não definida – terminei aqui.')
        return
    r = requests.post(webhook_url, json=payload)
    print('Webhook response status:', r.status_code)
    print('Done')

if __name__ == '__main__':
    run()
