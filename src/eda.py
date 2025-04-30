import seaborn as sns
import matplotlib.pyplot as plt

def visualizar_distribucion_reclamos(df):
    """Grafica la cantidad de reclamos por año"""
    plt.figure(figsize=(10,5))
    sns.countplot(x=df["AÑO"], palette="coolwarm")
    plt.title("Distribución de Reclamos por Año")
    plt.xlabel("Año")
    plt.ylabel("Cantidad de Reclamos")
    plt.show()
