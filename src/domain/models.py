from dataclasses import dataclass
from typing import Optional

@dataclass
class Owner:
    """Entidad de Dominio: Representa un Dueño de mascota."""
    id: Optional[int]
    name: str
    residence: str
    phone: str
    
    def is_valid(self) -> bool:
        """Regla de negocio: no podemos tener nombres o teléfonos vacíos"""
        return len(self.name.strip()) > 0 and len(self.phone.strip()) > 0

@dataclass
class Pet:
    """Entidad de Dominio: Representa una Mascota vinculada a un Dueño."""
    id: Optional[int]
    owner_id: int
    breed: str
    weight: float
    color: str
    age: int
    size: str

    def is_valid(self) -> bool:
        """Regla de negocio: la mascota debe tener una raza válida y edad >= 0"""
        return len(self.breed.strip()) > 0 and self.age >= 0
