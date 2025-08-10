# Guia de Configuração do Ambiente para Teste com Fooocus-API

## 1. Instale o Fooocus-API

- Clone o repositório oficial do Fooocus-API ou baixe a versão desejada.
- Siga as instruções do README do Fooocus-API para instalar dependências e iniciar o serviço.

## 2. Instale as dependências do projeto

No terminal, execute:
```pwsh
pip install -r requirements.txt
```

Certifique-se de que o Python e o pip estejam instalados e configurados.

## 3. Configure as variáveis de ambiente

Defina a URL do Fooocus-API (normalmente rodando localmente):
```pwsh
$env:FOOOCUS_URL="http://127.0.0.1:7865"
```

## 4. Execute o Fooocus-API

No diretório do Fooocus-API, execute:
```pwsh
python app.py
```
Ou siga o comando recomendado pelo projeto.

## 5. Teste a geração de imagens

Execute o script principal do seu projeto:
```pwsh
python src/main.py
```

Se tudo estiver correto, a imagem será gerada usando a API Fooocus.

## Observações
- Certifique-se de que a porta 7865 esteja livre e o serviço Fooocus-API esteja rodando.
- Ajuste o valor de `FOOOCUS_URL` se usar outra porta ou endereço.
- Consulte a documentação do Fooocus-API para endpoints e parâmetros atualizados.
