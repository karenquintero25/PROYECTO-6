from src.application.use_cases import RegisterOwnerUseCase, RegisterPetUseCase

class ConsoleUI:
    def __init__(self, register_owner: RegisterOwnerUseCase, register_pet: RegisterPetUseCase):
        self.register_owner = register_owner
        self.register_pet = register_pet

    def run(self):
        print("--- Sistema de Veterinaria Automático (4 Capas) ---")
        
        while True:
            print("\n1. Registrar Dueño")
            print("2. Registrar Mascota")
            print("3. Salir")
            opcion = input("Elige una opción: ")

            if opcion == '1':
                print("\n-- Registro de Dueño --")
                nombre = input("Nombre completo: ")
                residencia = input("Dirección de residencia: ")
                telefono = input("Número de teléfono: ")
                
                try:
                    owner = self.register_owner.execute(nombre, residencia, telefono)
                    print(f"[EXITO] Debido registrado con ID: {owner.id}")
                except Exception as e:
                    print(f"[ERROR] {e}")

            elif opcion == '2':
                print("\n-- Registro de Mascota --")
                try:
                    owner_id = int(input("ID del Dueño: "))
                except ValueError:
                    print("[ERROR] El ID del dueño debe ser un número entero.")
                    continue
                    
                raza = input("Raza de la mascota: ")
                
                try:
                    peso = float(input("Peso (kg): "))
                    edad = int(input("Edad (años): "))
                except ValueError:
                    print("[ERROR] Peso y edad deben ser números.")
                    continue

                color = input("Color: ")
                tamano = input("Tamaño (P, M, G): ")

                try:
                    pet = self.register_pet.execute(owner_id, raza, peso, color, edad, tamano)
                    print(f"[EXITO] Mascota registrada con ID: {pet.id} para el dueño {owner_id}")
                except Exception as e:
                    print(f"[ERROR] {e}")

            elif opcion == '3':
                print("Saliendo del sistema...")
                break
            else:
                print("Lamentablemente, opción no válida.")
