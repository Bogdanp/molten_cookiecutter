from typing import List, Optional

from molten import FieldValidationError, field, schema

from ..components.pets import Pet as PetModel
from ..components.pets import Species


class SpeciesValidator:
    def validate(self, field, value):
        try:
            Species(value)
        except (TypeError, ValueError) as e:
            raise FieldValidationError(str(e))

        return value


@schema
class Pet:
    id: Optional[int] = field(response_only=True)
    species: str = field(validator=SpeciesValidator())
    name: str
    age: int = field(minimum=0, maximum=120)

    @classmethod
    def from_model(cls, ob):
        return Pet(
            id=ob.id,
            species=ob.species.value,
            name=ob.name,
            age=ob.age,
        )

    def to_model(self):
        return PetModel(
            id=self.id,
            species=Species(self.species),
            name=self.name,
            age=self.age,
        )


@schema
class PetList:
    pets: List[Pet]
