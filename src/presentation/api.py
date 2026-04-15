import json
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from src.application.use_cases import RegisterOwnerUseCase, RegisterPetUseCase, RegisterAdoptionUseCase, RegisterReportUseCase
from src.domain.repositories import OwnerRepository, PetRepository, AdoptionRepository, ReportRepository
import dataclasses
import os

class WebAPI:
    """Capa de Presentación Web: Expone los casos de uso a través del protocolo HTTP."""
    
    def __init__(self, app: Flask, register_owner: RegisterOwnerUseCase, register_pet: RegisterPetUseCase, 
                 owner_repo: OwnerRepository, pet_repo: PetRepository,
                 register_adoption: RegisterAdoptionUseCase = None, register_report: RegisterReportUseCase = None,
                 adoption_repo: AdoptionRepository = None, report_repo: ReportRepository = None):
        self.app = app
        CORS(self.app) # PERMITE QUE CUALQUIER ARCHIVO HTML SE CONECTE POR CORS
        self.register_owner = register_owner
        self.register_pet = register_pet
        
        # Necesitaremos los repositorios simplemente para los GET (lectura)
        self.owner_repo = owner_repo
        self.pet_repo = pet_repo
        self.register_adoption = register_adoption
        self.register_report = register_report
        self.adoption_repo = adoption_repo
        self.report_repo = report_repo
        
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

        @self.app.route('/api/adoptions', methods=['GET'])
        def get_adoptions():
            if not self.adoption_repo: return jsonify([])
            adoptions = self.adoption_repo.get_all()
            return jsonify([dataclasses.asdict(a) for a in adoptions])

        @self.app.route('/api/adoptions', methods=['POST'])
        def create_adoption():
            data = request.json
            try:
                if not self.register_adoption: raise Exception("Not configured")
                adoption = self.register_adoption.execute(
                    pet_id=int(data.get('pet_id', 0)),
                    adopter_name=data.get('adopter_name', ''),
                    contact=data.get('contact', '')
                )
                return jsonify(dataclasses.asdict(adoption)), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 400

        @self.app.route('/api/reports', methods=['GET'])
        def get_reports():
            if not self.report_repo: return jsonify([])
            reports = self.report_repo.get_all()
            return jsonify([dataclasses.asdict(r) for r in reports])

        @self.app.route('/api/reports', methods=['POST'])
        def create_report():
            data = request.json
            try:
                if not self.register_report: raise Exception("Not configured")
                report = self.register_report.execute(
                    report_type=data.get('report_type', ''),
                    description=data.get('description', ''),
                    location=data.get('location', ''),
                    color=data.get('color', ''),
                    size=data.get('size', ''),
                    contact=data.get('contact', '')
                )
                return jsonify(dataclasses.asdict(report)), 201
            except Exception as e:
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
