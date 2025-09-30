from transformers import AutoTokenizer, AutoModelForCausalLM
import settings
import torch
from huggingface_hub import login
import json
import re
login(token=settings.login)

class RAGRecrutamento:
    def __init__(self, model_name="google/gemma-3-1b-it", cache_dir="../models", offload_folder="../offload"):
        """
        Inicializa o modelo e o tokenizer para RAG.
        """
        self.model_name = model_name
        
        # Carregar tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=f"{cache_dir}/{model_name}",
            load_in_8bit=True,
            dtype="float16"
        )
        
        # Carregar modelo
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            offload_folder=offload_folder
        )

    def rag(self, curriculo: str, job_description: str, max_tokens: int = 900) -> str:
        """
        Gera pontos de destaque e perguntas de entrevista a partir do currículo e descrição da vaga.
        Retorna o resultado em JSON (string).
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

4. Uma taxa de compatibilidade entre o candidato e a vaga, em decimal com o máximo de valor sendo 1.00 e o mínimo 0.00, considerando hard e soft skills, experiências anteriores, formação acadêmica e outros fatores relevantes.

Instruções obrigatórias:
- Use apenas informações do currículo e da vaga. Não invente fatos.
- Seja objetivo, claro e direto nos pontos de destaque.
- As perguntas devem ser diferentes entre si, relevantes para a vaga e incentivar respostas com exemplos concretos.
- Nenhuma pergunta pode ser repetida.
- Nenhuma pergunta pode repetir informações já abordadas no currículo que atendam a vaga.
- Considere experiências passadas, formação acadêmica, habilidades técnicas e comportamentais.
- **Não retorne o texto de entrada, nem o contexto, nem explicações adicionais.**
- A saída deve estar **exclusivamente em formato JSON**, válido, com o seguinte modelo:

{
  "resumo_candidato": "dados_cadastrais: ... ; formacoes: ... ; skills_tecnicas: ... ; skills_softs: ...",
  "resumo_vaga": "titulo_vaga: ... ; requisitos_hards: ... ; requisitos_softs: ... ; extras: ...",
  "perguntas_entrevista": [
    "Pergunta 1",
    "Pergunta 2",
    "Pergunta 3",
    "Pergunta 4",
    "Pergunta 5"
  ],
  "taxa_de_compatibilidade": "X.XX"
}
- Não adicione chaves diferentes das especificadas.  

        """},
            {"role": "user", "content": prompt}
        ]

        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)

        outputs = self.model.generate(**inputs, max_new_tokens=max_tokens)
        result = self.tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:])
        try:
            result = json.loads(re.findall(r"\{.*\}", result, re.DOTALL)[0] )
        except:
            print("Erro ao decodificar JSON. Resultado bruto:")
            print(result)
        return result
