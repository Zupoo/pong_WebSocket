import asyncio
from websockets.asyncio.server import serve
import json
import os


estado_bola = {
    "bola":{
        "bola_x": 400,
        "bola_y": 300,
        "vel_x": 5,
        "vel_y": 3,
        "largura": 20,
        "altura" : 20

        },
    "saque":{
        "sacando": True,
        "sacador": "jogador1"
    }
    # "jogador1":{
    #     "x": 350,
    #     "y": 550,
    #     "largura": 100,
    #     "altura": 20,
    #     "velocidade": 650,
    #     "pontucao": 0
    # }
    # "jogador2":{
    #     "x": 350,
    #     "y": 25,
    #     "largura": 100,
    #     "altura": 20,
    #     "velocidade": 650,
    #     "pontucao": 0
    # }
}

jogadores = {}

id_jogador = 0

# teclas = {'a': 'false', 'd': 'false', 'z':'false'}



async def receber(websocket):   #async def quer dizer q essa funcao pode parar de executar enquanto estiver esperando por algo

    jogador_existente = None
    if len(jogadores) <= 1:
        print(f"Nova conexão! websocket = {websocket}")
        for jogador in jogadores:
            jogador_existente = jogadores[jogador]["nome"]
        if jogador_existente == 'jogador1':
                jogadores[websocket] = {
                    "nome": "jogador2",
                    "x": 350,
                    "y": 20,
                    "largura": 100,
                    "altura": 20,
                    "velocidade": 650,
                    "pontuacao": 0,
                    "movimento" :{"a": False, "d": False, "w": False, "z": False},
                    "teclado" :{}
                }
        else:
            jogadores[websocket] = {
                "nome": "jogador1",
                "x": 350,
                "y": 550,
                "largura": 100,
                "altura": 20,
                "velocidade": 650,
                "pontuacao": 0,
                "movimento" :{"a": False, "d": False, "w": False, "z": False},
                "teclado" :{}

            }

        print(f"O jogador {websocket} acabou de se conectar")
        # estado_jogo["jogador1"] = jogadores[websocket]

        try:
            async for mensagem in websocket: #async for modifica o for pra q ele possa iterar no em um objeto assincrono, o  websocket n é um iterador comum como listas e dicionarios, quer dizer q ele pode ficar esperando por uma nova mensagem. e sempre q tiver uma nova mensagem ele vai rodar o for 
                # print(f"Recebido do {websocket} : {mensagem} (ainda em json)")
                comando = json.loads(mensagem)   #transformando o texto json recebido em um objeto de volta

                if comando["tipo"] == "mensagem":
                    await websocket.send(json.dumps({   #o await aqui serve pra n ficar esperando a mensagem ser enviada , pq ela n vai instantaneao. entao o codigo pode seguir e depois voltar aqui quando a mensagem for enviada
                        "tipo": "mensagem",
                        "texto": (f"Voce enviou: {comando["texto"]} para o servidor") 
                    }))

                    print(f"O Cliente disse: {comando['texto']}")


                elif comando["tipo"] == "movimento":
                    await websocket.send(json.dumps({
                        "tipo": "mensagem",
                        "texto": (f"Voce envou um comando de movimento para o servidor")
                    }))
                    # print(comando)
                    # # print(teclas)
                    # teclas["a"] = comando["a"]
                    # print(teclas)
                    # print(comando)
                    for tecla in comando:
                        # print(tecla)
                        if "a" in tecla:
                            jogadores[websocket]["movimento"]["a"] = comando[tecla]
                        elif "d" in tecla:
                            jogadores[websocket]["movimento"]["d"] = comando[tecla]
                        elif "w" in tecla:
                            jogadores[websocket]["movimento"]["w"] = comando[tecla]
                        elif "z" in tecla:
                            jogadores[websocket]["movimento"]["z"] = comando[tecla]


                        # teclas[tecla] = comando[tecla]
                    # print(teclas)                        
                        # jogadores[websocket]["teclas"][comando] = comando[tecla]

                    # elif comando["d"] == "true":  
                    #     if jogadores[websocket] == "jogador1":
                    #         estado_jogo["jogador1"]["x"] += estado_jogo["jogador1"]["velocidade"] /60
                elif comando["tipo"] == "tecla":
                    print("alou",comando)

                elif comando["tipo"] == "pergunta":
                    print(f"O cliente perguntou {comando['pedido']}")
                    jogadores_conectados = []
                    for usuario_conectado in jogadores:
                        jogadores_conectados.append(jogadores[usuario_conectado])

                    await websocket.send(json.dumps({
                        "tipo" : "jogadores",
                        "jogadores_conectados": jogadores_conectados,
                    }))

                else:
                    print(f"Comando desconhecido, tipo : {comando['tipo']}")            
        finally:
            del jogadores[websocket]
    else:
        print("servidor cheio")            

