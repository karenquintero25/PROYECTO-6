from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Owner, Pet

class OwnerRepository(ABC):
    @abstractmethod
    def save(self, owner: Owner) -> Owner:
        pass

    @abstractmethod
    def get_by_id(self, owner_id: int) -> Optional[Owner]:
        pass

    @abstractmethod
    def get_all(self) -> List[Owner]:
        pass

class PetRepository(ABC):
    @abstractmethod
    def save(self, pet: Pet) -> Pet:
        pass

    @abstractmethod
    def get_by_owner_id(self, owner_id: int) -> List[Pet]:
        pass

    @abstractmethod
    def get_all(self) -> List[Pet]:
        pass
