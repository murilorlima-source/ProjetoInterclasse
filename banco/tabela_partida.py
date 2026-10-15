from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

from database import db_sesseion, Partida, Time


def select_todos():
    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)

    partidas_sql = (
        select(Partida, TimeCasa, TimeVisitante)
        .join(TimeCasa, Partida.time_casa_id == TimeCasa.id)
        .join(TimeVisitante, Partida.time_visitante_id == TimeVisitante.id)
    )



    partidas_casa = db_sesseion.execute(partidas_sql).all()
    print(partidas_casa)
    return partidas_casa

def select_quantidade_total():
    partidas_sql = select(func.count(Partida.id))
    qtd_total = db_sesseion.execute(partidas_sql).scalar()
    return qtd_total
print(select_quantidade_total())



def select_partidas_time(id_time):
    TimeCasa = aliased(Time)
    TimeVisitante = aliased(Time)

    partidas_sql = (
        select(Partida, TimeCasa, TimeVisitante)
        .join(TimeCasa, Partida.time_casa_id == TimeCasa.id)
        .join(TimeVisitante, Partida.time_visitante_id == TimeVisitante.id)
        .where(or_(Partida.time_casa_id == id_time, Partida.time_visitante_id == id_time))
    )
    partidas_time = db_sesseion.execute(partidas_sql).all()
    return partidas_time



def salvar_partida(time_casa_id, time_visitante_id, gols_casa, gols_visitante, data_partida):
    try:
        partidanova = Partida(time_casa_id=int(time_casa_id), time_visitante_id=int(time_visitante_id),
                              gols_casa=int(gols_casa), gols_visitante=int(gols_visitante),
                              data_partida=data_partida)
        db_sesseion.add(partidanova)
        db_sesseion.commit()
        flash('Partida adicionada com sucesso', 'success')
    except SQLAlchemyError as e:
        db_sesseion.rollback()
        print(e)
        flash("Erro ao criar a partida", "Error")

    except Exception as e:
        db_sesseion.rollback()
        print(e)
        flash("Erro ao criar a partida", "Error")






