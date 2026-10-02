from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from database import Time, db_sesseion


def select_todos():
    # Buscar todos os times no banco
    # 1- montar o select
    times_sql = select(Time)
    # 2- Executar o select
    times = db_sesseion.execute(times_sql).scalars().all()
    return times

def salvar_times(nome, responsavel, turma):
    try:
        time_novo = Time(nome=nome, responsavel=responsavel, turma=turma)
        db_sesseion.add(time_novo)
        db_sesseion.commit()  # salvar no banco
        flash('Time adicionado com sucesso', 'success')
    except SQLAlchemyError as e:
        db_sesseion.rollback()
        flash("Ocorreu um erro ao adicionar o time", 'error')
        print(e)
    except Exception as e:
        db_sesseion.rollback()
        flash("Ocorreu um erro ao adicionar o time", 'error')
        print(e)
