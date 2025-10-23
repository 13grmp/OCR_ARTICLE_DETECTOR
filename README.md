# 🧾 Sistema de Análise e Validação de Documentos (Detecção de Artigo Científico)

## 📘 Visão Geral

Este projeto implementa um sistema que **analisa documentos em PDF ou imagem** e detecta se o conteúdo corresponde a um **artigo científico**.  
Se o documento **for um artigo**, o sistema informa que **não é válido**.  
Se **não for um artigo**, ele:

- Segmenta o texto em **parágrafos**;  
- Conta o número total de parágrafos;  
- Realiza **tokenização** e **contagem de palavras**;  
- Lista as **palavras mais frequentes**;  
- Gera um **resumo avaliativo** com auxílio de um **LLM (GPT-4o-mini)**, indicando se o documento cumpre a regra:
  > Mínimo de **2000 palavras** e **mais de 4 parágrafos**.

---

## 🚀 Como Executar

### 🧩 1. Requisitos

- Python 3.10 ou superior  
- [Tesseract OCR instalado](https://github.com/UB-Mannheim/tesseract/wiki)  
- Chave de API válida da OpenAI  

### 🧰 2. Instalação das dependências

No terminal (VS Code):

```bash
pip install pytesseract pdf2image spacy nltk openai pillow PyPDF2
python -m spacy download pt_core_news_sm

````

### ▶️ 3. Execução
Salve o arquivo Python como main.py e rode no terminal:

```bash
python main.py
````
Digite o caminho completo do arquivo PDF ou imagem quando solicitado:
```bash
📁 Informe o caminho completo do arquivo PDF ou imagem:
👉 Caminho: (caminho documento).
````

