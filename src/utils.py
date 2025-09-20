import pandas as pd 


def transform_df(df: pd.DataFrame, name_index: str) -> pd.DataFrame:
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