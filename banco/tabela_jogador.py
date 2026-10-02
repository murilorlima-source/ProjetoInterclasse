from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from database import db_sesseion, Jogadores


def select_todos():
    # buscar todos os jogadores no banco
    # 1- montar o select
    jogadores_sql = select(Jogadores)
    # 2- Executar o select
    jogadores = db_sesseion.execute(jogadores_sql).scalars().all()
    return jogadores



def salvar_jogadores(nome, posicao, time_id, numero_camisa):
    try:
        jogador_novo = Jogadores(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=int(time_id))
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