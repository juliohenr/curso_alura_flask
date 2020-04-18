from flask import Flask, render_template, request, redirect


app = Flask(__name__)

class Jogo:

    def __init__(self,nome,categoria,console):

        self.nome = nome
        self.categoria = categoria
        self.console = console





jogo1 = Jogo('super mario','ação','snes')
jogo2 = Jogo('pokemon gold','rpg','gba')

lista = [jogo1,jogo2]



@app.route('/')
def ola():



    return render_template('lista.html',titulo='jogos',jogos=lista)


@app.route('/novo')
def novo():

    return render_template('novo.html',titulo='Novo Jogo')


@app.route('/criar', methods = ['POST',])
def criar():

    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo3 = Jogo(nome,categoria,console)


    lista.append(jogo3)

    return redirect('/')



app.run(debug=True)

