import sqlite3
from typing import List, Optional
from src.domain.models import Owner, Pet, Adoption, Report
from src.domain.repositories import OwnerRepository, PetRepository, AdoptionRepository, ReportRepository

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

class SQLiteAdoptionRepository(AdoptionRepository):
    def __init__(self, db_path: str = "veterinaria.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS adoptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pet_id INTEGER NOT NULL,
                    adopter_name TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    FOREIGN KEY(pet_id) REFERENCES pets(id)
                )
            ''')

    def save(self, adoption: Adoption) -> Adoption:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if adoption.id is None:
                cursor.execute(
                    "INSERT INTO adoptions (pet_id, adopter_name, contact) VALUES (?, ?, ?)",
                    (adoption.pet_id, adoption.adopter_name, adoption.contact)
                )
                adoption.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE adoptions SET pet_id=?, adopter_name=?, contact=? WHERE id=?",
                    (adoption.pet_id, adoption.adopter_name, adoption.contact, adoption.id)
                )
            conn.commit()
        return adoption

    def get_all(self) -> List[Adoption]:
        adoptions = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, pet_id, adopter_name, contact FROM adoptions")
            for row in cursor.fetchall():
                adoptions.append(Adoption(
                    id=row[0], pet_id=row[1], adopter_name=row[2], contact=row[3]
                ))
        return adoptions

class SQLiteReportRepository(ReportRepository):
    def __init__(self, db_path: str = "veterinaria.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    location TEXT NOT NULL,
                    color TEXT NOT NULL,
                    size TEXT NOT NULL,
                    contact TEXT NOT NULL
                )
            ''')

    def save(self, report: Report) -> Report:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if report.id is None:
                cursor.execute(
                    "INSERT INTO reports (report_type, description, location, color, size, contact) VALUES (?, ?, ?, ?, ?, ?)",
                    (report.report_type, report.description, report.location, report.color, report.size, report.contact)
                )
                report.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE reports SET report_type=?, description=?, location=?, color=?, size=?, contact=? WHERE id=?",
                    (report.report_type, report.description, report.location, report.color, report.size, report.contact, report.id)
                )
            conn.commit()
        return report

    def get_all(self) -> List[Report]:
        reports = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, report_type, description, location, color, size, contact FROM reports")
            for row in cursor.fetchall():
                reports.append(Report(
                    id=row[0], report_type=row[1], description=row[2], location=row[3], color=row[4], size=row[5], contact=row[6]
                ))
        return reports
