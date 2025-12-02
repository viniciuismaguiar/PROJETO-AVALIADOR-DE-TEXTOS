# Avaliador de Textos — Modo Educacional

Um programa interativo para avaliar textos em português (dissertação, conto, poema, fábula) com feedback automático, métricas detalhadas e sugestões de reescrita.

---

## Requisitos do Sistema

- **Python 3.8+** (testado em Python 3.14)
- **Windows, macOS ou Linux**
- **pip** (gerenciador de pacotes Python)
- ~10 MB de espaço em disco

---

## Instalação

### 1. Instalar e configurar o Git no terminal

Antes de baixar o projeto, é necessário instalar o Git.

* Baixe e instale o Git:
  [https://git-scm.com/downloads](https://git-scm.com/downloads)

Após a instalação, verifique se o Git está funcionando no terminal:

```bash
git --version
```

Se uma versão for exibida, o Git está configurado corretamente.

---

### 2. Clonar ou baixar o projeto

```bash
git clone https://github.com/SEU-USUARIO/PROJETO-AVALIADOR-DE-TEXTOS.git
cd PROJETO-AVALIADOR-DE-TEXTOS
```

---

### 3. (Recomendado) Criar um ambiente virtual

```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

---

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 5. Baixar recursos NLTK (necessário apenas uma vez)

```bash
python -c "import nltk; nltk.download('punkt')"
```

Ou de forma interativa:

```python
python
>>> import nltk
>>> nltk.download('punkt')
>>> exit()
```

---

### 6. Executar o projeto

```bash
python main.py
```

*(Substitua `main.py` caso o arquivo principal tenha outro nome.)*

---

## Como Executar

### Iniciar o programa interativo

```bash
python main.py
```

ou alternativamente:

```bash
python -m data.main
```

### Menu de opções

Ao iniciar, você verá:

```
=== Avaliador de Textos — Modo Educacional ===
1 - Digitar o texto no terminal
2 - Avaliar um arquivo .txt
3 - Ajuda sobre critérios
4 - Sair
Escolha:
```

---

## Como Usar

### Opção 1: Digitar o texto no terminal

1. Escolha a opção `1` no menu
2. (Opcional) Informe um tema para a atividade
3. (Opcional) Indique o gênero textual (dissertação, conto, poema, fábula)
   - Se deixar em branco, o sistema tenta detectar automaticamente
   - Se não conseguir identificar, **você será forçado a escolher**
4. Cole ou digite o texto
5. Termine com uma linha contendo apenas `FIM` e pressione Enter

**Exemplo:**
```
Informe o tema da atividade (ou deixe vazio): Imaginação infantil

Opcional: indique o gênero textual a ser avaliado para sobrescrever a detecção automática.
Gêneros possíveis: dissertação, conto, poema, fábula
Informe o gênero (ou deixe vazio para detecção automática): 

Digite (ou cole) o texto. Para encerrar, digite uma linha com apenas 'FIM' e pressione Enter.
O menino encontrou uma chave dourada...
[... mais linhas ...]
FIM

===== RELATÓRIO COMPLETO =====
[Resultado da avaliação será exibido aqui]
```

### Opção 2: Avaliar um arquivo .txt

1. Escolha a opção `2` no menu
2. Informe o caminho do arquivo (ex: `C:\Users\vinic\Documents\meu_texto.txt`)
3. Siga o mesmo processo da opção 1

**Exemplo:**
```
Caminho do arquivo .txt: ./meu_texto.txt
```

### Opção 3: Ajuda sobre critérios

Exibe explicações dos critérios de avaliação:
- **Estrutura:** organização em parágrafos
- **Coesão:** conexão lógica entre frases
- **Clareza:** objetividade e fluidez
- **Vocabulário:** diversidade e adequação
- **Adequação ao tema:** relação com o tema informado

---

## Detecção Automática de Gênero

O programa detecta automaticamente o gênero baseado em marcadores textuais:

| Gênero | Marcadores | Exemplo |
|--------|-----------|---------|
| **Poema** | Múltiplas linhas curtas (≤8 palavras) | Versos com até 8 palavras por linha |
| **Carta** | Saudação + fechamento formal | "Querido...", "Atenciosamente" |
| **Fábula** | Animais + moral ou animal como agente | "A raposa disse:", "Moral: ..." |
| **Conto** | Marcadores narrativos | "Era uma vez", "Certa vez" |
| **Crônica** | Referências ao cotidiano | "Outro dia", "No ônibus" |
| **Artigo de opinião** | Marcadores de opinião | "Na minha opinião", "Defendo que" |
| **Dissertação** | 2+ marcadores argumentativos | "Portanto", "Logo", "Assim", "Contudo" |
| **Desconhecido** | Nenhum dos anteriores | Você será solicitado a escolher |

---

## O que o programa avalia

### Métricas automáticas

- Número de palavras e frases
- Média de palavras por frase
- Variedade e diversidade de vocabulário
- Parágrafos detectados
- Palavras mais frequentes
- Repetições relevantes

### Nota final

Escala de **0 a 10** baseada em:
- Estrutura (0-2 pontos)
- Coesão (0-2 pontos)
- Clareza (0-2 pontos)
- Vocabulário (0-2 pontos)
- Adequação ao tema (0-2 pontos)

### Feedback didático

- Comentários por critério
- Sugestões de melhoria específicas
- Exemplos de reescrita automática

---

## Salvar relatório

Após a avaliação, o programa pergunta se você deseja salvar o relatório em `.txt`:

```
Deseja salvar o relatório em .txt? (s/n): s
Nome do arquivo (ex: relatorio1.txt): meu_relatorio.txt
Relatório salvo em: meu_relatorio.txt
```

O arquivo será criado no diretório de execução.

---

## Estrutura do projeto

```
projeto-avaliacao_textos/
├── data/
│   ├── __init__.py              # Inicialização do pacote
│   ├── avaliador.py             # Detector de gênero + análise textual
│   ├── feedback.py              # Gerador de feedback + reescrita
│   └── main.py                  # Interface interativa (CLI)
├── main.py                      # Runner do projeto (executável)
├── requirements.txt             # Dependências Python
└── README.md                    # Este arquivo
```

---

## Dependências

- **nltk** — Processamento de linguagem natural (tokenização de frases e palavras)

Instaladas automaticamente com `pip install -r requirements.txt`.

---

## Solução de problemas

### Erro: "No module named 'nltk'"

**Solução:** Instale as dependências novamente:
```bash
pip install -r requirements.txt
```

### Erro: "LookupError: punkt"

**Solução:** Baixe o recurso `punkt` do NLTK:
```python
python -c "import nltk; nltk.download('punkt')"
```

### Caracteres acentuados aparecem como "??"

**Solução (Windows):** Configure o PowerShell para UTF-8:
```powershell
$env:PYTHONIOENCODING = "utf-8"
```

Ou execute diretamente no Windows Terminal (que suporta UTF-8 nativamente).

### O programa não detecta meu texto corretamente

- Verifique se você forneceu um tema relacionado
- Tente informar o gênero manualmente (em vez de deixar automático)
- O sistema usa heurísticas baseadas em marcadores textuais; não é 100% preciso

---

## Exemplos de uso

### Exemplo 1: Avaliar uma dissertação

```
Informe o tema: Impacto das redes sociais
Gênero: dissertação
Texto:
As redes sociais transformaram a comunicação moderna. Portanto, é necessário compreender seus impactos. Logo, devemos analisa-los criticamente. Assim, a sociedade avança na regulamentação.
FIM

→ Resultado: Dissertação detectada automaticamente, nota = 7/10
```

### Exemplo 2: Avaliar um conto com tema

```
Informe o tema: Aventura infantil
Gênero: (deixar vazio)
Texto:
Era uma vez um menino que encontrou uma chave misteriosa. Curioso, procurou a porta que ela abria. Depois de explorar a casa, descobriu um mundo mágico.
FIM

→ Resultado: Conto detectado, nota = 8/10
```

### Exemplo 3: Avaliar um arquivo

```
Opção: 2
Arquivo: ./poesia.txt
Gênero: (deixar vazio)

→ Resultado: Poema detectado (versos curtos), nota = 6/10
```

---

## Suporte

Para dúvidas ou melhorias, consulte o código-fonte em `data/`.

**Bom uso!**
