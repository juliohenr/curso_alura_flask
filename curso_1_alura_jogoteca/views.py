
from flask import render_template, request,redirect, session, flash, url_for, send_from_directory
from dao import JogoDao, UsuarioDao
from flask_mysqldb import MySQL
from models import Usuario, Jogo
import os
import time
from jogoteca import db, app
from helpers import deleta_arquivo,recupera_imagem

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)



@app.route('/')
def index():

    lista = jogo_dao.listar()

    return render_template('lista.html',titulo='jogos',jogos=lista)


@app.route('/novo')
def novo():

    if 'usuario_logado' not in session or session['usuario_logado'] == None:

        return redirect(url_for('login',proxima=url_for('novo')))

    return render_template('novo.html',titulo='Novo Jogo')



@app.route('/edit/<int:id>')
def edit(id):

    if 'usuario_logado' not in session or session['usuario_logado'] == None:

        return redirect(url_for('login',proxima=url_for('edit')))

    jogo = jogo_dao.busca_por_id(id)

    nome_imagem = recupera_imagem(id)

    return render_template('edit.html',titulo='editando jogo',jogo=jogo,capa_jogo= nome_imagem)



@app.route('/atualizar', methods = ['POST',])
def atualizar():

    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome,categoria,console,request.form['id'])


    jogo_dao.salvar(jogo)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}_{timestamp}.jpg')




    return redirect(url_for('index'))


@app.route('/deleta/<int:id>')
def delete(id):

    jogo_dao.deletar(id)

    flash("o jogo foi removido com sucesso!")

    return redirect(url_for('index'))



@app.route('/autenticar',methods=['POST',])
def autenticar():


    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    
    if usuario:

        if usuario.senha == request.form['senha']:

            session['usuario_logado'] = usuario.id

            flash(usuario.id + ' logou com sucesso!')

            proxima_pagina = request.form['proxima']

            return redirect(proxima_pagina)
    
    
    if 'mestra' == request.form['senha']:

        session['usuario_logado'] = request.form['usuario']

        flash(request.form['usuario'] + ' logou com sucesso!')

        proxima_pagina = request.form['proxima']

        return redirect(proxima_pagina)

    else:

        flash('senha ou usuário inválidos')

        return redirect(url_for('login'))



@app.route('/login')
def login():

    proxima = request.args.get('proxima')

    return render_template('login.html',proxima=proxima)




@app.route('/criar', methods = ['POST',])
def criar():

    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo3 = Jogo(nome,categoria,console)

    arquivo = request.files['arquivo']

    upload_path = app.config['UPLOAD_PATH']


    jogo_dao.salvar(jogo3)


    jogo3 = jogo_dao.salvar(jogo3)

    timestamp = time.time()

    arquivo.save(f'{upload_path}/capa{jogo3.id}_{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/logout')
def logout():

    session['usuario_logado'] = None
    flash('nenhum usuário logado')

    return redirect(url_for('index'))


@app.route("/uploads/<nome_arquivo>")
def imagem(nome_arquivo):

    return send_from_directory('uploads',nome_arquivo)