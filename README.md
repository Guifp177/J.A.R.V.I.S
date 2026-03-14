# J.A.R.V.I.S. — v1.5 Beta
<img width="1242" height="751" alt="Captura de tela 2026-02-13 175443" src="https://github.com/user-attachments/assets/0e048b6a-fdcf-45e1-97dd-d85a4b10c4fc" />
README PT-BR / EN

PT-BR
=========================================
Assistente inteligente local inspirado no J.A.R.V.I.S. do Tony Stark do MCU, desenvolvido em Python, com interface gráfica, voz opcional, microfone, memória persistente , utiliza integração com Ollama (Cloud Free/Paga ou Modelos Locais). 

💻 Requisitos:
1. Windows 10 ou 11
2. Python 3.10+
3. Ollama instalado
4. Conta Google Para GEMINI FREE/PAGO


🔧 Instruções:
1. Instale o Python [Aqui](https://www.python.org/downloads/)
2. Baixar o Ollama (Opcional) [Aqui](https://ollama.com/download) , Abrir e deixar na Bandeja do WIN com o modelo Qwen3-480b-Cloud Selecionado
3. Baixe o Projeto e rodar:
4. ```bash
   pip install -r requirements.txt
5. Criar um API no Ollama Grátis [Clique](https://ollama.com/settings/keys)
6. Criar um API GEMINI Grátis [Clique](https://aistudio.google.com/api-keys)
7. Executar o JARVIS_LAUNCHER.bat, e utilizar. 

🧩 Funcionalidades:
Interface gráfica em PyQt
Reconhecimento de voz 
Voz masculina 
Memória persistente (memory_store.json)
Pesquisa web
Modo silencioso (sem voz)
Launcher interativo (.bat)

📂 Estrutura do Projeto (Resumo)
assets/        → Sons, Imagens e Gifs da Interface
core/          → IA, memória e prompt principal
modules/       → Microfone, Som,Funcs
ui/            → Interface gráfica
voice/         → Voz do JARVIS e reconhecimento 
main.py        → Arquivo principal
JARVIS_LAUNCHER.bat → Launcher 


EN:
Local intelligent assistant inspired by J.A.R.V.I.S., developed in Python, with graphical interface, optional voice, microphone, persistent memory, and integration with Ollama (Cloud Free/Paid or Local).

💻Requirements:
Windows 10 or 11
Python 3.10+
Ollama Installed

🔧 Instructions:
1. Install Python [Here](https://www.python.org/downloads/)
2. Install Ollama [Ollama](https://ollama.com/download) , Run It and leave it in system tray with the QWEN3-480B-Cloud Model Selected
3. Download the project and run:
4. ```bash
   pip install -r requirements.txt
5. Create a API KEY for free on OLLAMA CLOUD and set it:
6. ```bash
   setx OLLAMA_API_KEY "sua_api"
7. Execute the JARVIS_LAUNCHER.bat, and now, use.

🧩 Features:
PyQt GUI: Modern and interactive interface.
Voice Recognition: Hands-free interaction.
Male Voice Output: Immersive J.A.R.V.I.S. vocal responses.
Persistent Memory: Saves context in memory_store.json.
Web Search: Capable of looking up real-time information.
Silent Mode: Option to toggle voice off.
Interactive Launcher: Simple .bat execution.

📂 Project Structure:
assets/ → UI Sounds, Images, and Gifs.
core/ → AI Logic, memory management, and system prompt.
modules/ → Microphone, Sound, and Utility functions.
ui/ → Graphical Interface files.
voice/ → Voice synthesis and recognition engine.
main.py → Application entry point.
JARVIS_LAUNCHER.bat → Quick-start script.



Aviso Legal / Disclaimer ⚠️
PT-BR: Este projeto é um tributo de fã, desenvolvido apenas para fins educacionais e de estudo de IA. O nome J.A.R.V.I.S., bem como os conceitos visuais e nomes associados ao Universo Cinematográfico Marvel (MCU), são marcas registradas e propriedade intelectual da Marvel Entertainment, LLC e The Walt Disney Company. Este software não possui fins lucrativos e não tem afiliação oficial com as empresas mencionadas.
EN: This project is a fan tribute, developed solely for educational and AI research purposes. The name J.A.R.V.I.S., as well as visual concepts and names associated with the Marvel Cinematic Universe (MCU), are registered trademarks and intellectual property of Marvel Entertainment, LLC and The Walt Disney Company. This software is non-profit and has no official affiliation with the aforementioned companies.
