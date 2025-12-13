# app/models.py
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# ---------- TEAM ----------
class TeamBase(SQLModel):
    name: str = Field(min_length=2, max_length=120)

class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # back_populates liga Team <-> Hero
    heroes: List["Hero"] = Relationship(back_populates="team")


# ---------- HERO ----------
class HeroBase(SQLModel):
    name: str = Field(min_length=2, max_length=120)
    secret_name: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0, le=200)

class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")
