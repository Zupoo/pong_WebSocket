const tela = document.getElementById("tela");     // pega o canvas do HTML pelo id "tela" (localiza ele la no html pra poder usar ele no JS)
const ctx = tela.getContext("2d");       // pega a ferramenta de desenho 2D do canvas (agora posso usar a funcçoes 2d do canvas pra desenhar )
const jogador1 = {       //criando o objeto jogador
    x: 0,
    y: 0,
    largura: 0,
    altura: 0,
    velocidade: 0,
    pontucao: 0
};
const jogador2 = {       //criando o objeto jogador
    x: 0,
    y: 0,
    largura: 0,
    altura: 0,
    velocidade: 0,
    pontuacao: 0
};


const bola ={
    x: 600,
    y: 300,
    largura: 20,
    altura: 20,
    velocidadeX: 100,
    velocidadeY: 100,
    velocidade_padrao: 100
};

const teclas_mover = {
    tipo: "movimento"
};



function atualizar() {

    ctx.clearRect(0, 0, tela.width, tela.height);  //apaga a area retangular, começando no 0 0 e apaga até o tamanho da tela inteira ou seja apaga tudo

    //---------------------------------Movimentar jogador---------------------------------
    // if (teclas["a"]) {
    //     jogador1.x -= jogador1.velocidade / 60;  //dividido por 60 pq cada vez q o codigo passa aqui é 1 frame e tem aproximadamente 60 fps
    //     if (jogador1.x < 0 ){ //limitando bordas se o jogador passou o pixel 0 
    //         jogador1.x = 0; //ele volta pro 0
    //     }
    // }
    // if (teclas["d"]) {
    //     jogador1.x += jogador1.velocidade / 60;
    //     if (jogador1.x > tela.width - jogador1.largura){
    //         jogador1.x = tela.width - jogador1.largura
    //     }
    // }
    // if (teclas["ArrowRight"]) {
    //     jogador2.x += jogador2.velocidade / 60;
    //     if (jogador2.x > tela.width - jogador2.largura){
    //         jogador2.x = tela.width - jogador2.largura
    //     }
    // }
    // if (teclas["ArrowLeft"]) {
    //     jogador2.x -= jogador2.velocidade / 60;
    //     if (jogador2.x < 0 ){ //limitando bordas se o jogador passou o pixel 0 
    //         jogador2.x = 0; //ele volta pro 0
    //     }
    // }        



//desenho placar
    ctx.font = "70px Verdana";  
    ctx.textAlign = "center";
    ctx.fillStyle = "Pink";
    ctx.fillText(jogador2.pontuacao ,tela.width/2 , tela.height*0.28);
    ctx.fillStyle = "LightBLue";
    ctx.fillText(jogador1.pontuacao ,tela.width/2, tela.height * 0.77);

    //---------------------------------desenhando jogador---------------------------------
    ctx.fillStyle = "LightBLue";  //faz tudo desenhado depois disso ser branco
    ctx.fillRect(      //desenha o jogador
        jogador1.x,
        jogador1.y,
        jogador1.largura,
        jogador1.altura
    );

    ctx.fillStyle = "Pink";  //faz tudo desenhado depois disso ser branco
    ctx.fillRect(      //desenha o jogador
        jogador2.x,
        jogador2.y,
        jogador2.largura,
        jogador2.altura
    );    

    //---------------------------------desenhando bola---------------------------------
    ctx.fillStyle = "green";
    ctx.fillRect(
        bola.x,
        bola.y,
        bola.largura,
        bola.altura
    );

    requestAnimationFrame(atualizar);  //faz repetir a funcao (while True)
}


document.addEventListener("keydown", (evento) => {  //addEventListener ele fica esperando acontecer algo (se oq aconteceu for"keydown",(pego o evento) e faz a funcao =>{ faz isso aqui})
    if (event.key == 'a' || event.key == 'd' || event.key == 'w' || event.key == 'z'){
    teclas_mover[event.key] = true;
    socket.send(JSON.stringify(teclas_mover))
    // console.log(teclas)
    }
    else{
        const teclas = {
        tipo: "tecla",
        tecla: evento.key
    }
        socket.send(JSON.stringify(teclas))

    }
    
});