async def game_loop():
    while True:

        if estado_bola["saque"]["sacando"] == True:
            ##### COLOCANDO VELOCIDADE 0 NA BOLA E POSICIONANDO NO MEIO DO JOGADOR ###
            for jogador in jogadores:
                player = jogadores[jogador]
                if player["nome"] == estado_bola["saque"]["sacador"]: ##### colocando a bola no meio do jogador q esta em estadobola.saque.sacador
                    bola_y = player['y'] - estado_bola["bola"]["altura"]
                    estado_bola["bola"]['bola_x'] = (player['x'] + player["largura"]/2) - estado_bola["bola"]["largura"]/2
                    estado_bola["bola"]["vel_x"] = 0
                    estado_bola["bola"]["vel_y"] = 0
                    if estado_bola["saque"]["sacador"] == 'jogador1': ### posicinando a bola no Y do jogador q ta sacando
                        estado_bola["bola"]["bola_y"] = player["y"] - estado_bola["bola"]["altura"]
                    elif estado_bola["saque"]["sacador"] == 'jogador2':
                        estado_bola["bola"]["bola_y"] = player["y"] + player["altura"]
                    if player["movimento"]["w"] == True:
                        print(player["movimento"]["z"])
                        if player["movimento"]["a"] == True:
                            estado_bola["bola"]["vel_x"] = -5
                        elif player["movimento"]["d"] == True:
                            estado_bola["bola"]["vel_x"] = 5
                        if player["movimento"]["z"] == True:
                            estado_bola["bola"]["vel_y"] = 35
                        else:
                            estado_bola["bola"]["vel_y"] = 10
                        estado_bola["saque"]["sacando"] = False


        else:
            #### RESPONSAVEL POR FAZER O MOVIMENTO DA BOLA e colisao com as paredes 0 800x  0 600y####
            estado_bola["bola"]["bola_x"] += estado_bola["bola"]["vel_x"]
            estado_bola["bola"]["bola_y"] += estado_bola["bola"]["vel_y"]
            if estado_bola["bola"]["bola_x"] <= 0:
                estado_bola["bola"]["vel_x"] *= (-1)
            if estado_bola["bola"]["bola_x"] >= 800 - estado_bola["bola"]["largura"]:
                estado_bola["bola"]["vel_x"] *= (-1)    

            if estado_bola["bola"]["bola_y"] <= 0:
                estado_bola["bola"]["vel_y"] *= (-1)
            if estado_bola["bola"]["bola_y"] >= 600 - estado_bola["bola"]["altura"]:
                estado_bola["bola"]["vel_y"] *= (-1)

            ### COLISAO COM OS PLAYERS ### IA q escreveu uma parte
            for jogador in jogadores:
                player = jogadores[jogador]

                if (
                    estado_bola["bola"]["bola_x"] < player["x"] + player["largura"]
                    and estado_bola["bola"]["bola_x"] + estado_bola["bola"]["largura"] > player["x"]
                    and estado_bola["bola"]["bola_y"] < player["y"] + player["altura"]
                    and estado_bola["bola"]["bola_y"] + estado_bola["bola"]["altura"] > player["y"]
                ):
                    if estado_bola["bola"]["vel_y"] < 0:
                        estado_bola["bola"]["vel_y"] -= 3

                    elif estado_bola["bola"]["vel_y"] > 0:
                        estado_bola["bola"]["vel_y"] += 3

                    estado_bola["bola"]["vel_y"] *= -1
                    print(estado_bola["bola"]["vel_y"])

                    #nao deixa a bola entrar dentro do jogador
                    if player['nome'] == 'jogador1':
                        estado_bola["bola"]["bola_y"] = player["y"] - estado_bola["bola"]["altura"] - 1
                    elif player['nome'] == 'jogador2':
                        estado_bola["bola"]["bola_y"] = player["y"] + estado_bola["bola"]["altura"] + 1
                    # if estado_bola["bola"]["vel_x"] == 0:
                    if player["movimento"]["a"] == True:
                        estado_bola["bola"]["vel_x"] = -5
                    elif player["movimento"]["d"] == True:
                        estado_bola["bola"]["vel_x"] = 5
                    
            ##### identificando pontuacao #####
            for jogador in jogadores:
                player = jogadores[jogador]
                bola_y = estado_bola["bola"]["bola_y"]
                if player['nome'] == 'jogador1':
                    if bola_y > player['y']: #se a bola passou do player 1
                        for jogador in jogadores: #adiciona 1 ponto pro jogador 2
                            if jogadores[jogador]["nome"] == "jogador2":
                                jogadores[jogador]["pontuacao"] += 1
                                print( jogadores[jogador]["pontuacao"])
                        estado_bola["saque"]["sacador"] = 'jogador1' #coloca a bola em estado de saque para o jogador 1 sacar
                        estado_bola["saque"]["sacando"] = True
                elif player['nome'] == 'jogador2':
                    if bola_y + estado_bola["bola"]["altura"] < player['y'] + player['altura']: #se a bola passar do player 2
                        for jogador in jogadores: #adiciona 1 ponto pro jogador 1
                            if jogadores[jogador]["nome"] == "jogador1":
                                jogadores[jogador]["pontuacao"] += 1
                                print( jogadores[jogador]["pontuacao"])
                                estado_bola["saque"]["sacador"] = 'jogador2' #coloca a bola em estado de saque para o jogador 2 sacar
                                estado_bola["saque"]["sacando"] = True


        ###### RESPONSAVEL POR FAZER O MOVIMENTO(modificar o X) DOS JOGADORES ###
        for jogador in jogadores:
            # print(jogadores[jogador]["x"])
            if jogadores[jogador]['movimento']['a'] == True:
                jogadores[jogador]["x"] -= jogadores[jogador]["velocidade"] /60
            if jogadores[jogador]['movimento']['d'] == True:
                jogadores[jogador]["x"] += jogadores[jogador]["velocidade"] /60
            # print(jogadores[jogador]["nome"],jogadores[jogador]["x"])
            # print(jogadores)


        ##### NAO TEM COMO ENVIAR O DICIONARIO nesse caso PQ A CHAVE É UM OBJETO WEBSOCKET, N FUNCIONA NO JASON ###
        estado_para_enviar = {}
        for websocket in jogadores:
            jogador = jogadores[websocket]

            estado_para_enviar[jogador["nome"]] = jogador

        ###### ENVIANDO PARA O JS (clientes)########
        for websocket in list(jogadores):
            try:
                await websocket.send(json.dumps({
                    "tipo": "estado_bola",
                    "estado": estado_bola
                    
                }))

                await websocket.send(json.dumps({
                    "tipo" : "estado_jogadores",
                    "estado": estado_para_enviar
                }))

            except:
                print(f"falha ao enviar o estado para o jogador {websocket}")                

        await asyncio.sleep(1 / 60)


