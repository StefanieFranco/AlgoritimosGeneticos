class Vehicle:
    def __init__(self, id, tipo, capacidade_kg, autonomia_km, custo_km):
        self.id = id
        self.tipo = tipo
        self.capacidade_kg = capacidade_kg
        self.autonomia_km = autonomia_km
        self.custo_km = custo_km
        self.rota = []