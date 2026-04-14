import sqlite3
from typing import List, Optional
from src.domain.models import Owner, Pet
from src.domain.repositories import OwnerRepository, PetRepository

class SQLiteOwnerRepository(OwnerRepository):
    def __init__(self, db_path: str = "veterinaria.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS owners (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    residence TEXT NOT NULL,
                    phone TEXT NOT NULL
                )
            ''')

    def save(self, owner: Owner) -> Owner:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if owner.id is None:
                cursor.execute(
                    "INSERT INTO owners (name, residence, phone) VALUES (?, ?, ?)",
                    (owner.name, owner.residence, owner.phone)
                )
                owner.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE owners SET name=?, residence=?, phone=? WHERE id=?",
                    (owner.name, owner.residence, owner.phone, owner.id)
                )
            conn.commit()
        return owner

    def get_by_id(self, owner_id: int) -> Optional[Owner]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, residence, phone FROM owners WHERE id=?", (owner_id,))
            row = cursor.fetchone()
            if row:
                return Owner(id=row[0], name=row[1], residence=row[2], phone=row[3])
        return None

    def get_all(self) -> List[Owner]:
        owners = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, residence, phone FROM owners")
            for row in cursor.fetchall():
                owners.append(Owner(id=row[0], name=row[1], residence=row[2], phone=row[3]))
        return owners


class SQLitePetRepository(PetRepository):
    def __init__(self, db_path: str = "veterinaria.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS pets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_id INTEGER NOT NULL,
                    breed TEXT NOT NULL,
                    weight REAL NOT NULL,
                    color TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    size TEXT NOT NULL,
                    FOREIGN KEY(owner_id) REFERENCES owners(id)
                )
            ''')

    def save(self, pet: Pet) -> Pet:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if pet.id is None:
                cursor.execute(
                    "INSERT INTO pets (owner_id, breed, weight, color, age, size) VALUES (?, ?, ?, ?, ?, ?)",
                    (pet.owner_id, pet.breed, pet.weight, pet.color, pet.age, pet.size)
                )
                pet.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE pets SET owner_id=?, breed=?, weight=?, color=?, age=?, size=? WHERE id=?",
                    (pet.owner_id, pet.breed, pet.weight, pet.color, pet.age, pet.size, pet.id)
                )
            conn.commit()
        return pet

    def get_by_owner_id(self, owner_id: int) -> List[Pet]:
        pets = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, owner_id, breed, weight, color, age, size FROM pets WHERE owner_id=?", (owner_id,))
            for row in cursor.fetchall():
                pets.append(Pet(
                    id=row[0], owner_id=row[1], breed=row[2], weight=row[3], color=row[4], age=row[5], size=row[6]
                ))
        return pets

    def get_all(self) -> List[Pet]:
        pets = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, owner_id, breed, weight, color, age, size FROM pets")
            for row in cursor.fetchall():
                pets.append(Pet(
                    id=row[0], owner_id=row[1], breed=row[2], weight=row[3], color=row[4], age=row[5], size=row[6]
                ))
        return pets
