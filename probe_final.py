import statistics
import subprocess

# parametro fixo para executar os experimentos
N = 10
# lista de experimentos
experiments = ["fibonacci.py", "gauss_legendre_quadrature.py", "prob_calculator.py","look_and_say.py","test_belief_propagation.py"]
experiments = ["scripts/"+n for n in experiments]
# parametros
param = ["-s","db-file","-H", "murmur","-m", "2d-ad"]

for i in range(5):
    # ATENÇÃO
    # Excluir as pastas .intpy e __pycache__, caso existam
    # Excluir o arquivo threshold.txt, caso exista
    args = ["python3",experiments[i],str(N)] + param
    for j in range(5):
        print(f"executando {experiments[i]} pela {j+1}º vez")
        subprocess.run(args)        
        
threshold = 0
with open("threshold.txt","r") as file:
    tempos = file.readlines()[:-1]
    tempos = [float(n[:-1]) for n in tempos]
    acc = []
    for i in range(0,len(tempos),5):
        acc.append(statistics.median(tempos[i:i+5]))
    threshold = max(acc)

# input("Posso continuar?")
with open("threshold.txt","w") as file:
    file.write(str(threshold))
