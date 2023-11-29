import matplotlib.pyplot as plt
import numpy as np
from shiny import App, render, ui

# Criando alguns dados aleatórios
t = np.linspace(0,2*np.pi, 1024)
data2d = np.sin(t)[:, np.newaxis] * np.cos(t)[np.newaxis]

app_ui = ui.page_fixed(
    ui.h2("Brincando com mapa de cores"),
    ui.markdown("""
        Este aplicativo é baseado em um [exemplo Matplotlib] [0] que exibe dados 2D
        com um mapa de cores ajustável pelo usuário. Usamos um controle deslizante 
        de intervalo para definir os dados intervalo que é coberto pelo mapa de cores.
        
        [0]: https://matplotlib.org/3.5.3/gallery/userdemo/colormap_interactive_adjustment.html
    """),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_radio_buttons("cmap", "Colormap type",
                dict(viridis = "Perceptual", gist_heat="Sequencitial", RdYlBu="Diverging")
            ),
            ui.input_slider("range", "Color range", -1, 1, value=(-1,1), step=0.05),
        ),
        ui.panel_main(
            ui.output_plot("plot")
        )
    )
)

def server(input, output, session):
    @output
    @render.plot
    def plot():
        fig, ax = plt.subplots()
        im = ax.imshow(data2d, cmap=input.cmap(), vmin=input.range()[0], vmax=input.range()[1])
        fig.colorbar(im, ax=ax)
        return fig

app = App(app_ui, server)