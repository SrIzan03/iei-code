Param(
    [string]$InputFile,
    [string]$OutputFile
)

# Leer el contenido del archivo JSON como texto
$jsonText = Get-Content -Path $InputFile -Raw

# Regex para eliminar atributos duplicados vacíos (address o phone)
# Patrón para encontrar "address" o "phone" con un valor vacío
$jsonProcessed = $jsonText -replace '"(address|phone)"\s*:\s*"",?', ''

# Guardar el JSON modificado en un archivo nuevo
Set-Content -Path $OutputFile -Value $jsonProcessed