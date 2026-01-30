import json
from datetime import datetime
import os

#*  FUNÇÕES DE SISTEMA (BANCO DE DADOS) 

def carregar_dados():
    try:
        with open('progresso.json', 'r') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se não existir, retorna a estrutura inicial do Growth Tracker
        return {'metas': {}, 'historico': {}}

def salvar_dados(dados):
    # Usamos 'w' para sobrescrever o arquivo com as novas informações
    with open('progresso.json', 'w') as f:
        json.dump(dados, f, indent=4)
    print('💾 Dados salvos com sucesso!')

def historico(xp_total):
    #? Pega a data de hoje no forato dia/mmes/ano
    data_hoje = datetime.now().strftime('%d/%m/%y')

    #? Adiciona ao nosso histórico
    dados_do_app['historico'][data_hoje] = xp_total

    #? Salva no arquivo .json para não perder
    salvar_dados(dados_do_app)
    print(f'📅 Progresso de {data_hoje} arquivado!')



#* --- FUNÇÕES DE USUÁRIO ---

def adicionar_metas(): 
    nome = input('Qual é a meta? ')
    while True:
        try:
            valor = int(input(f'Quanto de XP vale {nome}? '))
            break 
        except ValueError:
            print('❌ Erro: digite apenas números inteiros para o valor do xp')
            
    metas[nome] = valor
    
    #? Atualiza o dicionário principal e salva no arquivo
    dados_do_app['metas'] = metas
    salvar_dados(dados_do_app)
    
    print(f"✅ Meta '{nome}' adicionada com sucesso!")

def remover_metas():
    while True:
        if not metas:
            print('📭 Não há metas cadastradas para remover.')
            break
            
        remover = input('Qual meta deseja remover? ')
        if remover in metas:
            metas.pop(remover)
            
            #? Atualiza o dicionário principal e salva
            dados_do_app['metas'] = metas
            salvar_dados(dados_do_app)
            
            print(f'🗑️ {remover} removida!')
            break
        else: 
            print('⚠️ Essa meta não existe.')
            usuario = input('Deseja tentar remover outra? (s/n) ').strip().upper()
            if usuario == 'N':
                break
        input("\nPressione Enter para voltar ao menu...")
        break

                                                              
def executar_cheklist():
    print(f'\n--- INICIANDO CHECKLIST ---')
    xp_do_dia = 0

    #? fazendo pergunta de s/n baseado nas metas 
    for nome_metas, valor_xp in metas.items():
        resposta = input(f'Concluiu {nome_metas} {valor_xp} XP ? (s/n)').strip().upper()
        if resposta == 'S':
            xp_do_dia += valor_xp

    #? Calcula a porcentagem dinamica (Soma das metas cadatradas)
    metas_100_porcento = sum(metas.values())

    if metas_100_porcento > 0:
        porcentagem = (xp_do_dia / metas_100_porcento) * 100
    else:
        porcentagem = 0
    print(f'\n📊 Resultado Final: {xp_do_dia} XP ({porcentagem:.1f}%)')

    #? da o feefback de status

    if porcentagem >= 110:
        print('🚀 STATUS: FOCO TOTAL!')
    elif porcentagem >= 80:
        print('✅ STATUS: SEMANA ÓTIMA')
    
    input("\nPressione Enter para voltar ao menu...")
    
    

    

    #? SALVA NO HISTÓRICO COM A DATA
    
    historico(xp_do_dia)
    return

def exibir_historico():
    print('\n--- SEU PROGRESSo ---')
    historico_salvo = dados_do_app['historico']

    if not historico_salvo:
        print('📭 Nenhum dado registrado ainda.')
        return
    for data, xp in historico_salvo.items():
        metas_100 = sum(metas.values())
        if metas_100 > 0:
            porcentagem = (xp / metas_100) * 100
        else:
            porcentagem = 0
        
        total_simbolos = 10
        progresso_simbolos = int(porcentagem / 10)
        
        #? 2. Criando a barra com símbolos simples
        #? Se passar de 10, limitei a 10 para não quebrar o layout
        barra = "#" * min(progresso_simbolos, total_simbolos)
        vazio = "-" * (total_simbolos - len(barra))

        #? 3. Adiciona um efeito de "fogo" se passar de 100%
        bonus = " 🔥" if porcentagem > 100 else ""

        print(f"📅 {data} | [{barra}{vazio}] {porcentagem:.0f}% ({xp} XP){bonus}")

    input("\nPressione Enter para voltar ao menu...")
    
        

def exibir_metas():
    print('\n--- 🎯 MINHAS METAS ATUAIS ---')

    if not metas:
        print('📭 Nenhuma meta cadastrada ainda.')
        return
    
    #? Calcula o total de xp possivel 
    total_possivel = sum(metas.values())
    
    #? Loop para mostrar cada meta e seu valor
    for nome, valor in metas.items():
        print(f"• {nome}: {valor} XP")


    print(f"\n💎 Total de XP do dia: {total_possivel} XP")
    input("\nPressione Enter para voltar ao menu...")
    return

    



#* --- INICIALIZAÇÃO ---

# Carregamos os dados uma única vez no início
dados_do_app = carregar_dados()
# Criamos um atalho para as metas para facilitar o uso
metas = dados_do_app['metas']



#? loop inicial 

while True:
    #* Pra limpar o terminal 
    os.system('cls' if os.name == 'nt' else 'clear')
 
    print('\n--- GROWTH TRACKER ---')
    print('1. Iniciar Dia (Checklist)')
    print('2. Adicionar Meta')
    print('3. Remover Meta')
    print('4. Exibir Historico')
    print('5. Exibir Metas ')
    print('6. Sair')
    
    try:
        user = int(input('\nDigite o numero da opção desejada: '))
    except ValueError:
        print('❌ Erro: Digite apenas um dos numeros 1,2,3,4,5,6')

    permitido = [1, 2, 3 ,4,5,6]
    if user not in permitido: #? Not in pra falar não tem no... que seria não tem no permitido 
        print('⚠️ Opção não encontrada. Tente novamente. ')
        continue

    elif user == 1: 
        executar_cheklist()
    
    elif user == 2:
        adicionar_metas()

    elif user == 3:
        remover_metas()

    elif user == 4:
        exibir_historico()
    
    elif user == 5:
        exibir_metas()

    elif user == 6:
        print('Encerrando o GROWTH TRACKER')
        input("Pressione Enter para fechar...")
        break

