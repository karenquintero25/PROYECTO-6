import sys
import os
from flask import Flask

# Asegurar que el directorio raíz está en el path para poder importar src.*
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.infrastructure.sqlite_repository import SQLiteOwnerRepository, SQLitePetRepository, SQLiteAdoptionRepository, SQLiteReportRepository
from src.application.use_cases import RegisterOwnerUseCase, RegisterPetUseCase, RegisterAdoptionUseCase, RegisterReportUseCase
from src.presentation.api import WebAPI

def main():
    # 1. Instanciar Infraestructura (Conexión Real a Base de Datos SQLite)
    owner_repo = SQLiteOwnerRepository(db_path="veterinaria.db")
    pet_repo = SQLitePetRepository(db_path="veterinaria.db")
    adoption_repo = SQLiteAdoptionRepository(db_path="veterinaria.db")
    report_repo = SQLiteReportRepository(db_path="veterinaria.db")
    
    # 2. Instanciar Aplicación (Lógica de Negocio Pura)
    register_owner_uc = RegisterOwnerUseCase(owner_repository=owner_repo)
    register_pet_uc = RegisterPetUseCase(pet_repository=pet_repo, owner_repository=owner_repo)
    register_adoption_uc = RegisterAdoptionUseCase(adoption_repository=adoption_repo, pet_repository=pet_repo)
    register_report_uc = RegisterReportUseCase(report_repository=report_repo)
    
    # 3. Instanciar Servidor Flask (El núcleo)
    app = Flask(__name__)
    
    # 4. Instanciar Capa de Presentación (Inyectando Casos de Uso y Rutas)
    ui = WebAPI(
        app=app,
        register_owner=register_owner_uc,
        register_pet=register_pet_uc,
        owner_repo=owner_repo, # Usado solo para listar (GET)
        pet_repo=pet_repo,     # Usado solo para listar (GET)
        register_adoption=register_adoption_uc,
        register_report=register_report_uc,
        adoption_repo=adoption_repo,
        report_repo=report_repo
    )
    
    # 5. Iniciar la magia web en el puerto 5000
    print("Iniciando Clínica Veterinaria Web App... Entra a http://localhost:5000")
    ui.run()

if __name__ == "__main__":
    main()
