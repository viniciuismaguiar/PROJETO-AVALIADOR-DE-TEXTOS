# feedback.py
# Gera comentários didáticos e sugestões com base no relatório do avaliador.

import re
from typing import Dict, List, Tuple
from nltk.tokenize import sent_tokenize, word_tokenize
try:
    # Prefer relative imports when used as a package
    from .avaliador import (
        AvaliadorDissertacao,
        AvaliadorConto,
        AvaliadorPoema,
        AvaliadorFabula
    )
except Exception:
    # Fallback for direct script execution
    from avaliador import (
        AvaliadorDissertacao,
        AvaliadorConto,
        AvaliadorPoema,
        AvaliadorFabula
    )

# -----------------------------------------------------
# Seleciona a classe de avaliação conforme o gênero
# -----------------------------------------------------
def selecionar_avaliador(genero: str):
    genero = genero.lower()
    if genero in ["dissertação", "dissertacao"]:
        return AvaliadorDissertacao()
    if genero == "conto":
        return AvaliadorConto()
    if genero == "poema":
        return AvaliadorPoema()
    if genero in ["fábula", "fabula"]:
        return AvaliadorFabula()
    return AvaliadorDissertacao()  # fallback seguro


# -----------------------------------------------------
# Stopwords → NÃO contam como repetição relevante
# -----------------------------------------------------
_STOPWORDS = {
    "o","a","os","as","de","do","da","dos","das","e","em","no","na","nos","nas",
    "um","uma","uns","umas","por","para","com","se","que","mais","como","quando",
    "entre","sob","sobre","sem","sua","suas","seu","seus"
}

def _filtrar_repeticoes(repeticoes: List[str]) -> List[str]:
    """Remove palavras curtas e stopwords da análise de repetição."""
    return [w for w in repeticoes if len(w) > 2 and w.lower() not in _STOPWORDS]


# -----------------------------------------------------
# FUNÇÃO PRINCIPAL DE FEEDBACK
# -----------------------------------------------------
def _detokenize(tokens: List[str]) -> str:
    # Reconstrói uma string a partir de tokens simples, ajustando espaçamento antes de
    # pontuação comum.
    s = " ".join(tokens)
    s = s.replace(' ,', ',').replace(' .', '.').replace(' ;', ';').replace(' :', ':')
    s = s.replace(" ( ", " (").replace(" ) ", ") ")
    s = s.replace(" ' ", "'")
    # corrige espaços antes de exclamações/interrogações
    s = s.replace(' !', '!').replace(' ?', '?')
    # remove espaços duplos
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _reescrever_frases_longas(texto: str, max_words: int = 35, max_suggestions: int = 3) -> List[str]:
    """Gera reescritas melhores para frases muito longas usando tokenização.

    Estratégia:
    - Tokeniza sentenças; para sentenças longas procura um ponto de divisão natural
      (vírgula, ponto-e-vírgula, conjunção) próximo ao centro.
    - Se não encontrar, divide no meio preservando capitalização e pontuação.
    - Produz até `max_suggestions` sugestões no total (não por sentença).
    """
    sugestões: List[str] = []
    try:
        sentencas = sent_tokenize(texto)
    except Exception:
        sentencas = [s.strip() for s in re.split(r"[\.\?!]", texto) if s.strip()]

    # tokens/pontuações preferidas para cortes
    punct_candidates = {',', ';', ':'}
    conj_candidates = {'e', 'mas', 'porém', 'contudo', 'quando', 'enquanto', 'porque', 'pois'}

    for s in sentencas:
        # simplificação: use word_tokenize para obter tokens (inclui pontuação)
        try:
            tokens = word_tokenize(s)
        except Exception:
            tokens = s.split()

        # contar palavras (tokens alfanuméricos)
        word_tokens = [t for t in tokens if re.search(r"\w", t)]
        if len(word_tokens) <= max_words:
            continue

        mid = len(tokens) // 2
        # procurar pontuação próxima ao meio
        split_idx = None
        window = range(max(0, mid - 12), min(len(tokens), mid + 12))
        # primeiro pontuações
        for i in window:
            if tokens[i] in punct_candidates:
                split_idx = i + 1
                break
        # depois conjunções
        if split_idx is None:
            for i in window:
                if tokens[i].lower() in conj_candidates:
                    split_idx = i + 1
                    break
        # fallback: dividir no meio
        if split_idx is None:
            split_idx = mid

        # construir partes preservando tokens
        left = tokens[:split_idx]
        right = tokens[split_idx:]

        left_text = _detokenize(left)
        right_text = _detokenize(right)

        # garantir pontuação final adequada
        if not re.search(r"[\.\?!]$", left_text):
            left_text = left_text.rstrip(',;:') + '.'
        if right_text and not re.search(r"[\.\?!]$", right_text):
            right_text = right_text[0].upper() + right_text[1:]
            if not re.search(r"[\.\?!]$", right_text):
                right_text = right_text.rstrip(',;:') + '.'

        sugestao = f"Sugestão de reescrita: {left_text} {right_text}" if right_text else f"Sugestão de reescrita: {left_text}"
        sugestões.append(sugestao)

        # limite total de sugestões
        if len(sugestões) >= max_suggestions:
            break

    return sugestões


