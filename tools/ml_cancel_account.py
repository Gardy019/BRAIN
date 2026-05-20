"""
Abre o Mercado Livre em modo visivel para cancelamento de conta.
Voce faz o login manualmente; o script navega ate a pagina de encerramento.

Uso:
    python tools/ml_cancel_account.py
"""

import asyncio
from playwright.async_api import async_playwright


async def main():
    print("\n=== CANCELAMENTO DE CONTA MERCADO LIVRE ===")
    print("Abrindo navegador... faca o login na conta que deseja CANCELAR.\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome",
        )
        context = await browser.new_context(
            locale="pt-BR",
            viewport={"width": 1280, "height": 800},
        )
        page = await context.new_page()

        # Abre login do ML
        await page.goto("https://www.mercadolivre.com.br/", wait_until="domcontentloaded")

        print("Aguardando voce fazer login...")
        print("(O script continua automaticamente apos detectar o login)\n")

        # Aguarda ate o avatar/perfil aparecer (sinal de login concluido)
        try:
            await page.wait_for_selector(
                "[class*='nav-header-user'], [data-testid='header-user-info'], .nav-user-info, #nav-header-user-info",
                timeout=120000,  # 2 minutos para o usuario logar
            )
        except Exception:
            # Tenta selector alternativo — o ML muda bastante
            await page.wait_for_selector(
                "a[href*='/perfil'], a[href*='/minha-conta']",
                timeout=60000,
            )

        print("Login detectado! Navegando para configuracoes de conta...\n")
        await asyncio.sleep(1)

        # Navega direto para a pagina de encerramento de conta
        await page.goto(
            "https://www.mercadolivre.com.br/ajuda/Cancelar-minha-conta_12375",
            wait_until="domcontentloaded",
            timeout=30000,
        )

        await asyncio.sleep(2)

        # Verifica se chegou na pagina certa
        url_atual = page.url
        print(f"URL atual: {url_atual}")

        # Tenta encontrar o botao/link de cancelamento na pagina de ajuda
        cancelar_el = await page.query_selector(
            "a[href*='closeaccount'], a[href*='cancel'], button[class*='cancel'], "
            "[data-testid*='cancel'], a[href*='encerrar'], a[href*='excluir-conta']"
        )

        if cancelar_el:
            texto = await cancelar_el.inner_text()
            print(f"Botao encontrado: '{texto.strip()}'")
            print("\nATENCAO: Antes de clicar em qualquer botao de cancelamento,")
            print("confirme visualmente no navegador que esta logado na conta CORRETA.")
            input("\nPressione ENTER quando quiser que eu clique em prosseguir, ou Ctrl+C para abortar: ")
            await cancelar_el.click()
        else:
            print("\nNao encontrei botao automatico de cancelamento nesta pagina.")
            print("Opcoes manuais:")
            print("  1. Busque na pagina por 'Encerrar conta' ou 'Cancelar conta'")
            print("  2. Ou acesse: https://www.mercadolivre.com.br/minha-conta")
            print("     > Dados pessoais > Encerrar conta")
            print("\nNavegando para Minha Conta como alternativa...")
            await page.goto(
                "https://www.mercadolivre.com.br/minha-conta",
                wait_until="domcontentloaded",
            )
            print("\nO navegador esta aberto. Complete o processo manualmente.")
            print("Pressione Ctrl+C aqui no terminal quando terminar para fechar.\n")

        # Mantem o navegador aberto ate o usuario terminar
        print("\n--- Navegador aberto. Pressione Ctrl+C para encerrar o script. ---")
        try:
            while True:
                await asyncio.sleep(5)
                if page.is_closed():
                    break
        except asyncio.CancelledError:
            pass
        except KeyboardInterrupt:
            pass

        await browser.close()
        print("\nNavegador fechado. Script encerrado.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuario.")
