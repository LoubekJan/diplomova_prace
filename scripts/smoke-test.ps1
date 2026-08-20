param(
    [Parameter(Mandatory = $true)]
    [string]$BaseUrl
)

$ErrorActionPreference = "Stop"
$BaseUrl = $BaseUrl.TrimEnd("/")

Write-Host "Waiting for $BaseUrl/healthz"

$ready = $false

for ($i = 1; $i -le 120; $i++) {
    try {
        Invoke-WebRequest `
            -Uri "$BaseUrl/healthz" `
            -UseBasicParsing `
            -TimeoutSec 3 | Out-Null

        $ready = $true
        break
    }
    catch {
        Start-Sleep -Seconds 1
    }
}

if (-not $ready) {
    throw "Application did not become ready."
}

$title = "smoke-test-$([DateTimeOffset]::UtcNow.ToUnixTimeSeconds())"

$created = Invoke-RestMethod `
    -Method Post `
    -Uri "$BaseUrl/api/tasks" `
    -ContentType "application/json" `
    -Body (@{ title = $title } | ConvertTo-Json)

$tasks = Invoke-RestMethod `
    -Method Get `
    -Uri "$BaseUrl/api/tasks"

$found = @($tasks) | Where-Object { $_.title -eq $title }

if (-not $found) {
    throw "Created task was not returned by API."
}

Invoke-RestMethod `
    -Method Patch `
    -Uri "$BaseUrl/api/tasks/$($created.id)" `
    -ContentType "application/json" `
    -Body '{"completed":true}' | Out-Null

Invoke-RestMethod `
    -Method Delete `
    -Uri "$BaseUrl/api/tasks/$($created.id)" | Out-Null

Write-Host "Smoke test PASSED: $BaseUrl"
