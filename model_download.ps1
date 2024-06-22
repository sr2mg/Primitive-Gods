$url = "https://huggingface.co/MCZK/Ninja-V2-7B-GGUF/resolve/main/Ninja-V2-7B.Q5_K_M.iMatrix.gguf?download=true"
$outputFile = "Ninja-V2-7B.Q5_K_M.iMatrix.gguf"

Invoke-WebRequest -Uri $url -OutFile $outputFile
Write-Host "File downloaded: $outputFile"