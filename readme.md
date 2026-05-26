# freez in requirement

pip freeze > requirements.txt
pip install -r requirements.txt

# create environment 
python -m venv venv

# for windows
# to activate 
 .\venv\Scripts\Activate

# if not working
 Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser


# for mac
# to activate 
 source venv/bin/activate

# tokentize and detokenize text
 pip install tiktoken



# create requirements file
 pip freeze >requirements.txt


 # update 
  python.exe -m pip install --upgrade pip

 # gemini
   pip install google-genai#

 # fast api
    pip install "fastapi[standard]"

 # run fastapi
    fastapi dev server.py    



 # docker vector deb

    docekr compose up   

# to run in background
    docker compose up -d


# langchain pdf loader

   .. code-block:: bash

       pip install -U langchain-community pypdf

   Instantiate the loader:

   .. code-block:: python

       from langchain_community.document_loaders import PyPDFLoader

       loader = PyPDFLoader(
           file_path = "./example_data/layout-parser-paper.pdf",
           # headers = None
           # password = None,
           mode = "single",
           pages_delimiter = "

# langchain text splitter

 pip install -U langchain-text-splitters

 # langchain open ai embadding

   pip install -qU langchain-openai

# langchain quadrant db

   pip install -qU langchain-qdrant   

# install rq python

  pip install rq

# valkey 
  
   which is alternative of redis (open source)


# to run uvicorn
 uvicorn rag_queue.server:app --reload   

# to run the RQ worker on Windows (uses RQ SimpleWorker)
 python -m rag_queue.run_worker

# langgraph
 pip install -U langgraph

 # mongo db
 pip install -U pymongo langgraph langgraph-checkpoint-mongodb



 # memory layer to save long term memory using mem0
 pip install mem0ai