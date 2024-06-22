
from llama_cpp import Llama
import os
class LlamaCppAdapter:
    _instance = None
    def __new__(cls,n_ctx=4096):
        if not cls._instance:
            cls._instance = super(LlamaCppAdapter,cls).__new__(cls)
            my_path = os.path.dirname(os.path.abspath(__file__))
            cls._instance.llama:Llama = Llama(model_path=my_path+"/Ninja-V2-7B.Q5_K_M.iMatrix.gguf",n_ctx=n_ctx,n_gpu_layers=-1,verbose=False)

        return cls._instance

    def generate(self,prompt,max_new_tokens=250,temperature=0.5,top_p=0.7,top_k=80,stop=["\n"]):
        return self._generate(prompt,max_new_tokens,temperature,top_p,top_k,stop=stop)["choices"][0]["text"].strip()

    def _generate_stream(self,prompt,temperature,max_new_tokens,top_p,top_k):
        return self.llama(
            prompt,
            temperature=temperature,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            stop=["\n"],
            repeat_penalty=1.2,
            stream=True
        )


    def _generate(self,prompt:str,max_new_tokens:int,temperature:int,top_p:int,top_k:int,stop=["\n"]):
        return self.llama(
            prompt,
            temperature=temperature,
            max_tokens=max_new_tokens,
            top_p=top_p,
            top_k=top_k,
            stop=stop,
            repeat_penalty=1.2,
        )

