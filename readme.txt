-creaate an empty folder Cuncelloe_ChatBot
-open it is VS Code
-at terminal python -m venv nameoe_env
-Windows: python -m pip install --upgrade pip
-install python 3,10x version
-activate enviroment
-Windows (Command Prompt):
-Run .venv\Scripts\activate.

-ON OS command Windowspip install ollama
-ollama run llama3

-Them come back to VS Code terminal
-create requirements.txt with below content

-flask
-langchain
-langchain-community
-langchain-core
-langchain-ollama
-chromadb
-docx2txt

-and sab=ve and run below command
-pip install -r requirements.txt in the terminal command of VS Code
-then create three folder docs , static , templetes

                        docs -
                              |
                              |-DataAnalytics.txt
                              |-DataScience.txt
                              |-JavaFullStack.txt
                        

                        static - 
                                |- style.css

                        templetes - 
                                   |- index.html
                
                        app.py

- In docs folder there are three DataAnalytics , DataScience , JavaFullStack 
- In those folder the information of perticuler course (Title, info. , tools , duration ,fees)

- templetes folder there is html file structure of the file
- Static folder there is Css file designing of the page 
- app.py from this folder we actually build the model 
        - for building the model we need to import some in-build libraries like : flask , langchain , langchain-community , langchain-core , langchain-ollama , chromadb , docx2txt 
        - Flow Of Program : User → Frontend → Flask → LangChain → Embeddings → Chroma DB → Retrieval → LLM (Ollama) → Response → UI 
        - then for the run the Program we need to go to vs code terminal then write command "python app.py"
        - After command there is URL  called  http://127.0.0.1:5000
        - after hitting URL then project will run 