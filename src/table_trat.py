import pandas as pd 
from utils import save_bigquery, fill_na_values
import settings

from google.cloud import bigquery

client = bigquery.Client.from_service_account_json(settings.GOOGLE_CREDENTIALS)



vagas_df = client.list_rows("fiap-4.datathon.vagas").to_dataframe()



prospects_df = client.list_rows("fiap-4.datathon.prospects").to_dataframe()

applicants_df = client.list_rows("fiap-4.datathon.applicants").to_dataframe()


df = fill_na_values(vagas_df.merge(
    prospects_df,
    on="job_id",
    how="inner"
))

# LEFT JOIN com applicants (convertendo codigo → int)
df = df.merge(
    applicants_df,
    left_on=df["codigo"].astype(int),
    right_on="applicant_id",
    how="inner"
)

# Selecionar apenas as colunas da query
df = df[
    [
        "job_id",
        "informacoes_basicas_cliente",
        "informacoes_basicas_tipo_contratacao",
        "perfil_vaga_estado",
        "perfil_vaga_cidade",
        "perfil_vaga_vaga_especifica_para_pcd",
        "perfil_vaga_faixa_etaria",
        "perfil_vaga_nivel_profissional",
        "perfil_vaga_nivel_academico",
        "perfil_vaga_nivel_espanhol",
        "perfil_vaga_nivel_ingles",
        "codigo",
        "situacao_candidado",
        "infos_basicas_objetivo_profissional",
        "infos_basicas_local",
        "informacoes_pessoais_data_nascimento",
        "informacoes_pessoais_sexo",
        "informacoes_pessoais_pcd",
        "informacoes_profissionais_titulo_profissional",
        "informacoes_profissionais_area_atuacao",
        "informacoes_profissionais_certificacoes",
        "informacoes_profissionais_remuneracao",
        "informacoes_profissionais_nivel_profissional",
        "informacoes_profissionais_qualificacoes",
        "informacoes_profissionais_experiencias",
        "formacao_e_idiomas_nivel_academico",
        "formacao_e_idiomas_nivel_ingles",
        "formacao_e_idiomas_nivel_espanhol",
        "cv_pt_0"
    ]
]

save_bigquery(df, 'fiap-4.datathon.full_data')