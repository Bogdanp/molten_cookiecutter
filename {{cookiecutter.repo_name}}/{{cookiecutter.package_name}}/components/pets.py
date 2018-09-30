from enum import Enum

from sqlalchemy import CheckConstraint, Column, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.exc import IntegrityError

from ..models import Manager, Model


class Species(Enum):
    Bee = "bee"
    Cat = "cat"
    Dog = "dog"
    Turtle = "turtle"


class Pet(Model):
    id = Column(Integer, primary_key=True)
    species = Column(ENUM(Species, name="pet_species"), nullable=False)
    name = Column(String, nullable=False, unique=True)
    age = Column(Integer, nullable=False)

    __tablename__ = "pets"
    __table_args__ = (
        CheckConstraint("age >= 0 and age <= 120"),
    )


class PetError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class PetNameTaken(PetError):
    pass


class PetManager(Manager):
    def insert(self, pet):
        try:
            self.session.add(pet)
            self.session.flush()
            return pet
        except IntegrityError:
            raise PetNameTaken(f"you already have a pet named {pet.name!r}!")

    def delete_by_id(self, pet_id):
        self.session.query(Pet).filter_by(id=pet_id).delete()

    def find_all(self):
        return self.session.query(Pet).all()

    def find_by_id(self, pet_id):
        return self.session.query(Pet).get(id=pet_id)
