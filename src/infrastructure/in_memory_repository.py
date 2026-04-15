from typing import List, Optional
from src.domain.models import Owner, Pet, Adoption, Report
from src.domain.repositories import OwnerRepository, PetRepository, AdoptionRepository, ReportRepository

class InMemoryOwnerRepository(OwnerRepository):
    def __init__(self):
        self._db: List[Owner] = []
        self._current_id = 1

    def save(self, owner: Owner) -> Owner:
        if owner.id is None:
            owner.id = self._current_id
            self._current_id += 1
        self._db.append(owner)
        return owner

    def get_by_id(self, owner_id: int) -> Optional[Owner]:
        return next((o for o in self._db if o.id == owner_id), None)

    def get_all(self) -> List[Owner]:
        return list(self._db)

class InMemoryPetRepository(PetRepository):
    def __init__(self):
        self._db: List[Pet] = []
        self._current_id = 1

    def save(self, pet: Pet) -> Pet:
        if pet.id is None:
            pet.id = self._current_id
            self._current_id += 1
        self._db.append(pet)
        return pet

    def get_by_owner_id(self, owner_id: int) -> List[Pet]:
        return [p for p in self._db if p.owner_id == owner_id]

    def get_all(self) -> List[Pet]:
        return list(self._db)

class InMemoryAdoptionRepository(AdoptionRepository):
    def __init__(self):
        self._db: List[Adoption] = []
        self._current_id = 1

    def save(self, adoption: Adoption) -> Adoption:
        if adoption.id is None:
            adoption.id = self._current_id
            self._current_id += 1
        self._db.append(adoption)
        return adoption

    def get_all(self) -> List[Adoption]:
        return list(self._db)

class InMemoryReportRepository(ReportRepository):
    def __init__(self):
        self._db: List[Report] = []
        self._current_id = 1

    def save(self, report: Report) -> Report:
        if report.id is None:
            report.id = self._current_id
            self._current_id += 1
        self._db.append(report)
        return report

    def get_all(self) -> List[Report]:
        return list(self._db)
