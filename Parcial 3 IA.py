class SistemaInferencia:
    def __init__(self):
        self.hechos = {}
        self.reglas = []
    
    def agregar_hecho(self, proposicion, valor):
        self.hechos[proposicion] = valor
    
    def agregar_regla(self, antecedente, consecuente):
        self.reglas.append((antecedente, consecuente))
    
    def inferir(self):
        cambio = True
        while cambio:
            cambio = False
            for antecedente, consecuente in self.reglas:
                # Verificar si se cumple el antecedente
                if self.evaluar(antecedente):
                    # Si el consecuente no está o es False, actualizar
                    prop, valor = consecuente
                    if prop not in self.hechos or not self.hechos[prop]:
                        self.hechos[prop] = valor
                        cambio = True
                        print(f"Regla aplicada: {antecedente} -> {consecuente}")
    
    def evaluar(self, expresion):
        if expresion[0] == 'Y':
            return all(self.evaluar(sub) for sub in expresion[1:])
        elif expresion[0] == 'O':
            return any(self.evaluar(sub) for sub in expresion[1:])
        elif expresion[0] == 'NO':
            return not self.evaluar(expresion[1])
        else:
            # Es una proposición simple
            return self.hechos.get(expresion, False)
    
    def mostrar_estado(self):
        print("Estado actual:")
        for prop, valor in self.hechos.items():
            print(f"  {prop}: {valor}")
        print()

# Configurar el sistema con las reglas del problema
def configurar_sistema():
    sistema = SistemaInferencia()
    
    # Reglas:
    # 1. Si hay humo, entonces puede haber fuego: H -> F
    sistema.agregar_regla('H', ('F', True))
    # 2. Si hay fuego, entonces la alarma debe sonar: F -> A
    sistema.agregar_regla('F', ('A', True))
    # 3. Si hay alarma, entonces evacuar: A -> E
    sistema.agregar_regla('A', ('E', True))
    
    return sistema

# Escenario 1: Con humo
print("=== ESCENARIO 1: Con humo ===")
sistema1 = configurar_sistema()
sistema1.agregar_hecho('H', True)  # Hay humo
sistema1.mostrar_estado()
sistema1.inferir()
sistema1.mostrar_estado()

print("\n" + "="*50 + "\n")

# Escenario 2: Sin humo
print("=== ESCENARIO 2: Sin humo ===")
sistema2 = configurar_sistema()
sistema2.agregar_hecho('H', False)  # No hay humo
sistema2.mostrar_estado()
sistema2.inferir()
sistema2.mostrar_estado()