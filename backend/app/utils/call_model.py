from rag_model_test import RAGRecrutamento
from preprocessing import TextPreprocessing
import json

# instanciar apenas uma vez
rag_model = RAGRecrutamento()
preprocessing = TextPreprocessing()

def preprocess(text: str) -> str:
    """Função auxiliar para aplicar o pipeline de limpeza em um único texto."""
    return preprocessing.preprocess_text(
        [text],
        apply_lower=True,
        remove_ponctuation=True,
        remove_numbers=True,
        clean_html=True,
        apply_unidecode=True,
        remove_stopwords=True,
        remove_duplicates=True
    )

def validate_model_output(result: dict) -> tuple[bool, str]:
    """
    Valida se o output do modelo está no formato correto.
    Retorna (True, "") se válido ou (False, msg_erro) se inválido.
    """
    expected_keys = {
        "resumo_candidato",
        "resumo_vaga",
        "perguntas_entrevista",
        "taxa_de_compatibilidade"
    }

    if not isinstance(result, dict):
        return False, "Model output must be a dictionary."

    missing_keys = expected_keys - result.keys()
    if missing_keys:
        return False, f"Model output is missing required keys: {', '.join(missing_keys)}"

    return True, ""

def call_model(payload: str | dict) -> str:
    """
    Recebe um JSON (string ou dict) com 'curriculo' e 'job_description',
    aplica preprocessamento e retorna o resultado do modelo RAG.
    """
    # Garantir que o input é dict
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            return "Invalid JSON string. Provide a valid JSON with 'curriculo' and 'job_description'."
    elif not isinstance(payload, dict):
        return "Input must be a JSON string or dictionary."

    curriculo = payload.get("curriculo", "").strip()
    job_description = payload.get("job_description", "").strip()

    if not curriculo or not job_description:
        return "Both 'curriculo' and 'job_description' must be provided and non-empty."

    # preprocessar textos
    curriculo_processed = preprocess(curriculo)
    job_description_processed = preprocess(job_description)


    # chamar modelo
    result = rag_model.rag(curriculo_processed, job_description_processed)

    # validar saída
    is_valid, error_msg = validate_model_output(result)
    if not is_valid:
        return result, error_msg

    return result, 'Retorno com sucesso.'