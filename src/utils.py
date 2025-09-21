import pandas as pd 
from google.cloud import bigquery
import settings

def transform_df(df: pd.DataFrame, name_index: str) -> pd.DataFrame:
    ''' Transforma um DataFrame onde cada célula contém um dicionário em um DataFrame "achatado",
    com colunas expandidas e prefixadas pelo nome da coluna original.
    
    Args:
        df (pd.DataFrame): DataFrame de entrada onde cada célula contém um dicionário.
        name_index (str): Nome para a coluna de índice no DataFrame resultante.
    Returns:
        pd.DataFrame: DataFrame transformado com colunas expandid'''
    df_t = df.T
    df_t.index.name = name_index

    # Expandir cada coluna (que contém dicionários) em colunas separadas
    dfs_expand = []
    df_final = []
    for col in df_t.columns:
        # Expandir os dicionários
        expanded = df_t[col].apply(pd.Series)
        
        # Prefixar com o nome da coluna original
        expanded = expanded.add_prefix(f"{col}_")
        
        dfs_expand.append(expanded)

    # Concatenar todos os pedaços junto com o job_id
    df_final = pd.concat(dfs_expand, axis=1)
    df_final.reset_index(inplace=True)
    return df_final


def explode_prospects(df: pd.DataFrame, prefix: str = "prospects_") -> pd.DataFrame:
    """
    Transforma um DataFrame que contém várias colunas de prospects em uma estrutura normalizada,
    com uma linha por job_id/prospect.

    Args:
        df (pd.DataFrame): DataFrame de entrada contendo colunas no formato prospects_0, prospects_1, etc.
        prefix (str): Prefixo usado para identificar as colunas de prospects. Default = "prospects_".

    Returns:
        pd.DataFrame: DataFrame com uma linha por job_id/prospect.
    """

    # Identificar colunas de prospects
    prospect_cols = [c for c in df.columns if c.startswith(prefix)]

    # Transforma de wide -> long
    df_long = df.melt(
        id_vars=[c for c in df.columns if c not in prospect_cols],  # mantém job_id, titulo, etc.
        value_vars=prospect_cols,
        var_name="prospect_num",
        value_name="prospect"
    )

    # Remove linhas sem prospect
    df_long = df_long.dropna(subset=["prospect"])

    # Expande os dicionários
    df_prospects = df_long["prospect"].apply(pd.Series)

    # Junta no DataFrame final
    df_final = pd.concat([df_long.drop(columns=["prospect"]), df_prospects], axis=1)

    # Deixa prospect_num como número (opcional)
    df_final["prospect_num"] = df_final["prospect_num"].str.replace(prefix, "").astype(int)

    return df_final

def save_bigquery(
    df: pd.DataFrame, 
    table_id: str, 
    partition_field: str | None = None
):
    """
    Salva um DataFrame no BigQuery, sobrescrevendo a tabela se já existir.
    Pode particionar por um campo de data/datetime.

    Args:
        df (pd.DataFrame): DataFrame a ser salvo.
        table_id (str): ID completo da tabela no formato `project.dataset.table`.
        partition_field (str | None): Nome da coluna para particionar (precisa ser DATE/DATETIME/TIMESTAMP).
    """
    client = bigquery.Client.from_service_account_json(settings.GOOGLE_CREDENTIALS)

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  # Sobrescreve a tabela
        autodetect=True,
    )

    # Adiciona partição caso seja especificada
    if partition_field:
        job_config.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,  # Padrão é por dia
            field=partition_field                     # Coluna usada para particionar
        )

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # Aguarda conclusão

    print(f"✔ Data saved at table: {table_id} (partition: {partition_field if partition_field else 'none'})")


def changeColumns(df: pd.DataFrame) -> pd.DataFrame:
    ''' Transforma os nomes das colunas: tira espaços, substitui por underline e deixa em minúsculo
    Args:
        df (pd.DataFrame): DataFrame a ser transformado.   
    Returns:
        pd.DataFrame: DataFrame com colunas transformadas.'''
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()
    return df

def normalizeDataFrame(df: pd.DataFrame) -> pd.DataFrame:
    ''' Normaliza os dados do DataFrame: minúsculo, remove duplicados e reseta o índice
    Args:
        df (pd.DataFrame): DataFrame a ser normalizado.
    Returns:
        pd.DataFrame: DataFrame normalizado.
    '''
    df = df.map(lambda x: x.lower() if isinstance(x, str) else x).drop_duplicates().reset_index(drop=True)
    return df

def adjust_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajusta automaticamente os dtypes de um DataFrame:
      - Converte colunas numéricas para int ou float
      - Converte colunas de datas para datetime
      - Mantém como string o que não for possível converter
    """
    df = df.copy()
    
    for col in df.columns:
        # Tenta converter para datetime
        try:
            converted = pd.to_datetime(df[col],format='dd-MM-yyyy', errors="raise", utc=False)
            df[col] = converted
            continue
        except Exception:
            pass
        
        # Tenta converter para numérico
        try:
            converted = pd.to_numeric(df[col], errors="raise")
            # Se todos forem inteiros, usa int
            if pd.api.types.is_integer_dtype(converted):
                df[col] = converted.astype("Int64")  # int nulo seguro
            else:
                df[col] = converted.astype(float)
            continue
        except Exception:
            pass
        
        # Se não converteu nada, garante que seja string
        df[col] = df[col].astype(str)
    
    return df

def fill_na_values(
    df: pd.DataFrame, 
    fill_int: int = 0, 
    fill_float: float = 0.0, 
    fill_str: str = "Não identificado"
) -> pd.DataFrame:
    """
    Preenche valores nulos no DataFrame:
      - Colunas int → fill_int
      - Colunas float → fill_float
      - Colunas string → fill_str
      - Datetime → mantém NaT
    """
    df = df.copy()

    for col in df.columns:
        if pd.api.types.is_integer_dtype(df[col]):
            df[col] = df[col].fillna(fill_int).astype("Int64")
        elif pd.api.types.is_float_dtype(df[col]):
            df[col] = df[col].fillna(fill_float)
        elif pd.api.types.is_string_dtype(df[col]):
            df[col] = df[col].fillna(fill_str)

    return df


def adjustDataframe(df: pd.DataFrame, name_index: str, explode_df: bool = False) -> pd.DataFrame:
    ''' Realiza uma série de transformações no DataFrame, incluindo transformação, explosão de prospects,
    mudança de nomes de colunas e normalização dos dados.
    Args:
        df (pd.DataFrame): DataFrame a ser ajustado.
        name_index (str): Nome para a coluna de índice no DataFrame resultante.
        explode_df (bool): Indica se deve explodir os prospects em linhas separadas.
    Returns:
        pd.DataFrame: DataFrame ajustado.
    '''
    df = transform_df(df, name_index)
    if explode_df:
        df = explode_prospects(df)
    df = changeColumns(df)
    df = normalizeDataFrame(df)
    df = adjust_dtypes(df)
    df = fill_na_values(df)
    return df