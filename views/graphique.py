from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from utils.constants import *


class GraphiqueManager:
    def __init__(self):
        self.fig = Figure( figsize=(7, 3.5), dpi=100,facecolor=FOND_CARTE)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(FOND_CARTE)
        self._style_ax()

    def _style_ax(self):
        self.ax.tick_params( axis='x', colors='white', labelsize=9)
        self.ax.tick_params( axis='y', colors='white', labelsize=9)
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.ax.grid( axis='y', color='white', linestyle='--', alpha=0.15)
        self.ax.set_axisbelow(True)

    def update_graph(self,recettes,depenses,economies):
        self.ax.clear()
        self._style_ax()
        x = range(7)
        labels = [ 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']

        # BARRES
        largeur = 0.22
        self.ax.bar([i - largeur for i in x],recettes,width=largeur,color="#FFB830",label="Recettes",alpha=0.90)
        self.ax.bar(x,depenses,width=largeur,color="#FF4757",label="Dépenses",alpha=0.90)
        self.ax.bar([i + largeur for i in x],economies,width=largeur,color="#3D9BE9",label="Économies",alpha=0.90)

        # DESIGN
        self.ax.set_xticks(list(x))
        self.ax.set_xticklabels(labels)
        self.ax.set_ylabel("Montant (Ar)",color="white",fontsize=9)
        self.ax.legend(loc="upper left",frameon=False,labelcolor="white",fontsize=8)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.fig.tight_layout(pad=1.5)
        self.canvas.draw()


def creer_figure_graphique():
    manager = GraphiqueManager()
    return (manager.fig, manager.canvas, manager.ax)


def dessiner_courbe(ax,recettes,depenses,economies):
    ax.clear()
    ax.set_facecolor(FOND_CARTE)
    ax.tick_params(axis='x',colors='white',labelsize=9)
    ax.tick_params(axis='y',colors='white',labelsize=9)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(axis='y', color='white', linestyle='--', alpha=0.15)
    ax.set_axisbelow(True)
    x = list(range(7))
    labels = ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim']
    largeur = 0.22

    ax.bar([i - largeur for i in x],recettes,width=largeur,color="#FFB830",label="Recettes")
    ax.bar(x,depenses,width=largeur,color="#FF4757",label="Dépenses")
    ax.bar([i + largeur for i in x],economies,width=largeur,color="#3D9BE9",label="Économies")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Montant (Ar)",color="white",fontsize=9)
    ax.legend(loc="upper left",frameon=False,labelcolor="white",fontsize=8)
    ax.figure.subplots_adjust(left=0.08,right=0.98,top=0.90,bottom=0.20)