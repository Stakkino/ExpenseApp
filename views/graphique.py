from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils.constants import *

class GraphiqueManager:
    def __init__(self):
        self.fig = Figure(figsize=(5, 2), dpi=100, facecolor=FOND_CARTE)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(FOND_CARTE)
        self._style_ax()

    def _style_ax(self):
        self.ax.tick_params(axis='x', colors='white', labelsize=8)
        self.ax.tick_params(axis='y', colors='white', labelsize=8)
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.ax.grid(axis='y', color='gray', linestyle='--', alpha=0.3)

    def update_graph(self, recettes, depenses):
        self.ax.clear()
        self._style_ax()
        x = range(7)
        labels = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
        self.ax.plot(x, recettes, color="#07e13a", marker='o', label='Recettes', linewidth=2)
        self.ax.plot(x, depenses, color="#d12f1c", marker='o', label='Dépenses', linewidth=2)
        
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(labels)
        self.fig.tight_layout(pad=1.0)
        self.canvas.draw()

def creer_figure_graphique():
    manager = GraphiqueManager()
    return manager.fig, manager.canvas, manager.ax

def dessiner_courbe(ax, recettes, depenses):
    ax.clear()
    ax.set_facecolor(FOND_CARTE)
    ax.tick_params(axis='x', colors='white', labelsize=8)
    ax.tick_params(axis='y', colors='white', labelsize=8)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis='y', color='white', linestyle='--', alpha=0.2)
    x = range(7)
    labels = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
    ax.plot(x, recettes, color="#07e13a", marker='o', linestyle='-', linewidth=2, label='Recettes')
    ax.plot(x, depenses, color='#d12f1c', marker='o', linestyle='-', linewidth=2, label='Dépenses')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.figure.subplots_adjust(bottom=0.2)