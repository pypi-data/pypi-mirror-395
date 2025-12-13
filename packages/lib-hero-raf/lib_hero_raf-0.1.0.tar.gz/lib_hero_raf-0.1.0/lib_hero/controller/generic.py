# app/routers/generic.py
from typing import Any, Callable, Generic, Optional, Type, TypeVar
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import SQLModel, Session
from util.database import get_session
from repository.base import Repository
from service.base import Service

ModelT = TypeVar("ModelT", bound=SQLModel)
CreateT = TypeVar("CreateT", bound=SQLModel)
UpdateT = TypeVar("UpdateT", bound=SQLModel)
ReadT   = TypeVar("ReadT", bound=SQLModel)

class Hooks(Generic[ModelT, CreateT, UpdateT]):
    """
    Pontos de extensão opcionais para regras específicas.
    """
    def pre_create(self, payload: CreateT, session: Session) -> None: ...
    def pre_update(self, payload: UpdateT, session: Session, obj: ModelT) -> None: ...
    def pre_delete(self, session: Session, obj: ModelT) -> None: ...

def create_crud_router(
    *,
    model: Type[ModelT],
    create_schema: Type[CreateT],
    update_schema: Type[UpdateT],
    read_schema: Type[ReadT],
    prefix: str,
    tags: list[str],
    hooks: Optional[Hooks[ModelT, CreateT, UpdateT]] = None,
    page_size_limit: int = 200,
) -> APIRouter:
    """
    Cria endpoints: POST /, GET /, GET /{id}, PATCH /{id}, DELETE /{id}
    """
    router = APIRouter(prefix=prefix, tags=tags)

    repo: Repository[ModelT, CreateT, UpdateT] = Repository(model)
    service: Service[ModelT, CreateT, UpdateT] = Service(repo)
    _hooks = hooks or Hooks()  # instancia vazia (métodos no-op)

    @router.post("/", response_model=read_schema, status_code=201)
    def create_item(payload: create_schema, session: Session = Depends(get_session)):
        if hasattr(_hooks, "pre_create") and callable(_hooks.pre_create):
            _hooks.pre_create(payload, session)
        return service.create(session, payload)

    @router.get("/", response_model=list[read_schema])
    def list_items(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = Query(100, le=page_size_limit),
    ):
        return service.list(session, offset, limit)

    @router.get("/{item_id}", response_model=read_schema)
    def get_item(item_id: int, session: Session = Depends(get_session)):
        obj = service.get(session, item_id)
        if not obj:
            raise HTTPException(404, "Not found")
        return obj

    @router.patch("/{item_id}", response_model=read_schema)
    def update_item(item_id: int, payload: update_schema, session: Session = Depends(get_session)):
        obj = service.get(session, item_id)
        if not obj:
            raise HTTPException(404, "Not found")
        if hasattr(_hooks, "pre_update") and callable(_hooks.pre_update):
            _hooks.pre_update(payload, session, obj)
        try:
            return service.update(session, item_id, payload)
        except ValueError:
            raise HTTPException(404, "Not found")

    @router.delete("/{item_id}", status_code=204)
    def delete_item(item_id: int, session: Session = Depends(get_session)):
        obj = service.get(session, item_id)
        if not obj:
            raise HTTPException(404, "Not found")
        if hasattr(_hooks, "pre_delete") and callable(_hooks.pre_delete):
            _hooks.pre_delete(session, obj)
        try:
            service.delete(session, item_id)
        except ValueError:
            raise HTTPException(404, "Not found")

    return router
