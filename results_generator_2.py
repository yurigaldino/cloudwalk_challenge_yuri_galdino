import re
import json
from collections import defaultdict

# Inicializa as estruturas de dados
matches = defaultdict(lambda: {
    "total_kills": 0,
    "players": set(),
    "kills": defaultdict(int),
    "kills_by_means": defaultdict(int)
})
current_match = 1

# Expressões regulares para capturar eventos relevantes
player_connect_pattern = re.compile(r'ClientUserinfoChanged: \d+ n\\([^\\]+)')
kill_pattern = re.compile(r'Kill: \d+ \d+ \d+: ([^ ]+) killed ([^ ]+) by ([^ ]+)')
new_match_pattern = re.compile(r'InitGame:')

# Abre e lê o arquivo de log
with open('c:/Users/Yuri/Desktop/qgames.log.txt', 'r') as file:
    for line in file:
        # Detecta o início de uma nova partida
        if new_match_pattern.search(line):
            current_match += 1

        # Captura os jogadores que se conectaram
        player_connect_match = player_connect_pattern.search(line)
        if player_connect_match:
            player = player_connect_match.group(1)
            matches[current_match]["players"].add(player)
            if player not in matches[current_match]["kills"]:
                matches[current_match]["kills"][player] = 0

        # Captura os eventos de morte
        kill_match = kill_pattern.search(line)
        if kill_match:
            killer, victim, means = kill_match.groups()
            matches[current_match]["total_kills"] += 1
            matches[current_match]["kills_by_means"][means] += 1
            if killer != '<world>':
                matches[current_match]["kills"][killer] += 1
            if victim in matches[current_match]["kills"]:
                matches[current_match]["kills"][victim] -= 1

# Converte os conjuntos de jogadores para listas
for match in matches.values():
    match["players"] = list(match["players"])

# Gera o ranking de jogadores
ranking = defaultdict(int)
for match in matches.values():
    for player, kills in match["kills"].items():
        ranking[player] += kills

# Ordena o ranking
sorted_ranking = sorted(ranking.items(), key=lambda item: item[1], reverse=True)

# Cria o dicionário de saída
output = {
    "matches": matches,
    "ranking": sorted_ranking
}

# Salva a saída em formato JSON
with open('c:/Users/Yuri/Desktop/CloudwalkTest/results.json', 'w') as outfile:
    json.dump(output, outfile, indent=4)

print(json.dumps(output, indent=4))