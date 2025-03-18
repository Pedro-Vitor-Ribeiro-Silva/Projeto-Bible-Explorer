from flask import Flask, render_template, request
import google.generativeai as genai
import requests

app = Flask(__name__)
genai.configure(api_key="")

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':

        if 'tema' in request.form:  # Usuário pesquisou por tema
            versao_da_biblia = request.form.get('bibleVersion', 'almeida')  # Define um padrão
            tema = request.form.get('tema')
            print(tema)
            model = genai.GenerativeModel('gemini-2.0-flash')
            prompt = f"""Me forneça apenas a parte final da seguinte URL no formato correto, sem explicações ou textos adicionais: 
            https://bible-api.com/livro+capitulo:versiculo?translation={versao_da_biblia}. 

            Substitua "livro", "capitulo" e "versiculo" por um versículo real da Bíblia que esteja diretamente relacionado ao tema solicitado: "{tema}".  
            Certifique-se de que a resposta contenha um livro bíblico válido, um número de capítulo e um número de versículo.  
            Se não houver nenhum versículo relevante para esse tema, responda apenas com "NÃO ENCONTRADO", sem qualquer explicação adicional.

            Sua resposta deve conter **somente** a parte final da URL ou "NÃO ENCONTRADO", sem qualquer outro texto."""
            response = model.generate_content(prompt)

            texto_gemini = response.text.strip()
            print(f"Resposta da IA: {texto_gemini}")

            # Se a IA retornar "NÃO ENCONTRADO", exibimos uma mensagem de erro no template
            if texto_gemini.upper() == "NÃO ENCONTRADO":
                return render_template('index.html', erro="Nenhum versículo encontrado para esse tema.")

            # Validação da resposta da IA
            try:
                 # Consulta a API da Bíblia
                url = f'https://bible-api.com/{texto_gemini}'
                response_bible = requests.get(url)

                if response_bible.status_code != 200:
                    raise ValueError("Erro ao buscar versículo na API da Bíblia")

                data = response_bible.json()
                referencia_versiculo = data.get('reference', 'Referência não encontrada')
                versiculo_text = data.get('verses', [{'text': 'Texto não encontrado'}])[0]['text']

                return render_template('index.html', referencia_versiculo=referencia_versiculo, versiculo_text=versiculo_text, versao_da_biblia=versao_da_biblia)

            except Exception as e:
                print(f"Erro: {e}")
                return render_template('index.html', erro=f"Erro ao processar a resposta: {e}")
        
        
        
        else:
            versao_da_biblia = request.form.get('bibleVersion')
            livro = request.form.get('bible-book')
            capitulo = request.form.get('bible-chapter')
            versiculo = request.form.get('bible-verse')

            # Validação: Verificar se todos os campos necessários estão presentes
            if not livro or not capitulo or not versiculo:
                return render_template('index.html', erro="Por favor, preencha todos os campos: livro, capítulo e versículo.")

            # Validação: Verificar se capitulo e versículo são números válidos
            if not capitulo.isdigit() or not versiculo.isdigit():
                return render_template('index.html', erro="Capítulo e versículo devem ser números válidos.")

            # Criar a URL para a consulta
            url = f'https://bible-api.com/{livro}+{capitulo}:{versiculo}?translation={versao_da_biblia}'

            try:
                response = requests.get(url)

                # Verificar se a resposta foi bem-sucedida
                if response.status_code != 200:
                    raise ValueError("Erro ao buscar versículo na API da Bíblia")

                data = response.json()
                referencia_versiculo = data.get('reference', 'Referência não encontrada')
                versiculo_text = data.get('verses', [{'text': 'Texto não encontrado'}])[0]['text']

                return render_template('index.html', referencia_versiculo=referencia_versiculo, versiculo_text=versiculo_text, versao_da_biblia=versao_da_biblia)

            except Exception as e:
                # Caso ocorra algum erro durante a requisição
                return render_template('index.html', erro=f"Erro ao processar a solicitação: {e}")






if __name__ == '__main__':
    app.run(debug=True)
