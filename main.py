import os
import database
from time import sleep
from dieta import Alimento, Refeicao, Meta, Usuario

# --- BANCO DE DADOS  ---
database.criar_tabelas()
biblioteca_alimentos = database.carregar_todos_alimentos()
lista_usuarios = database.carregar_todos_usuarios()


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPressione Enter para continuar...")

def obter_input_numerico(prompt: str, tipo_numero=float):
    while True:
        try:

            entrada = input(prompt)

            numero = tipo_numero(entrada)

            return numero
        except ValueError:
            print(f"Erro: Entrada inválida. Por favor, digite um número válido.")

def cadastrar_alimento():
    limpar_tela()
    print("--- Cadastro de Novo Alimento ---")
    nome = input("Nome do alimento: ")
    calorias = obter_input_numerico("Calorias por 100g: ")
    proteinas = obter_input_numerico("Proteínas por 100g: ")
    carboidratos = obter_input_numerico("Carboidratos por 100g: ")
    gordura = obter_input_numerico("Gorduras por 100g: ")

    novo_alimento = Alimento(nome, calorias, proteinas, carboidratos, gordura)
    biblioteca_alimentos.append(novo_alimento)
    database.salvar_alimento(novo_alimento)
        
    print(f"\nAlimento '{nome}' cadastrado com sucesso!")
    pausar()

def cadastrar_usuario():
    limpar_tela()
    print("--- Cadastro de Novo Usuário ---")
    nome = input("Nome do usuário: ")

    while True:
        genero = input("Sexo (M/F): ").upper() 
        if genero in ['M', 'F']:
            break
        else:
            print("Erro: Entrada inválida. Por favor, digite apenas M ou F.")

    idade = obter_input_numerico("Idade: ", tipo_numero=int)
    peso = obter_input_numerico("Peso (kg): ")
    altura = obter_input_numerico("Altura (cm): ")
    while True:
        objetivo = input("Qual o seu objetivo (Ex: Emagrecer, Manter ou Ganhar Massa)? ").upper()
        if objetivo in ["EMAGRECER", "MANTER", "GANHAR MASSA"]:
            break
        else:
            print("Erro: Entrada inválida. Por favor, digite corretamente seu objetivo")

    novo_usuario = Usuario(nome, genero, idade, peso, altura, objetivo)
    
    lista_usuarios.append(novo_usuario)
    database.salvar_usuario(novo_usuario)
    
    print(f"\nUsuário '{nome}' cadastrado com sucesso!")
    pausar()

def selecionar_item(lista, tipo_item="item"):
    """Função genérica para exibir uma lista e permitir que o usuário selecione um item."""
    if not lista:
        print(f"Nenhum {tipo_item} cadastrado.")
        return None
    
    for i, item in enumerate(lista):
        print(f"{i + 1}. {item.nome}")
    
    while True:
        try:
            escolha = int(input(f"Escolha o número do {tipo_item}: "))
            if 1 <= escolha <= len(lista):
                return lista[escolha - 1]
            else:
                print("Número inválido.")
        except ValueError:
            print("Por favor, digite um número.")

def registrar_refeicao():
    limpar_tela()
    print("--- Registrar Nova Refeição ---")
    
    print("Selecione o usuário:")
    usuario_selecionado = selecionar_item(lista_usuarios, "usuário")
    if not usuario_selecionado:
        pausar()
        return

    data = input("Digite a data da refeição (ex: 22-08-2025): ")
    nome_refeicao = input("Qual o nome da refeição (ex: Café da Manhã, Almoço)? ")
    
    refeicao = Refeicao(nome_refeicao)

    while True:
        limpar_tela()
        print(f"Adicionando alimentos para '{nome_refeicao}' de {usuario_selecionado.nome}")
        print("\nSelecione um alimento da biblioteca:")
        
        alimento_selecionado = selecionar_item(biblioteca_alimentos, "alimento")
        if not alimento_selecionado:
            pausar()
            break
        
        try:
            quantidade = float(input(f"Digite a quantidade de '{alimento_selecionado.nome}' em gramas: "))
            refeicao.add_alimentos(alimento_selecionado, quantidade)
        except ValueError:
            print("Quantidade inválida. Por favor, digite um número.")
            sleep(2)
        
        continuar = input("Deseja adicionar outro alimento a esta refeição? (s/n): ").lower()
        if continuar != 's':
            break

    usuario_selecionado.registrar_refeicao(refeicao, data)
    pausar()