document.addEventListener("keyup", (evento) => {
    if (event.key == 'a' || event.key == 'd' || event.key == 'w' || event.key == 'z'){
    teclas_mover[event.key] = false;
    socket.send(JSON.stringify(teclas_mover))
    }
    
    
});



document.addEventListener("keydown", (evento) => { 
    // console.log(evento.key); //mostra no console quando no f12
});


tela.width = 800;
tela.height = 600;

atualizar()


// const socket = new WebSocket("ws://localhost:8765");//cria um objeto do tipo websocket, agora a "variavel"socket é um objeto e pode usar funçoes do websocket //igual quando tem umca classe e gera um objeto da classe
//ws://localhost:8765 é endereço
const socket = new WebSocket("wss://pong-websocket.onrender.com"); //para conectar o o websocket em vez do localhost
//e ao criar o objeto socket ele ja tenta conectar ao endereço q passa como parametro
socket.onopen = () => {    // coloca a funçao dentro de socket.open pra quando o navegador rodar socket.onopen() rodar a funcao
    console.log("Conectado ao servidor!"); 
    const mensagem_usuario = prompt("Digite alguma coisa:");
    const comando = {
        tipo: "mensagem",
        texto: mensagem_usuario
    };
    socket.send(JSON.stringify(comando))
};

socket.onmessage = (evento) => {     

    // console.log(evento)
    // O navegador executa esta função quando uma mensagem chega do servidor por causa do .onmessage
    // console.log("Servidor respondeu:", evento.data);    //coloca essa funçao dentro do socket.onmessage e evento é o parametro, 
    const resposta = JSON.parse(evento.data)
    if (resposta.tipo == "mensagem"){
        console.log(resposta.texto)
    }
    else if (resposta.tipo == "jogadores"){
        console.log(resposta.jogadores_conectados)
    }

    else if (resposta.tipo == "estado_bola"){
        const estado_bola = resposta.estado;

        bola.x = estado_bola.bola.bola_x;
        bola.y = estado_bola.bola.bola_y;
        bola.velocidadeX = estado_bola.bola.vel_x;
        bola.velocidadeY = estado_bola.bola.vel_y;
        bola.altura = estado_bola.bola.altura;
        bola.largura = estado_bola.bola.largura;
    }
    else if (resposta.tipo == "estado_jogadores"){
        const estado = resposta.estado;

        jogador1.x = estado.jogador1.x;
        jogador1.y = estado.jogador1.y;
        jogador1.largura = estado.jogador1.largura;
        jogador1.altura = estado.jogador1.altura;
        jogador1.velocidade = estado.jogador1.velocidade;
        jogador1.pontuacao = estado.jogador1.pontuacao;

        jogador2.x = estado.jogador2.x;
        jogador2.y = estado.jogador2.y;
        jogador2.largura = estado.jogador2.largura;
        jogador2.altura = estado.jogador2.altura;
        jogador2.velocidade = estado.jogador2.velocidade;
        jogador2.pontuacao = estado.jogador2.pontuacao;

    }

    else if (resposta.tipo == "movimento"){
        socket.send(JSON.stringify(teclas))
        console.log(teclas)    
    }

    


    //nesse caso evento.data é a mensagem q vou enviada la do servidor.py   websocket.send                                                                          


};

// const comando = { //criando um objeto 
//     tipo: "mover",
//     direcao: "direita"
// };
// socket.send(JSON.stringify(comando))   // transformando o objeto comando em uma string json e enviando ela para o servidor


// document.addEventListener("keydown", (evento) => {


//     if (evento.key == "a"){
//         const comando = { //criando um objeto 
//         tipo: "mover",
//         direcao: "esquerda",
//         tecla: evento.key

//         };
//     socket.send(JSON.stringify(comando))   // transformando o objeto comando em uma string json e enviando ela para o servidor
//     }

//     else if (evento.key == "d"){
//         const comando = {
//             tipo: "mover",
//             direcao: "direita",
//             tecla: evento.key
//         };
//     socket.send(JSON.stringify(comando))   // transformando o objeto comando em uma string json e enviando ela para o servidor
//     };

// });

const botao_usuarios_conectados  = document.getElementById("btnUsuarios");
botao_usuarios_conectados.addEventListener('click', () =>{
    console.log('botao click');
    const comando = {
        tipo: "pergunta",
        pedido: "usuarios_conectados"
    }
    socket.send(JSON.stringify(comando))
});
