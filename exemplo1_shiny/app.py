from shiny import App, ui, render

# Parte 1: interface do usuario (ui)
# Parte 2: server
# Parte 3: combinar os dois usando o 'shiny.App'

#? Exemplo 1
#* Hello World

# Part 1: ui
app_ui = ui.page_fluid(
    ui.input_slider("n","Escolha um número n:", 0,100,40),
    ui.output_text_verbatim("txt")
)

# Part 2: server
#* A parte dinâmica será definida aqui
def server(input, output, session):
    @output # dizer que deve ser exibido na pag. web
    @render.text # dizer que é um texto
    def txt():
        return f"n*2 é {input.n()*2}"
        # inpunt.n() estamos acessando o valor do slider

# Combinar no shiny app
# A variável deve ser "app"

app = App(app_ui, server)