def ver_resumo_diario():
    limpar_tela()
    print("--- Ver Resumo Diário ---")
    
    print("Selecione o usuário:")
    usuario_selecionado = selecionar_item(lista_usuarios, "usuário")
    if not usuario_selecionado:
        pausar()
        return

    data = input("Digite a data que deseja ver o resumo (ex: 22-08-2025): ")
    
    usuario_selecionado.exibir_resumo_diario(data)
    pausar()

def calcular_tmb_get():
    limpar_tela()
    print("--- Calcular Taxa Metabólica Basal e Gasto Energético ---")
    
    print("\nSelecione o usuário para o qual deseja calcular as métricas:")
    usuario_selecionado = selecionar_item(lista_usuarios, "usuário")
    
    if not usuario_selecionado:
        pausar()
        return

    limpar_tela()
    print(f"Calculando para: {usuario_selecionado.nome}")
    print("\nSelecione o nível de atividade física:")
    print("1. Sedentário (pouco ou nenhum exercício)")
    print("2. Levemente Ativo (exercício leve 1-2 dias/semana)")
    print("3. Moderadamente Ativo (exercício moderado 3-5 dias/semana)")
    print("4. Muito Ativo (exercício pesado 6 dias/semana)")
    print("5. Extremamente Ativo (exercício muito pesado, trabalho físico, 7 dias/semana)")

    fatores_atividade = {
        '1': 1.2,
        '2': 1.375,
        '3': 1.55,
        '4': 1.725,
        '5': 1.9
    }

    while True:
        escolha = input(">> ")
        if escolha in fatores_atividade:
            fator_selecionado = fatores_atividade[escolha]
            break
        else:
            print("Erro: Opção inválida. Digite um número de 1 a 5.")

    metricas = usuario_selecionado.calcular_metricas_energeticas(fator_selecionado)
    
    limpar_tela()
    print("\n" + "="*30)
    print(f"RESULTADOS PARA {usuario_selecionado.nome.upper()}")
    print("="*30)
    print(f"Taxa Metabólica Basal (TMB): {metricas['tmb']:.2f} kcal por dia.")
    print(f"\nGasto Energético Total (GET): {metricas['get']:.2f} kcal por dia.")
    print("="*30)

    get_calculado = metricas['get']
    objetivo_usuario = usuario_selecionado.objetivo.lower() 
    meta_sugerida = 0

    if "emagrecer" in objetivo_usuario:
        meta_sugerida = get_calculado * 0.85
        print(f"\nPara o objetivo de emagrecer, a meta sugerida é 85% do GET.")
    elif "ganhar" in objetivo_usuario:
        meta_sugerida = get_calculado * 1.15
        print(f"\nPara o objetivo de ganhar massa, a meta sugerida é 115% do GET.")
    elif "manter" in objetivo_usuario:
        meta_sugerida = get_calculado
        print(f"\nPara o objetivo de manter o peso, a meta sugerida é 100% do GET.")

    if meta_sugerida > 0:
        print(f"Meta de calorias calculada: {meta_sugerida:.2f} kcal")
        
        confirmar = input(f"Deseja definir esta meta para {usuario_selecionado.nome}? (s/n): ").lower()
        if confirmar == 's':
            nova_meta = Meta(calorias=meta_sugerida)
            usuario_selecionado.definir_meta(nova_meta)
    
    pausar()


def exibir_menu_principal():
    limpar_tela()
    print("===== CONTROLE DE DIETA  =====")
    print("\nEscolha uma opção:")
    print("1. Cadastrar novo usuário")
    print("2. Cadastrar novo alimento")
    print("3. Registrar uma refeição")
    print("4. Calcular Taxa Met. Basal e Gasto Energético")
    print("5. Ver resumo diário")
    print("6. Sair")
    return input(">> ")

def main():
    
    while True:
        escolha = exibir_menu_principal()

        if escolha == '1':
            cadastrar_usuario()
        elif escolha == '2':
            cadastrar_alimento()
        elif escolha == '3':
            registrar_refeicao()
        elif escolha == '4':
            calcular_tmb_get()
        elif escolha == '5':
            ver_resumo_diario()
        elif escolha == '6':
            print("Obrigado por usar o programa.")
            sleep(2)
            limpar_tela()
            break
        else:
            print("Opção inválida! Tente novamente.")
            sleep(2)


if __name__ == "__main__":
    main()