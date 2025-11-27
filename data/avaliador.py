# avaliador.py
import re
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize

# ===========================
# DETECTOR DE GÊNERO TEXTUAL
# ===========================
class DetectorGenero:
    def detectar(self, texto):
        # Normaliza entrada
        texto_stripped = texto.strip()
        t = texto_stripped.lower()

        # linhas não vazias (versos ou parágrafos)
        linhas = [l.strip() for l in texto_stripped.splitlines() if l.strip()]

        # --- POEMA ---
        # Se houver múltiplas linhas e a maioria for curta (poucas palavras), é provável poema.
        if len(linhas) >= 2:
            curto = sum(1 for l in linhas if len(l.split()) <= 8)
            if curto / len(linhas) >= 0.6 and not re.search(r"\bcap(í|i)tulo\b", t):
                return "poema"

        # --- CARTA ---
        # Procura saudações típicas no início e fechamentos formais no texto
        abertura = re.match(r"^(querido|querida|prezado|prezada|caro|cara)\b", t)
        fechamento = re.search(r"(atenciosamente|cordialmente|cumprimentos|grato|grata)\b", t)
        if abertura and fechamento:
            return "carta"

        # --- FÁBULA ---
        animais_fabula = [
            "leão", "raposa", "lobo", "corvo", "tartaruga", "lebre", "cervo",
            "gato", "cachorro", "rato", "coelho", "água-viva"
        ]
        marcadores_moral = ["moral:", "moraleja", "lição", "ensinamento", "ensinamento moral"]

        # Fábula: presença de animais + indicador de moral OR animal como agente (fala/ação humana)
        has_animal = any(animal in t for animal in animais_fabula)
        has_moral_marker = any(moral in t for moral in marcadores_moral)
        # procura padrões do tipo 'o cachorro disse' ou 'a raposa falou' (indicando animal personificado)
        animais_regex = r"\b(?:" + "|".join(re.escape(a) for a in animais_fabula) + r")\b"
        agente_padrao = re.compile(animais_regex + r"(?:\s+(?:\w+)){0,5}\s+(?:disse|falou|falavam|falou|diz|dizia|pensou|pensaram)\b", re.I)
        animal_agente = bool(agente_padrao.search(t))
        if has_animal and (has_moral_marker or animal_agente):
            return "fábula"

        # --- CONTO ---
        marcadores_conto = ["era uma vez", "certa vez", "numa noite", "um dia", "anos depois"]
        # Conto costuma trazer marcadores narrativos e ser mais extenso que microconto
        if any(p in t for p in marcadores_conto) or ("quando" in t and "disse" in t):
            # evita confundir com fábula (já tratada acima)
            return "conto"

        # --- CRÔNICA ---
        marcadores_cronica = ["outro dia", "no ônibus", "no mercado", "cotidiano", "manhã seguinte"]
        if any(m in t for m in marcadores_cronica):
            return "crônica"

        # NOTE: detecção de 'resumo' foi removida para evitar falsos positivos.

        # --- ARTIGO DE OPINIÃO ---
        marcadores_artigo = ["na minha opinião", "defendo que", "acredito que"]
        if any(p in t for p in marcadores_artigo):
            return "artigo de opinião"

        # --- DISSERTAÇÃO ARGUMENTATIVA ---
        # Exigir 2+ marcadores argumentativos para classificar como dissertação (regra mais rígida)
        marcadores_argumento = ["portanto", "logo", "assim", "contudo", "entretanto", "tese", "dessa forma"]
        marcadores_narrativos = ["era uma vez", "falou", "caminhou", "história", "personagem"]
        contagem_argumentos = sum(1 for m in marcadores_argumento if m in t)
        if contagem_argumentos >= 2 and not any(narr in t for narr in marcadores_narrativos):
            return "dissertação"

        # Default: retornar "desconhecido" para forçar que o usuário escolha o gênero
        return "desconhecido"


