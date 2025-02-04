import random
from collections import defaultdict

num_lanzamientos = int(input("Numero de Lanzamientos: "))

frecuencia_suma = defaultdict(int)

for _ in range(num_lanzamientos):
    dice1 = random.randint(1, 20)
    dice2 = random.randint(1, 20)
    dice3 = random.randint(1, 20)
    sum = dice1 + dice2 + dice3
    frecuencia_suma[sum] += 1

print("\nTabla de frecuencias:")
print("Suma (X)\tFrecuencia\tHistograma")
for x in range(3, 61):
    freq = frecuencia_suma.get(x, 0)
    barra = '■' * (freq // 100) 
    print(f"{x:2}\t{freq:9}\t\t{barra}")

