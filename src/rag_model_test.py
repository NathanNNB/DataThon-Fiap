from transformers import AutoTokenizer, AutoModelForCausalLM
import settings
import torch
from huggingface_hub import login

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

    def rag(self, curriculo: str, job_description: str, max_tokens: int = 500) -> str:
        """
        Gera pontos de destaque e perguntas de entrevista a partir do currículo e descrição da vaga.
        Retorna o resultado em JSON (string).
        """
        prompt = f"""
        Contexto:
        Sua tarefa é ler o texto do currículo de um candidato e a descrição da vaga e gerar exatamente:

        1. Cinco pontos de destaque do candidato, em frases curtas e diretas (máximo 2 linhas cada), resumindo experiências, conquistas, habilidades e competências mais relevantes para a vaga.
        2. Cinco perguntas estratégicas para entrevista, que explorem motivação, comportamento, soft skills, competências ou requisitos da vaga que não aparecem claramente no currículo.

        Instruções obrigatórias:
        - Use apenas informações do currículo e da vaga. Não invente fatos.
        - Seja objetivo, claro e direto nos pontos de destaque (formato de mini resumo).
        - As perguntas devem ser diferentes entre si, relevantes para a vaga e incentivar respostas com exemplos concretos.
        - Nenhum ponto de destaque pode ser repetido.
        - Nenhuma pergunta pode ser repetida.
        - Nenhuma pergunta pode repetir informações já abordadas nos pontos de destaque.
        - Considere experiências passadas, formação acadêmica, habilidades técnicas e comportamentais.
        - Não retorne o texto de entrada, nem o contexto, nem explicações adicionais.

        - A saída deve estar **exclusivamente em formato JSON**:

        ```json
          "pontos_de_destaque": [
            "Resumo curto do ponto 1",
            "Resumo curto do ponto 2",
            "Resumo curto do ponto 3",
            "Resumo curto do ponto 4",
            "Resumo curto do ponto 5"
          ],
          "perguntas_entrevista": [
            "Pergunta 1",
            "Pergunta 2",
            "Pergunta 3",
            "Pergunta 4",
            "Pergunta 5"
          ]
        ```

        Entrada: 

        Currículo:
        {curriculo}

        Vaga:
        {job_description}
        """

        messages = [
            {"role": "system", "content": "Você é um assistente de recrutamento virtual."},
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
        return result
