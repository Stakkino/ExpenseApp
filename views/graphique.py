from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils.constants import *

def creer_figure_graphique():
    fig = Figure(figsize=(5, 2), dpi=100, facecolor=FOND_CARTE)
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.set_facecolor(FOND_CARTE)
    return fig, canvas, ax

def dessiner_bar_chart(ax, recettes, depenses):
    ax.clear()
    ax.set_facecolor(FOND_CARTE)
    x = range(7)
    labels = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
    ax.bar([i-0.2 for i in x], recettes, width=0.3, color='#2ecc71')
    ax.bar([i+0.2 for i in x], depenses, width=0.3, color='#e74c3c')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, color='white', fontsize=8) 
    ax.tick_params(axis='y', colors='white', labelsize=8)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis='y', color='gray', linestyle='--', alpha=0.3)
    ax.figure.tight_layout(pad=1.0)