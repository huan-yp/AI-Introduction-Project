$env:http_proxy = "http://localhost:7890"
$env:https_proxy = "http://localhost:7890"
[System.Net.WebRequest]::DefaultWebProxy = New-Object System.Net.WebProxy($env:http_proxy)
[System.Net.WebRequest]::DefaultWebProxy.BypassProxyOnLocal = $false
conda activate AI
python -m api.tts_server
