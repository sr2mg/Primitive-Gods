# Primitive Gods
A game using llm.


## installation
`https://huggingface.co/MCZK/Ninja-V2-7B-GGUF/resolve/main/Ninja-V2-7B.Q5_K_M.iMatrix.gguf?download=true`からモデルをDLしてください。  
`pip install -r requirements.txt`した後llama-cpp-pythonを入れてください。  
`pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121`でCuBLASを使えるはずです。  
`cp .env.template .env`で.envを作成し`ANTHROPIC_API_KEY=""`を書いてください。  


## play
`python start.py`

## 備考

[Ninja-V2-7B](https://huggingface.co/Local-Novel-LLM-project/Ninja-V2-7B)を量子化した、[MCZK/Ninja-V2-7B-GGUF](https://huggingface.co/MCZK/Ninja-V2-7B-GGUF)のQ5_K_M.iMatrixを使用しています。

