# main.py
# Interface principal: menu, leitura, execução do avaliador e geração de relatório em arquivo.

try:
    # Prefer relative imports when used as a package
    from .avaliador import analisar_texto
    from .feedback import pontuar_e_gerar_feedback
except Exception:
    # Fallback for direct script execution (keeps backwards compatibility)
    from avaliador import analisar_texto
    from feedback import pontuar_e_gerar_feedback
import datetime
import os

def mostrar_menu():
    print("\n=== Avaliador de Textos — Modo Educacional ===")
    print("1 - Digitar o texto no terminal")
    print("2 - Avaliar um arquivo .txt")
    print("3 - Ajuda sobre critérios")
    print("4 - Sair")
    escolha = input("Escolha: ").strip()
    return escolha

def ler_texto_terminal():
    print("\nDigite (ou cole) o texto. Para encerrar, digite uma linha com apenas 'FIM' e pressione Enter.")
    linhas = []
    while True:
        try:
            l = input()
        except EOFError:
            break
        if l.strip().upper() == "FIM":
            break
        linhas.append(l)
    return "\n".join(linhas)

def ler_arquivo_txt(caminho: str):
    if not os.path.isfile(caminho):
        print("Arquivo não encontrado.")
        return None
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return None

def imprimir_relatorio_completo(texto: str, tema: str, rel, fb):
    print("\n===== RELATÓRIO COMPLETO =====\n")
    print(f"Tema informado: {tema}\n")
    print(f"Nota final: {fb['nota_final']}/10  (Pontos totais: {fb['pontos']}/10)\n")
    print(f"Gênero detectado: {rel.get('genero', 'desconhecido').capitalize()}\n")

    print("Detalhes por critério (0-2):")
    for k, v in fb['detalhe'].items():
        print(f" - {k.capitalize()}: {v}/2")

    print("\nComentários:")
    if fb['comentarios']:
        for c in fb['comentarios']:
            print(" *", c)
    else:
        print("Nenhum comentário específico.")

    print("\nSugestões de reescrita:")
    if fb['sugestoes']:
        for s in fb['sugestoes']:
            print(" -", s)
    else:
        print("Nenhuma sugestão específica.")

    if fb['exemplo_reescrita']:
        print("\nExemplos rápidos de reescrita:")
        for e in fb['exemplo_reescrita']:
            print(" >", e)

    print("\nResumo das métricas:")
    # Principais métricas numéricas
    print(f" - Número de palavras: {rel.get('num_palavras', 0)}")
    print(f" - Número de frases: {rel.get('num_frases', 0)}")
    print(f" - Média de palavras por frase: {rel.get('media_palavras_por_frase', 0)}")
    print(f" - Variedade de vocabulário (%): {rel.get('variedade_vocabulario', 0)}")
    print(f" - Vocabulário único (tokens): {rel.get('vocabulario_unico', 0)}")

    # Parágrafos
    paragrafos = rel.get('paragrafos', [])
    print(f" - Parágrafos detectados: {len(paragrafos)}")
    if paragrafos:
        exemplo_par = paragrafos[0].strip().replace("\n", " ")
        if len(exemplo_par) > 180:
            exemplo_par = exemplo_par[:180].rstrip() + "..."
        print(f"   Exemplo (início): {exemplo_par}")

    # Top palavras mais frequentes (limitado)
    mais_freq = rel.get('mais_frequentes', [])[:5]
    if mais_freq:
        print(" - Palavras mais frequentes:")
        for w, c in mais_freq:
            print(f"    {w}: {c}")

    # Repetições relevantes (filtradas e limitadas)
    repeticoes = rel.get('repeticoes_relevantes', [])
    repeticoes_filtradas = [w for w in repeticoes if len(w) > 2]
    if repeticoes_filtradas:
        mostra = repeticoes_filtradas[:10]
        print(f" - Repetições relevantes (ex.): {', '.join(mostra)}")

    print("\n===== FIM DO RELATÓRIO =====\n")

def salvar_relatorio_em_txt(nome_arquivo: str, texto: str, tema: str, rel, fb):
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write("RELATÓRIO DE AVALIAÇÃO\n")
            f.write(f"DATA: {datetime.datetime.now().isoformat()}\n\n")
            f.write(f"TEMA: {tema}\n\n")
            f.write(f"NOTA: {fb['nota_final']} /10  (pontos: {fb['pontos']}/10)\n\n")
            f.write("Comentários:\n")
            for c in fb['comentarios']:
                f.write(" - " + c + "\n")
            f.write("\nSugestões:\n")
            for s in fb['sugestoes']:
                f.write(" - " + s + "\n")
            f.write("\nResumo das métricas:\n")
            f.write(f" - Número de palavras: {rel.get('num_palavras', 0)}\n")
            f.write(f" - Número de frases: {rel.get('num_frases', 0)}\n")
            f.write(f" - Média de palavras por frase: {rel.get('media_palavras_por_frase', 0)}\n")
            f.write(f" - Variedade de vocabulário (%): {rel.get('variedade_vocabulario', 0)}\n")
            f.write(f" - Vocabulário único (tokens): {rel.get('vocabulario_unico', 0)}\n")
            paragrafos = rel.get('paragrafos', [])
            f.write(f" - Parágrafos detectados: {len(paragrafos)}\n")
            if paragrafos:
                resumo = paragrafos[0][:200].replace("\n", " ")
                if len(paragrafos[0]) > 200:
                    resumo = resumo.rstrip() + "..."
                f.write(f"   Exemplo (início): {resumo}\n")
            mais_freq = rel.get('mais_frequentes', [])[:5]
            if mais_freq:
                f.write(" - Palavras mais frequentes:\n")
                for w, c in mais_freq:
                    f.write(f"    {w}: {c}\n")
            repeticoes = rel.get('repeticoes_relevantes', [])
            repeticoes_filtradas = [w for w in repeticoes if len(w) > 2]
            if repeticoes_filtradas:
                mostra = repeticoes_filtradas[:10]
                f.write(f" - Repetições relevantes (ex.): {', '.join(mostra)}\n")
        print(f"Relatório salvo em: {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar relatório: {e}")

