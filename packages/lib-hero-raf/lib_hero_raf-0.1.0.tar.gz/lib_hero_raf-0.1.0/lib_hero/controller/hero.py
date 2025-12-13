# app/routers/hero.py
from fastapi import HTTPException
from sqlmodel import Session, select
from controller.generic import create_crud_router, Hooks
from model.models import Hero, Team
from model.dto import HeroCreate, HeroUpdate, HeroRead

class HeroHooks(Hooks[Hero, HeroCreate, HeroUpdate]):
    def pre_create(self, payload: HeroCreate, session: Session) -> None:
        # se veio team_id, valida
        if payload.team_id is not None and payload.team_id != 0:
            if not session.get(Team, payload.team_id):
                raise HTTPException(400, "team_id inválido")

    def pre_update(self, payload: HeroUpdate, session: Session, obj: Hero) -> None:
        # se vai alterar team_id, valida
        if payload.team_id is not None:
            if payload.team_id != 0 and not session.get(Team, payload.team_id):
                raise HTTPException(400, "team_id inválido")

router = create_crud_router(
    model=Hero,
    create_schema=HeroCreate,
    update_schema=HeroUpdate,
    read_schema=HeroRead,
    prefix="/heroes",
    tags=["heroes"],
    hooks=HeroHooks(),
)
