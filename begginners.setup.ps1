# エラーが発生したら即座に終了
$ErrorActionPreference = "Stop"

# 仮想環境の名前（好みに応じて変更可能）
$VENV_NAME = ".venv"

# 仮想環境を作成
python -m venv $VENV_NAME

# 仮想環境をアクティベート
& "$VENV_NAME\Scripts\Activate.ps1"

pip install -r requirements.txt

# CUDA が利用可能かチェック
try {
    $nvidiaSmiOutput = nvidia-smi
    Write-Host "CUDA が利用可能です。CUDA 対応版をインストールします。"
    pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
}
catch {
    Write-Host "CUDA が利用できません。通常版をインストールします。"
    pip install llama-cpp-python
}

Write-Host "インストールが完了しました。"
Write-Host "仮想環境を有効化するには以下のコマンドを実行してください："
Write-Host "& `"$VENV_NAME\Scripts\Activate.ps1`""