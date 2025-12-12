# html-report-modern-formatter

Relatório HTML moderno para testes automatizados com Behave e Pytest.  
Visual elegante, responsivo e com suporte a temas escuros.

## Recursos
- Compatível com Behave e Pytest
- Layout moderno com CSS customizado
- Exportação de screenshots
- Filtros por status de execução

## Instalação
```bash
pip install html-report-modern-formatter
```

## Uso com Behave
- Configure o behave.ini:
    ```ini
    [behave.formatters]
    modern_html = html_report_modern_formatter.behave_formatter:ModernHTMLFormatter
    ```

## Uso com Pytest
- Configure o pytest.ini:
    ```ini
    [pytest]
    addopts = --modern-html=report.html
    ```

