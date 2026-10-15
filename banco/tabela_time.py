from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from database import Time, db_sesseion, Partida, Jogador


def select_todos():
    # Buscar todos os times no banco
    # 1- montar o select
    times_sql = (
        select(Time, func.count(Jogador.id).label("jogadores"))
        .outerjoin(Jogador, Jogador.time_id == Time.id)
        .group_by(Time.id)
    )


    # 2- Executar o select
    times = db_sesseion.execute(times_sql).all()
    return times

def select_quantidade_total():
    times_sql = select(func.count(Time.id))
    qtd_total = db_sesseion.execute(times_sql).scalar()
    return qtd_total
print(select_quantidade_total())

def salvar_times(nome, responsavel, turma):
    try:
        time_novo = Time(nome=nome, responsavel=responsavel, turma=turma)
        db_sesseion.add(time_novo)
        db_sesseion.commit()  # salvar no banco
        flash('Time adicionado com sucesso', 'success')
        return time_novo
    except SQLAlchemyError as e:
        db_sesseion.rollback()
        flash("Ocorreu um erro ao adicionar o time", 'error')
        print(e)
    except Exception as e:
        db_sesseion.rollback()
        flash("Ocorreu um erro ao adicionar o time", 'error')
        print(e)



def select_um(id_time):
    time_sql = select(Time).where(Time.id == id_time)
    time = db_sesseion.execute(time_sql).scalar_one_or_none()
    return time

print(select_um(10))
