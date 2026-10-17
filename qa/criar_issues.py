"""
Cria uma Issue no GitHub para cada caso de teste do casos-de-teste.md.

Uso:
    python criar_issues.py --teste           # só mostra o que seria criado
    python criar_issues.py                   # cria as Issues
    python criar_issues.py --sem-regressao   # cria sem os CT-REG
    python criar_issues.py --atualizar       # também atualiza título e texto das Issues que já existem

Requisitos: Python 3.8+ e GitHub CLI (gh) com login feito (gh auth login).
Pode rodar mais de uma vez: casos que já têm Issue são pulados.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time

REPO = "salfis/nasalinha-qa"
ARQUIVO_PADRAO = "casos-de-teste.md"

# Prefixo do ID -> label de área
LABEL_AREA = {
    "AUTH": "area:auth",
    "CHK": "area:checkin",
    "PTS": "area:pontos",
}

# Área dos casos de regressão (CT-REG-01 = Autenticação, e assim por diante)
AREA_REGRESSAO = {
    "01": "area:auth",
    "02": "area:checkin",
    "03": "area:pontos",
}

TITULO_CASO = re.compile(r"^### (CT-(AUTH|CHK|PTS|REG)-(\d+))\s*(?::|—|-)\s*(.+)$")


def ler_casos(caminho):
    """Separa o arquivo em casos, a partir dos títulos '### CT-...'."""
    with open(caminho, encoding="utf-8") as f:
        linhas = f.read().splitlines()

    casos = []
    atual = None
    for linha in linhas:
        m = TITULO_CASO.match(linha)
        if m:
            if atual:
                casos.append(atual)
            atual = {
                "id": m.group(1),
                "prefixo": m.group(2),
                "numero": m.group(3),
                "titulo": m.group(4).strip(),
                "corpo": [],
            }
            continue
        # Um título '## ' fecha o caso atual (início de nova seção)
        if linha.startswith("## ") and atual:
            casos.append(atual)
            atual = None
            continue
        if atual:
            atual["corpo"].append(linha)
    if atual:
        casos.append(atual)

    for c in casos:
        texto = "\n".join(c["corpo"]).strip()
        # Remove o separador '---' do fim de cada caso
        texto = re.sub(r"\n*-{3,}\s*$", "", texto).strip()
        c["corpo"] = texto
    return casos


def labels_do_caso(caso):
    labels = ["caso-de-teste"]
    if caso["prefixo"] == "REG":
        labels.append("regressao")
        area = AREA_REGRESSAO.get(caso["numero"])
        if area:
            labels.append(area)
    else:
        labels.append(LABEL_AREA[caso["prefixo"]])
    return labels


def montar_corpo(caso):
    return (
        f"**ID:** {caso['id']}\n\n"
        f"{caso['corpo']}\n\n"
        "---\n"
        "_Caso de teste documentado em `qa/casos-de-teste.md`._\n"
    )


def gh(*args):
    try:
        return subprocess.run(
            ["gh", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        ).stdout
    except FileNotFoundError:
        sys.exit("Erro: GitHub CLI (gh) não encontrado. Instale em https://cli.github.com")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(e.stderr.strip() or e.stdout.strip())


def ids_existentes():
    """IDs (CT-...) que já têm Issue no repositório -> número da Issue."""
    saida = gh(
        "issue", "list", "--repo", REPO,
        "--state", "all", "--limit", "500",
        "--json", "number,title",
    )
    ids = {}
    for issue in json.loads(saida):
        m = re.search(r"\[(CT-[A-Z]+-\d+)\]", issue["title"])
        if m:
            ids[m.group(1)] = issue["number"]
    return ids


def escrever_corpo_tmp(caso):
    # Corpo vai por arquivo temporário para evitar problemas com acentos e aspas
    with tempfile.NamedTemporaryFile(
        "w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(montar_corpo(caso))
        return tmp.name


def atualizar_issue(numero, caso):
    titulo = f"[{caso['id']}] {caso['titulo']}"
    caminho_tmp = escrever_corpo_tmp(caso)
    try:
        gh("issue", "edit", str(numero), "--repo", REPO,
           "--title", titulo, "--body-file", caminho_tmp)
    finally:
        os.remove(caminho_tmp)


def criar_issue(caso):
    titulo = f"[{caso['id']}] {caso['titulo']}"
    args = ["issue", "create", "--repo", REPO, "--title", titulo]
    for label in labels_do_caso(caso):
        args += ["--label", label]

    caminho_tmp = escrever_corpo_tmp(caso)
    try:
        url = gh(*args, "--body-file", caminho_tmp).strip()
    finally:
        os.remove(caminho_tmp)
    return url


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Cria Issues dos casos de teste.")
    parser.add_argument("--arquivo", default=ARQUIVO_PADRAO,
                        help="caminho do casos-de-teste.md")
    parser.add_argument("--teste", action="store_true",
                        help="só mostra o que seria criado, sem criar nada")
    parser.add_argument("--atualizar", action="store_true",
                        help="atualiza título e texto das Issues que já existem")
    parser.add_argument("--sem-regressao", action="store_true",
                        help="não cria os casos CT-REG")
    args = parser.parse_args()

    if not os.path.exists(args.arquivo):
        sys.exit(f"Erro: arquivo '{args.arquivo}' não encontrado.")

    casos = ler_casos(args.arquivo)
    if args.sem_regressao:
        casos = [c for c in casos if c["prefixo"] != "REG"]

    if not casos:
        sys.exit("Nenhum caso encontrado. Os títulos devem seguir '### CT-XXX-00: Título'.")

    print(f"{len(casos)} casos encontrados em {args.arquivo}\n")

    if args.teste:
        for c in casos:
            print(f"[{c['id']}] {c['titulo']}")
            print(f"    labels: {', '.join(labels_do_caso(c))}")
        print("\nModo teste: nada foi criado. Rode sem --teste para criar.")
        return

    existentes = ids_existentes()
    criadas, atualizadas, puladas, erros = 0, 0, 0, 0

    for c in casos:
        if c["id"] in existentes:
            numero = existentes[c["id"]]
            if not args.atualizar:
                print(f"PULADO  [{c['id']}] já existe (#{numero})")
                puladas += 1
                continue
            try:
                atualizar_issue(numero, c)
                print(f"ATUALIZADO [{c['id']}] #{numero}")
                atualizadas += 1
                time.sleep(1)
            except RuntimeError as e:
                print(f"ERRO    [{c['id']}] {e}")
                erros += 1
            continue
        try:
            url = criar_issue(c)
            print(f"CRIADO  [{c['id']}] {url}")
            criadas += 1
            time.sleep(1)  # evita o limite de criação em sequência do GitHub
        except RuntimeError as e:
            print(f"ERRO    [{c['id']}] {e}")
            erros += 1

    print(f"\nResumo: {criadas} criadas, {atualizadas} atualizadas, {puladas} puladas, {erros} com erro.")
    if erros:
        print("Confira se as labels existem no repositório e se o 'gh auth login' foi feito.")


if __name__ == "__main__":
    main()