def pontuar_e_gerar_feedback(rel: Dict, tema: str = "", texto: str = None) -> Dict:

    repeticoes_raw = rel.get("repeticoes_relevantes", [])
    repeticoes = _filtrar_repeticoes(repeticoes_raw)

    frases_muito_longas = rel.get("frases_muito_longas", [])
    paragrafos_extensos = rel.get("paragrafos_extensos", [])
    variedade_vocab = rel.get("variedade_vocabulario", 0)
    adequacao_tema = 0  # default

    total_paragrafos = len(rel.get("paragrafos", []))
    total_palavras = rel.get("num_palavras", 0)
    tamanho_frase = rel.get("media_palavras_por_frase", 0)

    genero = rel.get("genero", "dissertação")
    avaliador = selecionar_avaliador(genero)
    notas_genero = avaliador.avaliar(rel)

    comentarios: List[str] = []
    sugestoes: List[str] = []
    contexto_genero: List[str] = []
    sugestoes_por_genero: List[str] = []
    detalhe = {}

    # =====================================================
    # 1) Estrutura
    # =====================================================
    estrutura = 2
    if total_paragrafos <= 1:
        estrutura = 0
        comentarios.append("Estrutura: O texto está muito compacto; organize-o melhor em parágrafos.")
    elif total_paragrafos == 2:
        estrutura = 1
        comentarios.append("Estrutura: Boa tentativa, mas os parágrafos ainda podem ser divididos melhor.")
    else:
        comentarios.append("Estrutura: Boa organização em parágrafos.")

    if paragrafos_extensos:
        comentarios.append(f"Estrutura: Existem {len(paragrafos_extensos)} parágrafos muito longos.")
        sugestoes.append("Divida os parágrafos mais extensos para facilitar a leitura.")

    # Gera comentários iniciais por gênero (contextualização educativa)
    genero_lower = genero.lower()
    if genero_lower in ["dissertação", "dissertacao"]:
        contexto_genero.append("Dissertação: foque em tese clara, argumentos e conclusão coerente.")
        sugestoes_por_genero.append("Garanta uma tese assertiva e use conectores para ligar argumentos.")
    elif genero_lower == "conto":
        contexto_genero.append("Conto: priorize enredo, sequência de eventos e um desfecho marcante.")
        sugestoes_por_genero.append("Trabalhe a construção de cena e personagens; elimine descrições supérfluas.")
    elif genero_lower == "poema":
        contexto_genero.append("Poema: atenção à concisão, ritmo e imagens poéticas.")
        sugestoes_por_genero.append("Varie os versos e utilize imagens e metáforas para enriquecer as estrofes.")
    elif genero_lower in ["fábula", "fabula"]:
        contexto_genero.append("Fábula: destaque a ação dos personagens animais e deixe a moral explícita.")
        sugestoes_por_genero.append("Reforce a moral no final e simplifique a narrativa para maior impacto.")
    else:
        contexto_genero.append(f"Gênero detectado: {genero}. Ajuste o texto conforme os critérios gerais.")

    # =====================================================
    # 2) Coesão
    # =====================================================
    coesao = 2
    if tamanho_frase > 36:
        coesao = 0
        comentarios.append("Coesão: Muitas frases longas; períodos extensos prejudicam a ligação entre ideias.")
    elif tamanho_frase > 26:
        coesao = 1
        comentarios.append("Coesão: Algumas frases longas; é possível melhorar conectores e pontuação.")
    else:
        comentarios.append("Coesão: Boa fluidez entre as frases.")

    # =====================================================
    # 3) Clareza
    # =====================================================
    clareza = 2
    if total_palavras < 80:
        clareza = 0
        comentarios.append("Clareza: O texto está muito curto; falta desenvolvimento das ideias.")

    if repeticoes:
        clareza = max(0, clareza - 1)
        comentarios.append("Clareza: Há repetição de palavras; varie seu vocabulário.")
        sugestoes.append(f"Varie palavras repetidas, como '{repeticoes[0]}', utilizando sinônimos adequados.")

    if frases_muito_longas:
        clareza = max(0, clareza - 1)
        comentarios.append("Clareza: Algumas frases muito longas dificultam a compreensão.")
        sugestoes.append("Divida frases longas em períodos menores para facilitar a leitura.")

    # =====================================================
    # 4) Vocabulário
    # =====================================================
    vocab = 2
    if variedade_vocab < 30:
        vocab = 0
        comentarios.append("Vocabulário: Pouca variedade; procure diversificar o uso de palavras.")
    elif variedade_vocab < 45:
        vocab = 1
        comentarios.append("Vocabulário: Variedade moderada; pode-se ampliar o repertório lexical.")
    else:
        comentarios.append("Vocabulário: Muito bom repertório lexical.")

    # Adiciona sugestões específicas por gênero quando aplicável
    if sugestoes_por_genero:
        sugestoes.extend(sugestoes_por_genero)

    # =====================================================
    # 5) Adequação ao tema
    # =====================================================
    adequacao = 2
    if tema:
        # Heurística melhor: checar presença das palavras do tema no conjunto de palavras do texto
        palavras_tema = [w for w in re.findall(r"\w+", tema.lower())]
        palavras_texto = set(rel.get("palavras_minusculas", []))
        matches = sum(1 for w in palavras_tema if w in palavras_texto)
        if matches == 0:
            adequacao = 0
            comentarios.append("Adequação ao tema: Pouca relação com o tema informado.")
        elif matches < max(1, len(palavras_tema)//2):
            adequacao = 1
            comentarios.append("Adequação ao tema: Relação parcial com o tema; pode aprofundar o foco.")
        else:
            comentarios.append("Adequação ao tema: Boa relação com o tema.")
    else:
        comentarios.append("Adequação ao tema: Tema não informado; avaliação feita apenas pelo texto.")

    # =====================================================
    # NOTA FINAL
    # =====================================================
    total_pontos = estrutura + coesao + clareza + vocab + adequacao
    nota_final = round(total_pontos, 2)

    detalhe.update({
        "estrutura": estrutura,
        "coesao": coesao,
        "clareza": clareza,
        "vocabulario": vocab,
        "adequacao": adequacao
    })

    # exemplo de reescrita
    exemplo_reescrita = []
    if frases_muito_longas:
        exemplo_reescrita.append("Exemplo: transforme uma frase longa em duas mais curtas.")

    # Exemplos adicionais por gênero
    if genero_lower == "poema":
        exemplo_reescrita.append("Exemplo (poema): substitua descrições literais por imagens sensoriais e varie o comprimento dos versos.")
    if genero_lower in ["fábula", "fabula"]:
        exemplo_reescrita.append("Exemplo (fábula): torne a moral mais explícita na última frase.")
    if genero_lower == "conto":
        exemplo_reescrita.append("Exemplo (conto): acrescente um detalhe de personagem que explique a motivação do conflito.")

    # Auto-reescrita: gera exemplos automáticos a partir do texto (se fornecido)
    texto_base = texto if texto is not None else "\n".join(rel.get("linhas", []))
    exemplo_reescrita_auto = _reescrever_frases_longas(texto_base)

    # Não alteramos a ordem de 'comentarios' original; expomos contexto de gênero separadamente

    return {
        "nota_final": nota_final,
        "pontos": total_pontos,
        "detalhe": detalhe,
        "comentarios": comentarios,
        "sugestoes": sugestoes,
        "exemplo_reescrita": exemplo_reescrita,
        # campos adicionais (estruturados)
        "comentarios_gerais": comentarios,
        "comentarios_por_genero": contexto_genero,
        "sugestoes_gerais": sugestoes,
        "sugestoes_por_genero": sugestoes_por_genero,
        "exemplo_reescrita_auto": exemplo_reescrita_auto,
        "_texto_base": texto_base
    }
