class Alimento:
    def __init__(self,nome,calorias,proteinas,carboidratos,gordura):
        self.nome = nome
        self.calorias_por_100g = calorias
        self.proteinas = proteinas
        self.carboidratos = carboidratos
        self.gordura = gordura

    def calcular_calorias(self, quantidade):
        calorias = (self.calorias_por_100g / 100) * quantidade
        return calorias

    def __repr__(self):
        return f"Alimento(Nome='{self.nome}', P/100g: C={self.carboidratos}g, P={self.proteinas}g, G={self.gordura}g)"
    
class Refeicao:
    def __init__(self,nome):
        self.nome = nome
        self.alimentos_consumidos = []

    def add_alimentos(self, alimento:Alimento, quantidade):
        if isinstance(alimento, Alimento):
            self.alimentos_consumidos.append((alimento, quantidade))
            print(f"{alimento.nome} ({quantidade}g) adicionado ao {self.nome}.")
        else:
            print("Erro: Apenas objetos da classe Alimento podem ser adicionados.")

    def calcular_total_calorias(self):
        total_calorias = 0
        for alimento, quantidade in self.alimentos_consumidos:
            total_calorias += alimento.calcular_calorias(quantidade)
        return total_calorias
        
    def __repr__(self):
        return f"Refeicao(Nome='{self.nome}', Itens={len(self.alimentos_consumidos)})"
    

class Meta:
    """
    Uma classe simples para armazenar os dados da meta de um usuário.
    """
    def __init__(self, calorias):
        self.calorias = calorias

    def __repr__(self):
        return f"Meta(Calorias={self.calorias} kcal)"

class Usuario:
    def __init__(self,nome,genero,idade,peso,altura,objetivo):
        self.nome = nome
        self.genero = genero
        self.idade = idade
        self.peso = peso
        self.altura = altura
        self.objetivo = objetivo
        self.meta = None
        self.registros = {}

    def definir_meta(self, meta:Meta):
        if isinstance(meta, Meta):
            self.meta = meta
            print(f"Meta definida para {self.nome}: {self.meta}")
        else:
            print("Erro: a meta deve ser um objeto Meta.")

    def registrar_refeicao(self, refeicao: Refeicao, data):
        """
        Registra uma refeição completa em uma data específica.
        """
        if data not in self.registros:
            self.registros[data] = [] 
        
        self.registros[data].append(refeicao)
        print(f"Refeição '{refeicao.nome}' registrada para {self.nome} no dia {data}.")

    def exibir_resumo_diario(self, data):
        """
        Calcula e exibe o total consumido em um dia e compara com a meta.
        """
        if data not in self.registros:
            print(f"Nenhum registro encontrado para o dia {data}.")
            return

        refeicoes_do_dia = self.registros[data]
        total_calorias_dia = sum(r.calcular_total_calorias() for r in refeicoes_do_dia)

        print(f"\n--- Resumo do dia {data} para {self.nome} ---")
        for refeicao in refeicoes_do_dia:
            print(f"- {refeicao.nome}: {refeicao.calcular_total_calorias():.2f} kcal")
        
        print(f"\nTotal Consumido: {total_calorias_dia:.2f} kcal")
        
        if self.meta:
            print(f"Meta de Calorias: {self.meta.calorias:.2f} kcal")
            restante = self.meta.calorias - total_calorias_dia
            if restante >= 0:
                print(f"Calorias restantes: {restante:.2f} kcal")
            else:
                print(f"Você excedeu a meta em {-restante:.2f} kcal")
        else:
            print("Nenhuma meta definida para comparação.")

    def calcular_metricas_energeticas(self, fator_atividade: float):
        """
        Calcula a TMB (Mifflin-St Jeor) e o GET do usuário.

        """
        # Fórmula de Mifflin-St Jeor
        if self.genero == 'M':
            # TMB para homens
            tmb = (10 * self.peso) + (6.25 * self.altura) - (5 * self.idade) + 5
        else: 
            # TMB para mulheres
            tmb = (10 * self.peso) + (6.25 * self.altura) - (5 * self.idade) - 161

        # Gasto Energético Total (GET) = TMB * Fator de Atividade
        gasto_energetico_total = tmb * fator_atividade

        return {'tmb': tmb, 'get': gasto_energetico_total}