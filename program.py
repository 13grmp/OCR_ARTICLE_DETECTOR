# ===========================================
# ETAPA 1: Instalar dependências (execute apenas 1x)
# ===========================================
# pip install pytesseract pdf2image spacy nltk openai pillow PyPDF2
# python -m spacy download pt_core_news_sm

# ===========================================
# ETAPA 2: Importar bibliotecas
# ===========================================
import pytesseract
from PIL import Image
import spacy
import nltk
import re
import io
import openai
from collections import Counter
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from nltk.corpus import stopwords
from pathlib import Path

# Baixar stopwords do NLTK (caso não tenha)
nltk.download('stopwords')

# ===========================================
# ETAPA 3: Selecionar arquivo manualmente
# ===========================================
print("📁 Informe o caminho completo do arquivo PDF ou imagem:")
file_path = input("👉 Caminho: ").strip()
file = Path(file_path)

if not file.exists():
    raise FileNotFoundError("Arquivo não encontrado. Verifique o caminho informado.")

print(f"📄 Arquivo selecionado: {file.name}")

# ===========================================
# ETAPA 4: Função de extração de texto
# ===========================================
def extract_text(file_path):
    text = ""
    if file_path.suffix.lower() == ".pdf":
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""
            
            # Caso o PDF seja só imagem (OCR)
            if len(text.strip()) < 100:
                pages = convert_from_path(file_path)
                for page in pages:
                    text += pytesseract.image_to_string(page, lang="por")
        except:
            pages = convert_from_path(file_path)
            for page in pages:
                text += pytesseract.image_to_string(page, lang="por")

    elif file_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang="por")

    return text

texto = extract_text(file)
print("🧾 Texto extraído (primeiros 500 caracteres):\n")
print(texto[:500])

# ===========================================
# ETAPA 5: Detecção de artigo científico
# ===========================================
def is_scientific_article(text):
    keywords = [
        "resumo", "abstract", "introdução",
        "metodologia", "resultados", "conclusão",
        "referências", "bibliografia"
    ]
    text_lower = text.lower()
    hits = sum(1 for word in keywords if word in text_lower)
    score = hits / len(keywords)
    return score >= 0.4

eh_artigo = is_scientific_article(texto)
if not eh_artigo:
    print("🚫 Documento inválido: O documento não é um artigo científico.")
else:
    print("✅ Documento válido: Artigo científico detectado.")

# ===========================================
# ETAPA 6: Segmentação de parágrafos
# ===========================================
nlp = spacy.load("pt_core_news_sm")

def segment_paragraphs(text):
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if len(p.strip()) > 0]
    return paragraphs

paragrafos = segment_paragraphs(texto)
print(f"🧩 Total de parágrafos detectados: {len(paragrafos)}")

# ===========================================
# ETAPA 7: Contagem de palavras e frequência
# ===========================================
def analyze_words(paragraphs):
    text = " ".join(paragraphs).lower()
    words = re.findall(r'\b\w+\b', text)
    stop = set(stopwords.words('portuguese'))
    words_clean = [w for w in words if w not in stop and len(w) > 2]
    freq = Counter(words_clean).most_common(10)
    return len(words_clean), freq

total_palavras, freq = analyze_words(paragrafos)
print(f"📄 Total de palavras: {total_palavras}")
print("🔠 Palavras mais frequentes:", freq)

# ===========================================
# ETAPA 8: Resumo com LLM (somente aqui)
# ===========================================
openai.api_key = "SUA_CHAVE_API_AQUI"  # substitua por sua chave

def gerar_resumo(texto, total_palavras, total_paragrafos):
    regra = (total_palavras > 2000 and total_paragrafos > 4)
    conformidade = "conforme" if regra else "NÃO conforme"
    prompt = f"""
    Resuma o seguinte texto em português e indique se ele está conforme à regra (>2000 palavras e >4 parágrafos):
    Texto: {texto[:4000]}...
    Resuma em 4 linhas e finalize dizendo se o texto está {conformidade}.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message.content

if not eh_artigo:
    resumo = gerar_resumo(texto, total_palavras, len(paragrafos))
    print("\n📝 Resumo Avaliativo:\n", resumo)
# ===========================================

def main():
    try:
        # Solicita caminho do arquivo
        print("📁 Informe o caminho completo do arquivo PDF ou imagem:")
        file_path = input("👉 Caminho: ").strip()
        file = Path(file_path)

        if not file.exists():
            raise FileNotFoundError("Arquivo não encontrado. Verifique o caminho informado.")

        print(f"📄 Arquivo selecionado: {file.name}")

        # Extrai texto do documento
        texto = extract_text(file)
        print("🧾 Texto extraído (primeiros 500 caracteres):\n")
        print(texto[:500])

        # Verifica se é artigo científico
        eh_artigo = is_scientific_article(texto)
        if not eh_artigo:
            print("🚫 Documento inválido: O documento não é um artigo científico.")
            return

        print("✅ Documento válido: Artigo científico detectado.")

        # Segmenta parágrafos usando técnica de segmentação
        paragrafos = segment_paragraphs(texto)
        total_paragrafos = len(paragrafos)
        print(f"🧩 Total de parágrafos detectados: {total_paragrafos}")

        # Análise de palavras e frequência
        total_palavras, palavras_frequentes = analyze_words(paragrafos)
        print(f"📄 Total de palavras: {total_palavras}")
        print("🔠 Palavras mais frequentes:")
        for palavra, freq in palavras_frequentes:
            print(f"- {palavra}: {freq} ocorrências")

        # Verifica conformidade com as regras
        esta_conforme = total_palavras > 2000 and total_paragrafos > 4
        status = "conforme" if esta_conforme else "NÃO conforme"
        
        # Gera resumo usando LLM apenas nesta etapa
        resumo = gerar_resumo(texto, total_palavras, total_paragrafos)
        print("\n📝 Resumo Avaliativo:\n", resumo)

    except Exception as e:
        print(f"❌ Erro ao processar o documento: {str(e)}")

if __name__ == "__main__":
    main()