async def main(): # criando a funcao async main
    # async with serve(receber, "localhost", 8765): #async modifica o with para q ele possa usar um objeto assincrono #local
    PORT = int(os.environ.get("PORT", 8765)) #se existir uma variável de ambiente chamada PORT, use ela. Se não existir, use 8765."
    async with serve(receber, "0.0.0.0", PORT):  #0.0.0.0 permite que o servidor receba conexões externas.
        # argumento:
        #ao passar a funcao receber como uma "variavel" em vez de receber() quer dizer q ela pode ser executada a qualquer momento, só quando for nescessaria em nao agora
        #localhost quer dizer só aceite conexoes vindas do proprio computador
        #8765 é a porta 
        # print("Servidor iniciado em ws://localhost:8765")
        print(f"Servidor iniciado na porta {PORT}")
        asyncio.create_task(game_loop())    #isso cria uma task que já começa a rodar em background AGORA ,Só vai executar DE VERDADE quando encontrar um await (que libera o controle), nessa linha a tarefa é apenas criada // ela roda em paralelo com o resto do programa, diferente do await nomedafuncao() q só vai continuar a execucao das prixmas linhas quando a funcao acabar
        await asyncio.Future()  # isso faz com q algo nunca aconteça , ou seja o o with nunca fecha , o programa fica "esperando" algo acontecer pra fechar o whit mas isso nunca acontece









asyncio.run(main())  #a funcao main() nesse caso deve ser rodada assim pq ela é uma funcao async/ aqui esta sendo criado um eventloop 
#o eventloop é o responsavel por escolher quem é o proximo da fila, por exemplo quando o codigo para em um await, é o event loop q decide quem sera a proxima tarefa





# await asyncio.gather(       Roda várias tarefas em PARALELO e espera TODAS terminarem  Se uma der erro, TODAS são canceladas.
#     tarefa1(),
#     tarefa2(),
#     tarefa3()
# )

# iniciar servidor:
#python servidor.py     no terminal
# comandos cmd:  cd nome,cd ..,  dir