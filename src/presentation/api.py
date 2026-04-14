import json
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from src.application.use_cases import RegisterOwnerUseCase, RegisterPetUseCase
from src.domain.repositories import OwnerRepository, PetRepository
import dataclasses
import os

class WebAPI:
    """Capa de Presentación Web: Expone los casos de uso a través del protocolo HTTP."""
    
    def __init__(self, app: Flask, register_owner: RegisterOwnerUseCase, register_pet: RegisterPetUseCase, 
                 owner_repo: OwnerRepository, pet_repo: PetRepository):
        self.app = app
        CORS(self.app) # PERMITE QUE CUALQUIER ARCHIVO HTML SE CONECTE POR CORS
        self.register_owner = register_owner
        self.register_pet = register_pet
        
        # Necesitaremos los repositorios simplemente para los GET (lectura)
        self.owner_repo = owner_repo
        self.pet_repo = pet_repo
        
        self.setup_routes()

    def setup_routes(self):
        
        # --- RUTAS DE LA API --- #
        
        @self.app.route('/api/owners', methods=['GET'])
        def get_owners():
            owners = self.owner_repo.get_all()
            return jsonify([dataclasses.asdict(o) for o in owners])

        @self.app.route('/api/owners', methods=['POST'])
        def create_owner():
            data = request.json
            try:
                owner = self.register_owner.execute(
                    name=data.get('name', ''),
                    residence=data.get('residence', ''),
                    phone=data.get('phone', '')
                )
                return jsonify(dataclasses.asdict(owner)), 201
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

        @self.app.route('/api/pets', methods=['GET'])
        def get_pets():
            pets = self.pet_repo.get_all()
            return jsonify([dataclasses.asdict(p) for p in pets])

        @self.app.route('/api/pets', methods=['POST'])
        def create_pet():
            data = request.json
            try:
                pet = self.register_pet.execute(
                    owner_id=int(data.get('owner_id', 0)),
                    breed=data.get('breed', ''),
                    weight=float(data.get('weight', 0)),
                    color=data.get('color', ''),
                    age=int(data.get('age', 0)),
                    size=data.get('size', '')
                )
                return jsonify(dataclasses.asdict(pet)), 201
            except Exception as e: # Captura errores como "dueño no existe"
                return jsonify({"error": str(e)}), 400
                
        # --- RUTAS FRONTEND (Servir Archivos HTML/CSS/JS) --- #

        @self.app.route('/')
        def index():
            frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'frontend')
            return send_from_directory(frontend_dir, 'index.html')

        @self.app.route('/<path:filename>')
        def static_files(filename):
            frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'frontend')
            return send_from_directory(frontend_dir, filename)

    def run(self):
        self.app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
