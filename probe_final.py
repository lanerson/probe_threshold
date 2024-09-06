import os
import shutil
import statistics
import subprocess

# Parâmetro fixo para executar os experimentos
N = 10
# Lista de experimentos
experiments = ["fibonacci.py", "gauss_legendre_quadrature.py", "prob_calculator.py", "look_and_say.py", "test_belief_propagation.py"]
experiments = ["scripts/" + n for n in experiments]
# Parâmetros
param = ["-s", "db-file", "-H", "murmur", "-m", "2d-ad"]

# Função para excluir pastas e arquivos
def limpar_arquivos_e_pastas():
    # Listar pastas e arquivos a serem excluídos
    arquivos_para_excluir = ['threshold.txt']
    pastas_para_excluir = ['.intpy']

    # Excluir pastas
    for root, dirs, files in os.walk(".", topdown=False):
        for name in dirs:
            if name == '__pycache__':
                caminho = os.path.join(root, name)
                shutil.rmtree(caminho)
                print(f'A pasta "{caminho}" foi excluída com sucesso.')
                
    for pasta in pastas_para_excluir:
        if os.path.isdir(pasta):
            shutil.rmtree(pasta)
            print(f'A pasta "{pasta}" foi excluída com sucesso.')

    # Excluir arquivos
    for arquivo in arquivos_para_excluir:
        if os.path.isfile(arquivo):
            os.remove(arquivo)
            print(f'O arquivo "{arquivo}" foi excluído com sucesso.')
        else:
            print(f'O arquivo "{arquivo}" não foi encontrado ou não é um arquivo.')

# Limpar pastas e arquivos antes de iniciar os experimentos
limpar_arquivos_e_pastas()
# Executar os experimentos
for i in range(5):
    args = ["python3", experiments[i], str(N)] + param
    for j in range(5):
        print(f"Executando {experiments[i]} pela {j + 1}ª vez")
        subprocess.run(args)

# Processar o arquivo threshold.txt
threshold = 0
if os.path.isfile("threshold.txt"):
    with open("threshold.txt", "r") as file:
        tempos = file.readlines()[:-1]
        tempos = [float(n.strip()) for n in tempos]
        acc = []
        for i in range(0, len(tempos), 5):
            acc.append(statistics.median(tempos[i:i + 5]))
        threshold = max(acc)

# Atualizar o arquivo threshold.txt com o novo valor
with open("threshold.txt", "w") as file:
    file.write(str(threshold))

print(f"Threshold atualizado para: {threshold}")