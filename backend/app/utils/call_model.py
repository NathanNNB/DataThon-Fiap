from app.utils.model_rag import RAGRecrutamento
from app.utils.preprocessing import TextPreprocessing
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
        "candidateSummary",
        "jobSummary",
        "questions",
        "compatibility_rate"
    }

    if not isinstance(result, dict):
        return False, "Model output must be a dictionary.",500

    missing_keys = expected_keys - result.keys()
    if missing_keys:
        return False, 500

    return True, 200

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
            return "",400
    elif not isinstance(payload, dict):
        return "Input must be a JSON string or dictionary.",400

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

    return result, 200