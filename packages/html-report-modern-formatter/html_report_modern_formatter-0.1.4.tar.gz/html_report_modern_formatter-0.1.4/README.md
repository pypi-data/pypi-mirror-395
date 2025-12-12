# html-report-modern-formatter



Um formatter moderno em HTML para [Behave](https://behave.readthedocs.io/en/stable/), que gera relatórios interativos e visuais dos cenários BDD.

## ✨ Recursos
- Relatórios em HTML com layout moderno e responsivo
- Contabilização correta de cenários **Passados, Falhados, Ignorados e Erros**
- Gráficos de pizza e cards de resumo
- Suporte a screenshots por step (via Selenium)
- Integração com tags `@skip` para cenários ignorados

## 🚀 Instalação
- Após publicação no PyPI:
    ```bash
    pip install html-report-modern-formatter
    ```


## 🛠 Uso
- Execute o Behave com o formatter:
    ```bash
    behave -f modern_html -o reports/results.html
    ```

## 📂 Estrutura do relatório
- Resumo: cards com total de cenários por status
- Gráfico: pizza com distribuição dos resultados
- Detalhes: cada cenário com seus steps e screenshots

## ⚙️ Configuração de hooks
- No arquivo environment.py, adicione os hooks abaixo para suportar cenários ignorados e screenshots:
    ```python
    import os
    from datetime import datetime

    def before_scenario(context, scenario):
        # Ignora cenários marcados com @skip sem executar steps/hooks subsequentes
        if "skip" in scenario.tags:
            scenario.skip("Ignorado pelo marcador @skip")

    def after_step(context, step):
        # cria pasta se não existir
        os.makedirs("reports/screenshots", exist_ok=True)

        # gera nome único com timestamp
        timestamp = datetime.now().strftime("%y_%m_%d_%H_%M_%S")
        image_name = step.name.replace(' ', '_').replace('"', '')
        filename = f"reports/screenshots/{image_name}_{timestamp}.png"

        # salva screenshot via Selenium (somente se driver existir)
        if hasattr(context, "driver"):
            context.driver.save_screenshot(filename)
            # caminho relativo para o HTML
            step.screenshot = f"screenshots/{image_name}_{timestamp}.png"
        
    ```

## 📸 Screenshots
- Os screenshots capturados em cada step são exibidos automaticamente no relatório HTML.

# 📜 Licença
- Distribuído sob a licença MIT. Veja LICENSE para mais detalhes.

---

## 📦 Descrição para PyPI
> *Modern HTML formatter for Behave BDD reports. Generates interactive HTML reports with scenario statistics, charts, and screenshots support. Handles passed, failed, skipped, and error scenarios correctly.*

