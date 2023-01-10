import pandas as pd
import datacompy


def main():

    df_aeros = get_ready_to_compare_aeros()
    df_arte = get_ready_to_compare_arte()


    compare = datacompy.Compare(df_aeros,df_arte,join_columns=['cm', 'Verba'],df1_name='aeros', df2_name='arte')

    # Aeros
    so_aeros = compare.df1_unq_rows.copy()
    so_aeros = so_aeros.rename(columns={'valor': 'valor_aeros'})
    so_aeros.insert(0, 'descricao_erro','Só tem no aeros', True )
    so_aeros['valor_arte'] = None

    # Arte
    so_arte = compare.df2_unq_rows.copy()
    so_arte = so_arte.rename(columns={'valor': 'valor_arte'})
    so_arte.insert(0, 'descricao_erro','Só tem no arte', True )
    so_arte['valor_aeros'] = None

    # Valor diferente
    valor_diferente = compare.intersect_rows
    valor_diferente = valor_diferente[valor_diferente['valor_match']==False]
    valor_diferente.insert(0, 'descricao_erro','Valores diferentes', True )
    valor_diferente = valor_diferente.rename(columns={'valor_df1': 'valor_aeros','valor_df2': 'valor_arte' })
    valor_diferente = valor_diferente.drop(columns=['_merge','valor_match'])

    # resultado
    df = pd.concat([so_aeros, so_arte, valor_diferente])
    # valor_diferente.rename({'valor': 'valor_arte'})
    df.to_csv('resultado.csv', index=False, sep=';')



def get_ready_to_compare_aeros():
    df = pd.read_csv('aeros.csv', sep=';')

    df = df.drop(df.columns[3], axis=1)

    converte_verbas_aeros = {
        "1052": "1001",
        "1053": "1104",
        "1054": "1103",
        "1058": "1111",
        "1059": "1116",
        "1060": "1118",
        "1119": "1108",
        "1125": "1115",
        "1135": "1105",
        "1517": "1017",
    }

    df = df.replace({'verba': converte_verbas_aeros})

    return df


def get_ready_to_compare_arte():
    
    df = pd.read_csv('arte.csv')


    converte_verbas_arte = {
        '4023': '4003',
        '4024': '4003',
    }

    df = df.replace({'verba': converte_verbas_arte})

    return df

main()