# ===========================
# ANALISADOR BÁSICO
# ===========================
class AnalisadorBasico:
    def analisar(self, texto: str) -> dict:
        texto_limpo = texto.strip()
        frases = sent_tokenize(texto)
        palavras = word_tokenize(texto)

        numero_frases = len(frases)
        numero_palavras = len(palavras)
        media_palavras_por_frase = numero_palavras / numero_frases if numero_frases > 0 else 0

        palavras_minusculas = [p.lower() for p in palavras if p.isalpha()]
        vocabulario_unico = len(set(palavras_minusculas))
        variedade_vocabulario_pct = (vocabulario_unico / len(palavras_minusculas) * 100) if palavras_minusculas else 0

        # Parágrafos: blocos não vazios separados por linha em branco
        raw_pars = [b.strip() for b in re.split(r"\n\s*\n", texto) if b.strip()]
        paragrafos = raw_pars   
        paragrafos_extensos = [p for p in paragrafos if len(p.split()) > 120]

        # Frases muito longas
        frases_muito_longas = [f for f in frases if len(f.split()) > 35]

        # Palavras mais frequentes
        contador = Counter(palavras_minusculas)
        mais_frequentes = contador.most_common(10)

        # Repetições relevantes
        repeticoes_relevantes = [w for w,c in contador.items() if c > 2]

        return {
            "num_frases": numero_frases,
            "num_palavras": numero_palavras,
            "media_palavras_por_frase": round(media_palavras_por_frase,2),
            "variedade_vocabulario": round(variedade_vocabulario_pct,2),
            "vocabulario_unico": vocabulario_unico,
            "paragrafos_extensos": paragrafos_extensos,
            "paragrafos": paragrafos,
            "palavras_minusculas": palavras_minusculas,
            "frases_muito_longas": frases_muito_longas,
            "linhas": texto.split("\n"),
            "mais_frequentes": mais_frequentes,
            "repeticoes_relevantes": repeticoes_relevantes,
        }


# ===========================
# AVALIADORES ESPECÍFICOS
# ===========================
class AvaliadorDissertacao:
    def avaliar(self, rel: dict) -> dict:
        notas = {"Estrutura":2, "Coesão":2, "Clareza":2}

        if rel["media_palavras_por_frase"] > 25:
            notas["Clareza"] -= 1
        if len(rel["paragrafos_extensos"]) > 0:
            notas["Estrutura"] -= 1
        if rel["variedade_vocabulario"] < 25:
            notas["Coesão"] -= 1

        return notas

class AvaliadorConto:
    def avaliar(self, rel: dict) -> dict:
        notas = {"Criatividade":2, "Coesão":2}
        if rel["num_frases"] < 5:
            notas["Coesão"] -= 1
        if rel["vocabulario_unico"] < 50:
            notas["Criatividade"] -= 1
        return notas

class AvaliadorPoema:
    def avaliar(self, rel: dict) -> dict:
        notas = {"Musicalidade":2, "Imagem poética":2}
        linhas = rel["linhas"]
        versos_longos = [l for l in linhas if len(l.split()) > 10]
        if len(versos_longos) > len(linhas)*0.4:
            notas["Musicalidade"] -= 1
        if rel["variedade_vocabulario"] < 20:
            notas["Imagem poética"] -= 1
        return notas

class AvaliadorFabula:
    def avaliar(self, rel: dict) -> dict:
        notas = {"Moralidade":2, "Narrativa":2}
        if rel["num_frases"] < 4:
            notas["Narrativa"] -= 1
        if rel["variedade_vocabulario"] < 20:
            notas["Moralidade"] -= 1
        return notas


# ===========================
# AVALIADOR PRINCIPAL
# ===========================
class AvaliadorTexto:
    def __init__(self):
        self.detect = DetectorGenero()
        self.analisador = AnalisadorBasico()
        self.avaliadores = {
            "dissertação": AvaliadorDissertacao(),
            "conto": AvaliadorConto(),
            "poema": AvaliadorPoema(),
            "fábula": AvaliadorFabula()
        }

    def avaliar_texto(self, texto: str) -> dict:
        genero = self.detect.detectar(texto)
        relatorio = self.analisador.analisar(texto)
        avaliador = self.avaliadores.get(genero, AvaliadorDissertacao())
        notas = avaliador.avaliar(relatorio)

        relatorio.update({
            "genero": genero,
            "avaliacao": notas
        })
        return relatorio

# Compatibilidade com main.py
from typing import Optional
def analisar_texto(texto: str, tema: Optional[str] = "") -> dict:
    avaliador = AvaliadorTexto()
    rel = avaliador.avaliar_texto(texto)
    rel["tema"] = tema
    return rel
