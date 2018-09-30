from typing import Tuple

from molten import HTTP_201, HTTP_204, HTTP_400, HTTP_404, HTTPError, Route

from ..components.pets import PetError, PetManager
from .schemas import Pet, PetList


def list_pets(pet_manager: PetManager) -> PetList:
    return PetList([Pet.from_model(pet) for pet in pet_manager.find_all()])


def add_pet(pet: Pet, pet_manager: PetManager) -> Tuple[str, Pet]:
    try:
        return HTTP_201, Pet.from_model(pet_manager.insert(pet.to_model()))
    except PetError as e:
        raise HTTPError(HTTP_400, {"error": str(e)})


def get_pet(pet_id: int, pet_manager: PetManager) -> Pet:
    pet = pet_manager.find_by_id(pet_id)
    if pet is None:
        raise HTTPError(HTTP_404, {"error": f"Pet {pet_id} not found."})
    return Pet.from_model(pet)


def delete_pet(pet_id: int, pet_manager: PetManager) -> Tuple[str, None]:
    pet_manager.delete_by_id(pet_id)
    return HTTP_204, None


routes = [
    Route("/", list_pets),
    Route("/", add_pet, method="POST"),
    Route("/{pet_id}", get_pet),
    Route("/{pet_id}", delete_pet, method="DELETE"),
]
