# Ruta al archivo JSON
$inputFile = "C:\Users\GamerX\Desktop\ProyectoIEI\iei-code\wrappers\data_sources\edificios.json"

$outputFile = "C:\Users\GamerX\Desktop\ProyectoIEI\iei-code\wrappers\data_sources\edificios2.json"
# Leer el contenido del archivo JSON como texto
$jsonText = Get-Content -Path $inputFile -Raw

# Regex para eliminar atributos duplicados vacíos (address o phone)
# Patrón para encontrar "address" o "phone" con un valor vacío
$jsonProcessed = $jsonText -replace '"(address|phone)"\s*:\s*"",?', ''

# Guardar el JSON modificado en un archivo nuevo
Set-Content -Path $outputFile -Value $jsonProcessed

Write-Host "El archivo JSON procesado se ha guardado en: $outputFile"

# Convertir el JSON de vuelta a texto y guardar el archivo actualizado
$outputFile = "C:\Users\GamerX\Desktop\ProyectoIEI\iei-code\wrappers\data_sources\edificios2.json"


