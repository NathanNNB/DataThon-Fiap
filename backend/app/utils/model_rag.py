from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
import app.utils.settings as settings

from huggingface_hub import login
import json
import re
login(token=settings.login)

class RAGRecrutamento:
    def __init__(self, 
                 model_name="google/gemma-3-1b-it", 
                 cache_dir="../models", 
                 offload_folder="../offload", 
                 embed_model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Inicializa o modelo de geração e o modelo de embeddings para similaridade.
        """
        self.model_name = model_name

        # Tokenizer + modelo do LLM
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=f"{cache_dir}/{model_name}",
            load_in_8bit=True,
            dtype="float16"
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            offload_folder=offload_folder
        )

        # Modelo de embeddings para similaridade
        self.embed_model = SentenceTransformer(embed_model)

    def rag(self, curriculo: str, job_description: str, max_tokens: int = 900) -> dict:
        """
        Executa o RAG, calcula similaridade e retorna JSON estruturado.
        """
        prompt = f"""
        Entrada: 

        Currículo:
        {curriculo}

        Vaga:
        {job_description}
        """

        messages = [
            {"role": "system",
              "content": """ 
              Você é um assistente de recrutamento virtual.  
Sua tarefa é ler o texto do currículo de um candidato e a descrição da vaga e gerar exatamente:

1. Um resumo do currículo do candidato, **em no máximo 300 caracteres**, estruturado em uma única string, com os seguintes tópicos delimitados internamente:
    - dados_cadastrais: (endereço, objetivo profissional, tempo de experiência)
    - formacoes: (nível de formação, nível de línguas) 
    - skills_tecnicas: (habilidades hard-skills)
    - skills_softs: (habilidades soft-skills)
* IMPORTANTE: Se precisar, resuma para apenas os pontos mais relevantes para caber no limite de 300 caracteres.

2. Um resumo da vaga, **em no máximo 300 caracteres**, estruturado em uma única string, com os seguintes tópicos delimitados internamente:
    - titulo_vaga
    - requisitos_hards: (hard-skills necessárias)
    - requisitos_softs: (soft-skills necessárias)
    - extras: (informações adicionais, diferenciais, ademais)

* IMPORTANTE: Se necessário, sintetize para não ultrapassar 300 caracteres.

3. Cinco perguntas estratégicas para entrevista, que explorem motivação, comportamento, soft skills, competências ou requisitos da vaga que não aparecem claramente no currículo.

Instruções obrigatórias:
- Use apenas informações do currículo e da vaga. Não invente fatos.
-Use para o curriculo o que está em curriculo e para vaga o que está em Vaga.
- Seja objetivo, claro e direto nos pontos de destaque.
- As perguntas devem ser diferentes entre si, relevantes para a vaga e incentivar respostas com exemplos concretos.
- Nenhuma pergunta pode ser repetida.
- Nenhuma pergunta pode repetir informações já abordadas no currículo que atendam a vaga.
- **Não retorne o texto de entrada, nem o contexto, nem explicações adicionais.**
- A saída deve estar **exclusivamente em formato JSON**, válido, com o seguinte modelo:

{
  "candidateSummary": "dados_cadastrais: ... ; formacoes: ... ; skills_tecnicas: ... ; skills_softs: ...",
  "jobSummary": "titulo_vaga: ... ; requisitos_hards: ... ; requisitos_softs: ... ; extras: ...",
  "questions": [
    "Pergunta 1",
    "Pergunta 2",
    "Pergunta 3",
    "Pergunta 4",
    "Pergunta 5"
  ]
}
- Não adicione chaves diferentes das especificadas.  
              """},
            {"role": "user", "content": prompt}
        ]

        # Geração com o modelo LLM
        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)

        outputs = self.model.generate(**inputs, max_new_tokens=max_tokens)
        result = self.tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:])

        # Limpeza e parsing do JSON
        try:
            result = json.loads(re.findall(r"\{.*\}", result, re.DOTALL)[0])
        except:
            print("Erro ao decodificar JSON. Resultado bruto:")
            print(result)
            return {}

        # Recalcular similaridade usando embeddings
        candidate_summary = result.get("candidateSummary", "")
        job_summary = result.get("jobSummary", "")

        similarities = self.embed_model.similarity(self.embed_model.encode(candidate_summary), self.embed_model.encode(job_summary))

        result["compatibility_rate"] = str(similarities.tolist()[0][0])

        return result