from src.domain.models import Owner, Pet
from src.domain.repositories import OwnerRepository, PetRepository

class RegisterOwnerUseCase:
    def __init__(self, owner_repository: OwnerRepository):
        self.owner_repository = owner_repository

    def execute(self, name: str, residence: str, phone: str) -> Owner:
        owner = Owner(id=None, name=name, residence=residence, phone=phone)
        
        if not owner.is_valid():
            raise ValueError(f"Los datos del dueño '{name}' no son válidos.")
            
        return self.owner_repository.save(owner)

class RegisterPetUseCase:
    def __init__(self, pet_repository: PetRepository, owner_repository: OwnerRepository):
        self.pet_repository = pet_repository
        self.owner_repository = owner_repository

    def execute(self, owner_id: int, breed: str, weight: float, color: str, age: int, size: str) -> Pet:
        # Verificar que el dueño exista antes de asignarle una mascota
        owner = self.owner_repository.get_by_id(owner_id)
        if not owner:
            raise ValueError(f"No existe ningún dueño con el ID {owner_id}")
            
        pet = Pet(
            id=None,
            owner_id=owner_id,
            breed=breed,
            weight=weight,
            color=color,
            age=age,
            size=size
        )

        if not pet.is_valid():
            raise ValueError("Los datos de la mascota no son válidos.")

        return self.pet_repository.save(pet)
