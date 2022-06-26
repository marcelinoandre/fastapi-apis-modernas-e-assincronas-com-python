from time import sleep
from typing import Any, Dict, List, Optional

from fastapi import (Depends, FastAPI, Header, HTTPException, Path, Query,
                     Response, status)

from models import Curso

cursos = [
    {'id': 1, 'titulo': 'Programação para Leigos', 'aulas': 42, 'horas': 56},
    {'id': 2, 'titulo': 'Algoritmos e Lógica de Programação', 'aulas': 52, 'horas': 66},
]


def fake_db():
    try:
        print('Abrindo conexão com banco de dados...')
    finally:
        print('Fechando conexão com banco de dados...')


app = FastAPI(
    title='API de Cursos da Geek University',
    version='0.0.1',
    description='Uma API para estudo do FastAPI'
)


@app.get('/cursos',
         description='Retorna todos os cursos ou uma lista vazia.',
         summary='Retorna todos os cursos',
         response_model=List[Curso],
         response_description='Cursos encontrados com sucesso.')
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int = Path(default=None, title='ID do curso', description='Deve ser entre 1 e 300', gt=0, lt=300), db: Any = Depends(fake_db)):
    curso = search_curso(curso_id=curso_id, data=cursos)    
    if curso:
        return curso
    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')


@app.post('/cursos', status_code=status.HTTP_201_CREATED, response_model=Curso)
async def post_curso(curso: Curso):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)

    print(cursos)

    return curso


@app.put('/cursos/{curso_id}')
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    curso_data = search_curso(curso_id=curso_id, data=cursos)   
    if curso_data:
        return curso
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Não existe um curso com id {curso_id}')


@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):

    curso_data = search_curso(curso_id=curso_id, data=cursos)   
    if curso_data:
        cursos_del = list(filter(lambda x: x['id'] != curso_id, cursos ))
        print(cursos_del)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Não existe um curso com id {curso_id}')


@app.get('/calculadora')
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), x_geek: str = Header(default=None), c: Optional[int] = None):
    soma: int = a + b
    if c:
        soma = soma + c

    print(f'X-GEEK: {x_geek}')

    return {"resultado": soma}


def search_curso(curso_id: int, data: cursos )->dict | None:
    search = list(filter(lambda x: x['id'] == curso_id, data ))

    if len(search):
        return search[0]

