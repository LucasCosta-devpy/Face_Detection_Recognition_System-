# 🤖 Face Detection Recognition System

## 📜 Descrição do Projeto
O `Face_Detection_Recognition_System` é um sistema de reconhecimento facial que utiliza a câmera web do dispositivo local para capturar imagens em tempo real e compará-las com rostos previamente cadastrados no sistema. Caso o rosto capturado seja reconhecido, o sistema exibe as imagens da face capturada e a face correspondente cadastrada.

Este projeto foi desenvolvido com o objetivo de demonstrar como o reconhecimento facial pode ser implementado de forma simples em um ambiente local, sem a necessidade de conexão com servidores remotos ou serviços em nuvem.

## ⚙️ Como Funciona
1. **Captura de Imagem**: O sistema acessa a câmera web do computador e captura imagens em tempo real.
2. **Processamento e Reconhecimento**: A imagem capturada é comparada com um banco de dados local de imagens cadastradas.
3. **Exibição dos Resultados**: Se um rosto for reconhecido, o sistema exibe a imagem capturada e a imagem correspondente do banco de dados.

## 📦 Pré-Requisitos
- Python 3.x instalado no sistema
- Bibliotecas necessárias:
  - `opencv-python` para manipulação de imagens e acesso à câmera
  - `face_recognition` para detecção e reconhecimento facial
  - `numpy` para operações com arrays

### 🛠️ Instalação das Dependências
Para instalar as bibliotecas necessárias, execute:
```bash
pip install opencv-python face_recognition numpy

🚀 Como Executar o Projeto
    Clone o repositório:

        git clone https://github.com/seu-usuario/Face_Detection_Recognition_System.git
        cd Face_Detection_Recognition_System

    Adicione as imagens de rosto cadastradas: Coloque as imagens de rostos previamente cadastrados na pasta especificada pelo código (por exemplo, faces_cadastradas/).

    Execute o script principal:
        python face_recognition_system.py

📊 Funcionamento Detalhado
    Captura da Câmera: O sistema utiliza a biblioteca OpenCV para acessar a câmera do dispositivo e capturar quadros de vídeo em tempo real.
    Detecção de Rosto: Com a ajuda da biblioteca face_recognition, o sistema detecta e compara os rostos capturados com os rostos cadastrados.
    Reconhecimento e Exibição: Caso um rosto seja reconhecido, as imagens do rosto capturado e do rosto correspondente são exibidas lado a lado em uma janela de visualização.
⚠️ Observações
    Execução Local: Este código foi projetado para ser executado apenas localmente, usando a câmera e o banco de dados de imagens do dispositivo em que o código está rodando.
    Segurança: Certifique-se de usar este sistema em um ambiente seguro, pois ele não inclui medidas de proteção de dados ou segurança avançada.
📚 Exemplos de Uso
O projeto pode ser usado em aplicações de demonstração de reconhecimento facial, sistemas de segurança para pequenos escritórios ou apenas para fins educacionais e de aprendizado.

📄 Licença
Este projeto é de uso livre para fins educacionais e de desenvolvimento pessoal.

Para dúvidas ou contribuições, entre em contato através do repositório ou envie um e-mail para [lucas_dscosta@hotmail.com].
