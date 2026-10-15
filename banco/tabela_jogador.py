from flask import flash
from sqlalchemy import select, func, join
from sqlalchemy.exc import SQLAlchemyError
from database import db_sesseion, Time, Jogador, Partida


def salvar_jogadores(nome, posicao, time_id, numero_camisa):
    try:
        jogador_novo = Jogador(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=int(time_id))
        db_sesseion.add(jogador_novo)
        db_sesseion.commit()
        flash('Jogador adicionado com sucesso', 'success')
    except SQLAlchemyError as e:
        db_sesseion.rollback()
        print(e)
        flash('Erro ao salvar esse jogador no banco de dados{}', 'error')
    except Exception as e:
        db_sesseion.rollback()
        flash('Erro ao salvar esse jogador', f'erro')
        print(e)


def select_todos():
    # buscar todos os jogadores no banco
    # 1- montar o select
    # join(Tabela que eu quero juntar, condição=chave estrangeira igual chave primaria)
    jogadores_sql = select(Jogador, Time).join(Time, Jogador.time_id == Time.id)
    # 2- Executar o select
    # usar scalars quando tiver somente uma tabela
    jogadores = db_sesseion.execute(jogadores_sql).all()
    print(jogadores)
    return jogadores

def select_quantidade_total():
    jogadores_sql = select(func.count(Jogador.id))
    qtd_total = db_sesseion.execute(jogadores_sql).scalar()
    return qtd_total
print(select_quantidade_total())




def select_um(id_jogador):
    jogador_sql = select(Jogador).where(Jogador.id == id_jogador)
    jogador = db_sesseion.execute(jogador_sql).scalar_one_or_none()
    return jogador
print(select_um(1))

def select_por_time(id_time):
    jogador_sql = select(Jogador).where(Jogador.time_id == id_time)
    jogador = db_sesseion.execute(jogador_sql).scalars().all()
    return jogador
print(select_por_time(1))
