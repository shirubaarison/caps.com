from flask import Flask, render_template, redirect, request, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlalchemy as db
import datetime
from dateutil import parser

from gameUtils import *

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database
engine = db.create_engine("sqlite:///app.db")
connection = engine.connect()
metadata = db.MetaData()

# Tabelas
users = db.Table('users', metadata, autoload_with=engine)
history = db.Table('history', metadata, autoload_with=engine)

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    """ Filtro para exibir a data de uma maneira bonita """
    date = parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%b %d, %Y'
    return native.strftime(format) 

@app.route("/")
def index():
    """ Página principal """
    return render_template("index.html", inIndex=True)


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Registrar o desgraçado """
    if request.method == "GET":
        if session:
            return redirect("/")
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        conPassword = request.form.get("confirmation")

        # Verificar se o usuário fez alguma cagada
        if not username or not password or not conPassword:
            flash("Você esqueceu de algo seu animal")
            return redirect("/register")
        elif conPassword != password:
            flash("Presta atenção direito que você digitou as senhas errado")
            return redirect("/register")

        # Verificar se o nome de usuário já existe
        query = db.select(users.c['username']).where(users.c['username'] == username)
        userQuery = connection.execute(query).fetchall()
        if not userQuery:
            pass
        elif username == userQuery[0][0]:
            flash("Já existe um usuário com esse nome, pai")
            return redirect("/register")

        # Hash
        passHash = generate_password_hash(password)

        # Inserir
        connection.execute(db.insert(users), {"username": username, "hash": passHash})
        connection.commit()

        flash("Sucesso pae, agora cê já pode entrar e desfrutar das coisas lindas desse website")
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Registrar o desgraçado """
    if request.method == "GET":
        if session:
            return redirect("/")
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        # Verificar se o usuário fez alguma cagada
        if not username or not password:
            flash("Você esqueceu de algo seu animal")
            return redirect("/login")

        # Verificar se o nome de usuário já existe
        query = db.select(users.c['username']).where(users.c['username'] == username)
        userQuery = connection.execute(query).fetchall()
        if not userQuery:
            flash("Usuário não encontrado, pai")
            return redirect("/login")
            
        # Hash
        oldPassHash = connection.execute(db.select(users.c['hash']).where(users.c['username'] == username)).fetchall()
        passHash = generate_password_hash(password)

        if not check_password_hash(oldPassHash[0][0], request.form.get("password")):
            flash("Senha tá errada, pai")
            return redirect("/")

        # Lembrar do ID e nome do usuário
        query = db.select(users.c['id', 'username']).where(users.c['username'] == username)
        userData = connection.execute(query).fetchall()
        
        session["user_id"] = userData[0][0]
        session["username"] = userData[0][1]
        session["logged_in"]= True

        flash("Sucesso pae")
        return redirect("/")


@app.route("/logout")
def logout():
    """Sai da conta"""

    # Esquecer tudo...
    session.clear()

    # Redirecionar
    flash("Deslogado com sucesso")
    return redirect("/")

@app.route("/jogar", methods=["GET", "POST"])
def jogar():
    """Joga o jogo"""
    
    # Verificar se usuário está logado
    if not session:
        flash("Você tem que logar")
        return redirect("/")
    
    if request.method == "GET":
          # Selecionar o adversário aleatóriamente e sua foto também
        jogador = selecionarAdversario()
        jogadorFoto = f"src/{selecionarFoto(jogador)}"

        wins, loses = qtdVitoriasDerrotas()
        opWins, opLoses = qtdOponente(jogador)

        return render_template("jogar.html", inIndex=False, jogador=jogador, jogadorFoto=jogadorFoto, qtdVitorias=wins, opVitorias=opWins)
    
    else:
        # Pegar os dados
        data = request.get_json()
        whoOn = data["whoOn"]
        vitorias1 = data["vitorias1"]
        vitorias2 = data["vitorias2"] 
        adversario = data["adversario"]

        # Inserir na nova tabela de acordo com quem ganhou
        if whoOn == "X":
            connection.execute(db.insert(history), {"username": session['username'] , "opponent": adversario, "state": "won", "value": 1, "userID": session["user_id"], "datetime": datetime.datetime.utcnow()})
        else:
            connection.execute(db.insert(history), {"username": session['username'] , "opponent": adversario, "state": "lost", "value": 0, "userID": session["user_id"], "datetime": datetime.datetime.utcnow()})

        connection.commit()
        
        return redirect("/jogar")
    
@app.route("/partidas")
def partidas():
    """ Visualiza as partidas jogadas na conta """
    
    # Verificar se usuário está logado
    if not session:
        flash("Você tem que logar")
        return redirect("/")

    query = db.select(history.c['opponent'], history.c['state'], history.c['datetime']).where(history.c['userID'] == session["user_id"])
    userQuery = connection.execute(query).fetchall()
    
    wins, loses = qtdVitoriasDerrotas()

    return render_template("partidas.html", partidas=userQuery, qtdVitorias=wins, qtdPerdas=loses)

@app.route("/perfil")
def perfil():
    """ Perfil """
    
    # Verificar se usuário está logado
    if not session:
        flash("Você tem que logar")
        return redirect("/")
    
    return render_template("profile.html")

@app.route("/ranking")
def ranking():
    """ Ranking dos melhores jogadores de jogo da velha """

    _jogadores = []
    j = {}

    users = usuarios()

    for u in users:
        j = {}
        winsTotal, losesTotal = qtdJogador(u)
        j['nome'] = u
        j['wins'] = winsTotal
        j['losses'] = losesTotal
        if winsTotal != 0 or losesTotal != 0:
            _jogadores.append(j)

    for jogador in jogadores:
        j = {}
        winsTotal, losesTotal = qtdOponente(jogador)
        j['nome'] = jogador
        j['wins'] = winsTotal
        j['losses'] = losesTotal
        if winsTotal != 0 and losesTotal != 0:
            _jogadores.append(j)

    _jogadores = sorted(_jogadores, key=lambda x: (x["wins"] - x["losses"], x["wins"]), reverse=True)

    return render_template("ranking.html", jogadores=_jogadores)


def qtdVitoriasDerrotas():
    """ Retorna quantidade de vitórias e derrotas do usuário """

    wins = loses = 0
    query = db.select(history.c['state']).where(history.c['userID'] == session["user_id"])
    executeQuery = connection.execute(query).fetchall()

    for i in executeQuery:
        if i[0] == "won":
            wins += 1
        elif i[0] == "lost":
            loses += 1

    return wins, loses


def qtdOponente(jogador):
    """ Retorna quantidade de vitórias e derrotas do oponente """

    opWins = opLoses = 0
    query = db.select(history.c['state']).where(history.c['opponent'] == jogador)
    executeQuery = connection.execute(query).fetchall()

    for i in executeQuery:
        if i[0] == "won":
            opWins += 1
        elif i[0] == "lost":
            opLoses += 1

    return opWins, opLoses

def qtdJogador(jogador):
    """ Retorna quantidade de vitórias e derrotas do oponente """

    opWins = opLoses = 0
    query = db.select(history.c['state']).where(history.c['username'] == jogador)
    executeQuery = connection.execute(query).fetchall()

    for i in executeQuery:
        if i[0] == "won":
            opWins += 1
        elif i[0] == "lost":
            opLoses += 1

    return opWins, opLoses


def usuarios():
    """ Retorna jogadores do banco de dados """
    
    u = []
    executeQuery = connection.execute(db.select(users.c['username'])).fetchall()
    
    for i in executeQuery:
        u.append(i[0])

    return u