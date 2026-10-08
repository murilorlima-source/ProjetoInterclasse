from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from banco import tabela_time, tabela_jogador, tabela_partida
from database import db_sesseion, Time, Jogador, Partida

app = Flask(__name__)
app.secret_key = "murilorodrigo"


@app.route("/")
def dashboard():
    # Buscar todos os times no banco
    # 1- montar o select
    times_sql = select(Time)
    # 2- Executar o select
    times = tabela_time.select_quantidade_total()
    jogadores_sql = select(Jogador)
    jogadores = tabela_jogador.select_quantidade_total()
    partidas_sql = select(Partida)
    partidas = tabela_partida.select_quantidade_total()

    return render_template(
        "dashboard.html",
        total_jogadores=jogadores,
        total_times=times,
        total_partidas=partidas
    )


@app.route("/jogadores")
def listar_jogadores():
    jogadores = tabela_jogador.select_todos()
    print(jogadores)
    return render_template("jogadores.html", jogadores=jogadores)



@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    # quando clicar no botão cadastrar
    if request.method == "POST":
        # nome vindo do formulario
        time_id = request.form.get("time_id") or None
        nome = request.form.get("nome", "").strip()
        posicao = request.form.get("posicao", "").strip()
        numero_camisa = request.form.get("numero_camisa", "") or None

        if not time_id:
            flash('preencha o time_id', 'error')
            return redirect(url_for("novo_jogador"))
        if not nome:
            flash('Por favor, insira o seu nome', 'error')
            return redirect(url_for("novo_jogador"))
        if not numero_camisa:
            flash('Por favor, insira o seu número', 'error')
            return redirect(url_for("novo_jogador"))
        if not posicao:
            flash('Por favor, insira o seu posição', 'error')
            return redirect(url_for("novo_jogador"))
        #salvar no banco
        tabela_jogador.salvar_jogadores(nome=nome, posicao=posicao, time_id=time_id, numero_camisa=numero_camisa)

    jogador = tabela_jogador.select_todos()
    times = tabela_time.select_todos()
    return render_template("jogadores.html", jogador=jogador, times=times)


@app.route("/times")
def listar_times():
    times = tabela_time.select_todos()
    print(times)
    return render_template("times.html", times=times)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    # 1- pegar os valores digitado nos form
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        responsavel = request.form.get("responsavel", "").strip()
        turma = request.form.get("turma", "").strip()
        # 2- verificar se foi digitado
        if not nome:
            flash('Por favor, insira o seu nome', 'Error')
            return redirect(url_for("novo_time"))
        if not turma:
            flash('Preencha a turma do time', 'Error')
            return redirect(url_for("novo_time"))
        if not responsavel:
            flash('Por favor, insira o seu responsavel', 'Error')
            return redirect(url_for("novo_time"))
        # 3- salvar no banco
        tabela_time.salvar_times(nome=nome, responsavel=responsavel, turma=turma)

    times = tabela_time.select_todos()
    return render_template("times.html", times=times)

@app.route("/partidas")
def listar_partidas():
    partidas = tabela_partida.select_todos()
    print(partidas)
    return render_template("partidas.html", partidas=partidas)


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():
    if request.method == "POST":
        # pegar os campos no form
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()
        # verificar se foi digitado

        if not time_casa_id:
            flash('Por favor, insira o seu time', 'error')
            return redirect(url_for("nova_partida"))
        if not time_visitante_id:
            flash('Por favor, insira seu time', 'error')
            return redirect(url_for("nova_partida"))
        if not gols_casa:
            flash('Por favor, insira o seu gols', 'error')
            return redirect(url_for("nova_partida"))
        if not data_partida:
            flash('Por favor, insira o seu data', 'error')
            return redirect(url_for("nova_partida"))
        if not gols_visitante:
            flash('Por favor, insira o seu gols', 'error')
            return redirect(url_for("nova_partida"))


        #salvar no banco

        tabela_partida.salvar_partida(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)

    partidas = tabela_partida.select_todos()
    times = tabela_time.select_todos()

    return render_template("partidas.html", partidas=partidas, times=times)


if __name__ == "__main__":
    app.run(debug=True)



