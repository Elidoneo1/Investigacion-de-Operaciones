import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mplcursors

# Función para calcular la distribución
def calcular_distribucion():
    dados, caras = 3, 20
    min_suma, max_suma = dados, dados * caras
    
    # Inicializar matriz de programación dinámica
    dp = np.zeros((dados + 1, max_suma + 1), dtype=int)
    dp[0, 0] = 1
    
    for d in range(1, dados + 1):
        for s in range(1, max_suma + 1):
            dp[d, s] = sum(dp[d-1, max(0, s-caras):s])
    
    sumas = np.arange(min_suma, max_suma + 1)
    conteos = dp[dados, min_suma:max_suma + 1]
    probabilidades = conteos / 8000
    
    return sumas, conteos, probabilidades

# Calcular distribución
sumas, conteos, probabilidades = calcular_distribucion()

# Crear DataFrame para Excel
df = pd.DataFrame({
    'Suma (X)': sumas,
    'Combinaciones posibles': conteos,
    'Probabilidad': probabilidades
})

# Exportar a Excel con formato
with pd.ExcelWriter('distribucion_3d20.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Distribución', index=False)
    
    # Formatear columnas
    workbook = writer.book
    worksheet = writer.sheets['Distribución']
    format_percent = workbook.add_format({'num_format': '0.0000%'})
    worksheet.set_column('C:C', 15, format_percent)
    worksheet.set_column('A:B', 20)

# Gráfica mejorada (valores discretos)
plt.figure(figsize=(14, 7))
markerline, stemlines, baseline = plt.stem(
    sumas,
    probabilidades * 100,
    linefmt='C0-',
    markerfmt='C0o',
    basefmt=' ',
)

# Añadir anotaciones especiales
puntos_destacados = {
    3: 'Mínimo (1+1+1)',
    60: 'Máximo (20+20+20)',
    31: 'Moda (31)',
    32: 'Moda (32)'
}

for x, label in puntos_destacados.items():
    idx = np.where(sumas == x)[0][0]
    y = probabilidades[idx] * 100
    plt.annotate(label, (x, y),
                 xytext=(10, 15),
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle='->'),
                 bbox=dict(fc='white'))

# Configuración de la gráfica
plt.title('Distribución de Probabilidad para 3d20', fontsize=14)
plt.xlabel('Suma de los dados (X)', fontsize=12)
plt.ylabel('Probabilidad (%)', fontsize=12)
plt.grid(True, alpha=0.3, linestyle='--')
plt.xticks(np.arange(3, 61, 3))
plt.xlim(2, 61)

# Interactividad
cursor = mplcursors.cursor(hover=True)
@cursor.connect("add")
def on_add(sel):
    x, y = sel.target
    idx = np.where(sumas == int(x))[0][0]
    sel.annotation.set(text=f"Suma: {int(x)}\nProb: {probabilidades[idx]:.4%}\nCombinaciones: {conteos[idx]}")
    sel.annotation.get_bbox_patch().set(fc="white", alpha=0.95)

plt.show()