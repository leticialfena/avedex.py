# AveDex

Catálogo interativo de aves desenvolvido na disciplina de Boas Práticas de Programação do curso de Análise e Desenvolvimento de Sistemas.

## Funcionalidades

- Listagem e paginação das aves cadastradas;
- Busca textual sem diferenciar acentos ou letras maiúsculas e minúsculas;
- Busca por nome popular, nome científico, família, ordem ou dieta;
- Exibição dos detalhes de uma ave por ID;
- Seleção de aves por ID;
- Sorteio de uma ave aleatória;
- Comparação entre duas aves;
- Batalha AveDex por atributos numéricos;
- Download e cache local de imagens e sons;
- Tentativa de exibição de imagens no terminal;
- Reprodução de sons;
- Validação defensiva do dataset;
- Tratamento de erros no carregamento do JSON;
- Verificação das dependências do ambiente;
- Créditos e fontes dos dados.

## Como executar

O ponto de entrada da aplicação é o arquivo `main.py`.

```bash
python main.py
```

## Instalação das dependências

As dependências opcionais estão listadas em requirements.txt.

Para instalar:

```bash
pip install -r requirements.txt
```

Os recursos principais da AveDex funcionam sem as bibliotecas opcionais.

Os recursos de imagem, som e download dependem das bibliotecas disponíveis em requirements.txt.


```markdown
## Catálogo

O dataset atualmente possui 11 aves cadastradas:

- Bem-te-vi
- João-de-barro
- Canário-da-terra
- Sabiá-laranjeira
- Tucano-toco
- Arara-azul
- Coruja-buraqueira
- Beija-flor-tesoura
- Garça-branca-grande
- Quero-quero
- Pica-pau-do-campo

Os dados das aves são armazenados no arquivo JSON localizado em:

```text
data/aves.json
```

```markdown
## Estrutura do projeto

```text
avedex/
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── aves.json
├── src/
│   └── avedex/
│       ├── __init__.py
│       ├── ambiente.py
│       ├── app.py
│       ├── batalha.py
│       ├── catalogo.py
│       ├── comparacao.py
│       ├── creditos.py
│       ├── dados.py
│       ├── interface.py
│       ├── multimidia.py
│       └── utils.py
├── cache_midias/
└── docs/
    └── testes_manuais.md
```

```markdown
## Principais módulos

- `main.py`: ponto de entrada da aplicação;
- `src/avedex/app.py`: fluxo principal e controle do menu;
- `src/avedex/interface.py`: abertura e menu principal;
- `src/avedex/catalogo.py`: listagem, paginação, busca, detalhes e ave aleatória;
- `src/avedex/comparacao.py`: comparação entre duas aves;
- `src/avedex/batalha.py`: batalha entre aves por atributos;
- `src/avedex/multimidia.py`: download, cache, imagens e sons;
- `src/avedex/dados.py`: carregamento e validação do dataset;
- `src/avedex/ambiente.py`: verificação das dependências;
- `src/avedex/creditos.py`: créditos e fontes;
- `src/avedex/utils.py`: funções auxiliares utilizadas pelos demais módulos.

## Validação e tratamento de erros

O sistema realiza validações defensivas durante o carregamento do dataset.

Entre as verificações realizadas estão:

- arquivo JSON inexistente;
- JSON mal formatado;
- campos obrigatórios ausentes;
- IDs duplicados;
- campos numéricos inválidos;
- valores ausentes;
- entrada inválida para seleção de aves;
- opção inválida no menu.

Caso existam problemas no dataset, o programa informa os problemas encontrados sem encerrar de forma inesperada.

## Recursos de multimídia

A AveDex possui suporte opcional para imagens e sons.

As mídias são baixadas quando necessário e armazenadas localmente no diretório:

```text
cache_midias/
```
Assim, uma mídia que já foi baixada pode ser reutilizada sem realizar o download novamente.

O sistema também trata situações como:

URL de imagem ausente;
URL de som ausente;
falha no download;
biblioteca opcional não instalada;
terminal sem suporte para exibição da imagem;
falha na reprodução do som.

Os recursos opcionais não impedem o funcionamento do catálogo principal.

```markdown
## Comparação entre aves

O sistema permite selecionar duas aves e comparar:

- Nome científico;
- Família;
- Ordem;
- Tipo de dieta;
- Habitat;
- Comprimento;
- Peso;
- Status de conservação.

Ao final da comparação, o sistema informa qual das aves possui maior peso.

## Batalha AveDex

A Batalha AveDex permite selecionar duas aves e escolher um atributo numérico para determinar a vencedora.

Os atributos disponíveis são:

- Comprimento;
- Peso médio;
- Índice de conservação.

A mesma ave não pode ser selecionada para os dois lados da batalha.

## Exemplos de buscas

| Busca | Resultado esperado |
|---|---|
| `barro` | João-de-barro |
| `canario` | Canário-da-terra |
| `tyrannidae` | Bem-te-vi |
| `passeriformes` | Aves da ordem Passeriformes |
| `granivora` | Canário-da-terra e Arara-azul |
| `trochilidae` | Beija-flor-tesoura |
| `ardeidae` | Garça-branca-grande |

A busca não diferencia letras maiúsculas de minúsculas e remove diferenças de acentuação.

## Verificação do ambiente

A opção **Verificar ambiente** informa a disponibilidade das bibliotecas utilizadas pelos recursos opcionais da aplicação.

Entre as dependências verificadas estão:

- `requests`;
- `pygame`;
- `term_image`.

O núcleo da aplicação continua funcionando mesmo quando alguma dessas bibliotecas não está disponível.

## Testes manuais

Os testes manuais da aplicação estão documentados em:

```text
docs/testes_manuais.md

Entre os cenários considerados estão:

abertura do programa;
carregamento e validação do dataset;
listagem e paginação;
busca;
detalhes das aves;
comparação;
ave aleatória;
Batalha AveDex;
imagens;
sons;
cache de mídias;
tratamento de URLs ausentes;
tratamento de dependências ausentes;
verificação do ambiente;
créditos;
encerramento do programa.

```markdown
## Fontes dos dados

As principais fontes utilizadas no projeto são:

- WikiAves: https://www.wikiaves.com.br/
- IUCN Red List: https://www.iucnredlist.org/
- Wikimedia Commons: https://commons.wikimedia.org/
- Guia de Aves Funed: https://www.funed.mg.gov.br/

As fontes também estão registradas no próprio dataset em `data/aves.json`.

## Tecnologias utilizadas

- Python 3;
- JSON;
- `unicodedata`;
- `requests`;
- `pygame`;
- `term_image`;
- Git e GitHub.

## Objetivo do projeto

A AveDex foi desenvolvida como projeto acadêmico para praticar boas práticas de programação, incluindo:

- separação de responsabilidades;
- organização em módulos;
- reutilização de funções;
- validação defensiva;
- tratamento de erros;
- uso de arquivos JSON;
- dependências opcionais;
- cache local;
- documentação;
- testes manuais;
- controle de versões com Git.
## Autor
Letícia Alfena Cunha

