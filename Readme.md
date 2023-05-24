# Comparação verbas Arte x Aeros
Compara as verbas entre os sistemas Arte e Aeros, considerando grupos de verba, ou seja, abarca a possibilidade de que um determinado valor seja pago em uma verba X em um dos sistemas, e na verba Y em outro.

Caso duas verbas pertençam ao mesmo grupo, a soma delas será comparada. Se o total for igual, as duas serão consideradas iguais, mesmo que o valor individualmente seja diferente.

# Como executar

## A primeira vez
### Crie seu ambiente virtual
```
python -m venv venv
```
### Ative esse ambiente criado no passo anterior.

Para windows:
```
.\venv\Scripts\activate
```

Em Linux e Mac:
```
source venv/bin/activate
```
### Instale os pacotes necessários
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
## Da segunda vez em diante
Ative o ambiente virtual.

Para windows:
```
.\venv\Scripts\activate
```

Em Linux e Mac:
```
source venv/bin/activate
```

## Configure os grupos
O arquivo `groups.csv` contém os grupos de verbas. A primeira coluna representa o nome do grupo ao qual uma verba pertence, e a segunda coluna é o código da verba. Caso a verba não apareça na lista, ela será considerada como sem grupo, e será comparada individualmente.

## Gere arquivos CSV de cada um dos sistemas

### Arte
Entre no Arte, vá em Módulos -> Informações Gerenciais -> Extração de Informações, depois em Utilitários -> Comando SQL e clique em cancelar.
Execute o seguinte SQL, lembrando de alterar a data (marcada como [data], deve ser no formato DD/MM/AAAA).
```sql
SELECT
	codigo_contrato as cm,
	codigo_verba as verba,
	replace(sum(valor_verba), ',', '.') as valor
FROM RHMOVI_MOVIMENTO

WHERE
	TIPO_MOVIMENTO = 'ME' AND
	ANO_MES_REFERENCIA = TO_DATE([data], 'DD/MM/YYYY') AND
    valor_verba > 0
GROUP BY codigo_contrato , codigo_verba ;
```
Depois de executar, salve como arquivo como `CSV with headers` com um nome qualquer e no diretório que desejar.

### Aeros
Entre no Aeros e vá em Ferramentas -> Consultar Dados. Feche a janela `Usuário` e execute o seguinte SQL, lembrando de alterar o mês e o ano (marcados com [mês] e [ano]).
```sql
SELECT
	vw_calculos_folha.matricula_numero as cm,
	CASE
	    WHEN fpc037.fpc037_integracao is null
            THEN cast(vw_calculos_folha.fpc037_numero as varchar)
		ELSE fpc037.fpc037_integracao
	END AS verba,
    sum(vw_calculos_folha.fpm005_valor) as valor
FROM vw_calculos_folha
    JOIN fpc037 ON vw_calculos_folha.fpc037_cod =  fpc037.fpc037_cod
WHERE
    fpc036_ano = [ano] and
    fpc036_mes = [mês] and
    vw_calculos_folha.fpm005_valor > 0 and
    fpc036_tipo in (0,4, 7)

GROUP BY vw_calculos_folha.matricula_numero, verba;
```
Depois de executar, salve como arquivo csv com um nome qualquer e no diretório que desejar.

## Comparar

Para gerar a comparação você vai precisar:
- Nome do arquivo csv gerado no Arte
- Nome do arquivo csv gerado no Aeros
- Onde salvar o resultado da comparação

Então execute:
```
python main.py <diretorio_csv_arte> <diretorio_csv_aeros> <diretorio_salvar>
```
Por exemplo, se os arquivos CSV do Arte e do Aeros estiverem dentro da pasta do código, basta executar:
```
python main.py arte.csv aeros.csv resultado.csv
```
Se desejar executar o código com os arquivos CSV em outro diretório, obtenha a localização desses arquivos e execute algo como:
```
python main.py '\\cmbhfs.cmbh.mg.gov.br\rh\DIVPESCOMUM\Comparação folhas\arte.csv' '\\cmbhfs.cmbh.mg.gov.br\rh\DIVPESCOMUM\Comparação folhas\aeros.csv' '\\cmbhfs.cmbh.mg.gov.br\rh\DIVPESCOMUM\Comparação folhas\resultado.csv'
```
A planilha CSV com o resultado da comparação será salvo no diretório informado.
