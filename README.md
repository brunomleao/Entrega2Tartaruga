# Entrega2Tartaruga

obs: A atividade foi realizada no turtlesim, pois meu computador não me permite executar o gazebo.



https://github.com/brunomleao/Entrega2Tartaruga/assets/99328889/adc125b3-330a-48fa-90eb-33057f4966c2



# Descrição do Código

O código fornecido é um exemplo de controle de movimento de uma tartaruga no simulador ROS (Robot Operating System). Ele utiliza a biblioteca rclpy para comunicação com o ROS e os pacotes geometry_msgs.msg e turtlesim.msg para lidar com mensagens de controle e poses da tartaruga.

A estrutura do código é composta por três classes principais:

## Classe `Pose`

A classe Pose é uma extensão da classe TPose do pacote turtlesim.msg e representa a posição da tartaruga no espaço. Além dos atributos de posição (x e y), ela possui um atributo theta para representar a orientação da tartaruga. Essa classe também redefine os métodos especiais __repr__, __add__, __sub__ e __eq__, que são utilizados para facilitar operações e comparações entre poses.

## Classe `PathController`

A classe PathController é responsável por armazenar os pontos de destino por onde a tartaruga deve passar. Ela utiliza a estrutura de dados deque para criar uma fila de poses que representa a sequência de pontos a serem percorridos pela tartaruga. Os métodos enqueue, dequeue e is_empty são utilizados para adicionar pontos à fila, remover o próximo ponto da fila e verificar se a fila está vazia, respectivamente.

## Classe `TurtleController`

A classe TurtleController é uma subclasse de Node do pacote rclpy.node e é responsável por controlar os movimentos da tartaruga. Ela recebe a instância de um objeto PathController no construtor para obter os pontos de destino. A classe cria um publisher para enviar comandos de movimento para a tartaruga e um subscription para receber as poses da tartaruga. O método control_callback é executado periodicamente e calcula os comandos de movimento para a tartaruga com base na diferença entre a posição atual da tartaruga (pose) e o próximo ponto de destino (setpoint). O método pose_callback é chamado sempre que uma mensagem de pose é recebida e atualiza a posição atual da tartaruga. O método update_setpoint é responsável por obter o próximo ponto de destino da fila e atualizar o valor de setpoint. Quando a fila está vazia, a execução é encerrada.

# Utilização

Para utilizar o código, siga as seguintes etapas:

1. Certifique-se de ter o ROS instalado e configurado corretamente em seu sistema.
2. Execute o código fornecido em um ambiente ROS.
3. Será solicitado que você insira as coordenadas de destino para a tartaruga. Digite as coordenadas x e y para cada ponto de destino e pressione Enter para adicionar um novo ponto. Pressione Enter novamente sem digitar nada para finalizar a entrada de pontos.
A tartaruga irá se mover pelos pontos de destino na sequência especificada.
