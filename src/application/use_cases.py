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

class RegisterAdoptionUseCase:
    def __init__(self, adoption_repository: 'AdoptionRepository', pet_repository: PetRepository):
        self.adoption_repository = adoption_repository
        self.pet_repository = pet_repository

    def execute(self, pet_id: int, adopter_name: str, contact: str) -> 'Adoption':
        # Verificar que la mascota exista
        pet = next((p for p in self.pet_repository.get_all() if p.id == pet_id), None)
        if not pet:
            raise ValueError(f"No existe ninguna mascota con el ID {pet_id}")
            
        from src.domain.models import Adoption
        adoption = Adoption(
            id=None,
            pet_id=pet_id,
            adopter_name=adopter_name,
            contact=contact
        )

        if not adoption.is_valid():
            raise ValueError("Los datos de la adopción no son válidos.")

        return self.adoption_repository.save(adoption)

class RegisterReportUseCase:
    def __init__(self, report_repository: 'ReportRepository'):
        self.report_repository = report_repository

    def execute(self, report_type: str, description: str, location: str, color: str, size: str, contact: str) -> 'Report':
        from src.domain.models import Report
        report = Report(
            id=None,
            report_type=report_type,
            description=description,
            location=location,
            color=color,
            size=size,
            contact=contact
        )

        if not report.is_valid():
            raise ValueError("Los datos del denuncio no son válidos (descripción y ubicación son requeridas).")

        return self.report_repository.save(report)
