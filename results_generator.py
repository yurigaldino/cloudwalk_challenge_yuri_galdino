import re
import json

# Inicializa as estruturas de dados
players = set()
kills = {}

# Expressões regulares para capturar eventos relevantes
player_connect_pattern = re.compile(r'ClientUserinfoChanged: \d+ n\\([^\\]+)')
kill_pattern = re.compile(r'Kill: \d+ \d+ \d+: ([^ ]+) killed ([^ ]+)')

# Abre e lê o arquivo de log
with open('c:/Users/Yuri/Desktop/qgames.log.txt', 'r') as file:
    for line in file:
        # Captura os jogadores que se conectaram
        player_connect_match = player_connect_pattern.search(line)
        if player_connect_match:
            player = player_connect_match.group(1)
            players.add(player)
            if player not in kills:
                kills[player] = 0

        # Captura os eventos de morte
        kill_match = kill_pattern.search(line)
        if kill_match:
            killer, victim = kill_match.groups()
            if killer != '<world>':
                kills[killer] += 1
            if victim in kills:
                kills[victim] -= 1

# Converte o conjunto de jogadores para uma lista
players_list = list(players)

# Cria o dicionário de saída
output = {
    "players": players_list,
    "kills": kills
}

# Salva a saída em formato JSON
with open('c:/Users/Yuri/Desktop/CloudwalkTest/results.json', 'w') as outfile:
    json.dump(output, outfile, indent=4)

print(json.dumps(output, indent=4))