def forcar_escolha_genero(genero_detectado: str) -> str:
    """
    Se o gênero detectado for 'desconhecido', força o usuário a escolher um gênero válido.
    Caso contrário, retorna o gênero detectado.
    """
    if genero_detectado == "desconhecido":
        print("\n⚠ Gênero textual não identificado automaticamente.")
        print("Por favor, escolha o gênero do texto:")
        print("  - dissertação")
        print("  - conto")
        print("  - poema")
        print("  - fábula")
        while True:
            escolha = input("Informe o gênero: ").strip().lower()
            if escolha in ("dissertação", "dissertacao", "conto", "poema", "fábula", "fabula"):
                return escolha
            else:
                print("Gênero inválido. Tente novamente.")
    return genero_detectado

def ajuda_criterios():
    print("\n=== AJUDA: CRITÉRIOS DE AVALIAÇÃO ===")
    print("Estrutura: organização em parágrafos; divisão clara em introdução, desenvolvimento e conclusão.")
    print("Coesão: uso de conectores e conexão lógica entre frases.")
    print("Clareza: frases objetivas, sem períodos muito longos ou repetições desnecessárias.")
    print("Vocabulário: diversidade de vocabulário e adequação de linguagem (evitar gírias).")
    print("Adequação ao tema: relação entre o conteúdo do texto e o tema informado pelo usuário.")
    print("Observação: o sistema usa aproximações; a avaliação humana é sempre mais precisa.\n")

def main():
    print("Bem-vindo ao Avaliador de Textos.")
    while True:
        opc = mostrar_menu()
        if opc == "1":
            tema = input("\nInforme o tema da atividade (ou deixe vazio): ").strip()
            print("\nOpcional: indique o gênero textual a ser avaliado para sobrescrever a detecção automática.")
            print("Gêneros possíveis: dissertação, conto, poema, fábula")
            genero_informado = input("Informe o gênero (ou deixe vazio para detecção automática): ").strip().lower()
            texto = ler_texto_terminal()
            if not texto.strip():
                print("Nenhum texto informado. Voltando ao menu.")
                continue
            rel = analisar_texto(texto, tema)
            if genero_informado:
                # aceita apenas gêneros conhecidos; caso contrário mantém a detecção
                if genero_informado in ("dissertação", "dissertacao", "conto", "poema", "fábula", "fabula"):
                    rel["genero"] = genero_informado
                else:
                    print("Gênero não reconhecido — será usada a detecção automática.")
            else:
                # Se nenhum gênero foi informado, forçar escolha se detectado como 'desconhecido'
                rel["genero"] = forcar_escolha_genero(rel["genero"])
            fb = pontuar_e_gerar_feedback(rel, tema)
            imprimir_relatorio_completo(texto, tema, rel, fb)
            if input("Deseja salvar o relatório em .txt? (s/n): ").strip().lower() == "s":
                nome = input("Nome do arquivo (ex: relatorio1.txt): ").strip()
                if not nome.lower().endswith(".txt"):
                    nome += ".txt"
                salvar_relatorio_em_txt(nome, texto, tema, rel, fb)
        elif opc == "2":
            tema = input("\nInforme o tema da atividade (ou deixe vazio): ").strip()
            print("\nOpcional: indique o gênero textual a ser avaliado para sobrescrever a detecção automática.")
            print("Gêneros possíveis: dissertação, conto, poema, fábula")
            genero_informado = input("Informe o gênero (ou deixe vazio para detecção automática): ").strip().lower()
            caminho = input("Caminho do arquivo .txt: ").strip()
            texto = ler_arquivo_txt(caminho)
            if texto is None:
                continue
            rel = analisar_texto(texto, tema)
            if genero_informado:
                if genero_informado in ("dissertação", "dissertacao", "conto", "poema", "fábula", "fabula"):
                    rel["genero"] = genero_informado
                else:
                    print("Gênero não reconhecido — será usada a detecção automática.")
            else:
                # Se nenhum gênero foi informado, forçar escolha se detectado como 'desconhecido'
                rel["genero"] = forcar_escolha_genero(rel["genero"])
            fb = pontuar_e_gerar_feedback(rel, tema)
            imprimir_relatorio_completo(texto, tema, rel, fb)
            if input("Deseja salvar o relatório em .txt? (s/n): ").strip().lower() == "s":
                nome = input("Nome do arquivo (ex: relatorio1.txt): ").strip()
                if not nome.lower().endswith(".txt"):
                    nome += ".txt"
                salvar_relatorio_em_txt(nome, texto, tema, rel, fb)
        elif opc == "3":
            ajuda_criterios()
        elif opc == "4":
            print("Encerrando. Boa sorte com seus textos!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
