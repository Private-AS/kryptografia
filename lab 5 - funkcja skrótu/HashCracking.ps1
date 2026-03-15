param ( [int]$timeout = 1200 )

function New-Hash {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Text,

        [Parameter(Mandatory = $true)]
        [ValidateSet("SHA1","sha1",
        "SHA256","sha256",
        "SHA384","sha384",
        "SHA512","sha512",
        "MD5","md5")]
        [string]$Hash
    )

    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)

    switch ($Hash.ToUpper()) {
        "MD5"     { $alg = [System.Security.Cryptography.MD5]::Create() }
        "SHA1"    { $alg = [System.Security.Cryptography.SHA1]::Create() }
        "SHA256"  { $alg = [System.Security.Cryptography.SHA256]::Create() }
        "SHA384"  { $alg = [System.Security.Cryptography.SHA384]::Create() }
        "SHA512"  { $alg = [System.Security.Cryptography.SHA512]::Create() }
    }

    $hashBytes = $alg.ComputeHash($bytes)
    $hashString = [BitConverter]::ToString($hashBytes) -replace "-", ""
    return $hashString.ToLower()
}

function New-RandomString {
    param([int]$Length, [string]$Charset)
    $chars = $Charset.ToCharArray()
    -join (1..$Length | ForEach-Object { $chars | Get-Random })
}


$algorithm = [ordered]@{
        'SHA1'   = 100
        'SHA512' = 1700
    }
$charsets = '?l?d', '?a'
$ErrNo = 0
$MainFlag = $True
$timeoutFlags = @{
    'SHA1_?l?d' = $false
    'SHA1_?a' = $false
    'SHA512_?l?d' = $false
    'SHA512_?a' = $false
}
$i = 1
$results = @()
while ($MainFlag -and $ErrNo -lt 5) {
    $RandomString = New-RandomString -Length $i -Charset 'abcdefghijklmnopqrstuvwxyz'
    $sha1 = New-Hash -Text $RandomString -Hash 'SHA1'
    $sha512 = New-Hash -Text $RandomString -Hash 'SHA512'
    Write-Host "Generated Random String of length ${i}: $RandomString"
    $hashes = @{
        'SHA1'   = $sha1
        'SHA512' = $sha512
    }
    $mask = "?1" * $i
    $result = [PSCustomObject]@{
        Length = $i
        Text = $RandomString
        SHA1_Hash = $sha1
        SHA1_Time_ld = 0
        SHA1_Time_a = 0
        SHA512_Hash = $sha512
        SHA512_Time_ld = 0
        SHA512_Time_a = 0
    }
    foreach ($alg in $algorithm.Keys) {
        $hash = $hashes[$alg]
        foreach ( $charset in $charsets ) {
            
            Write-Host "Trying to crack $alg hash: $hash with mask: $mask and charset: $charset"
        
            $hashcatArgs = @(
                '-a', '3', 
                '-m', $algorithm[$alg], 
                '-O',
                '-d', '1',
                '--quiet',
                '--backend-ignore-cuda',
                '--potfile-disable',
                #'--hwmon-disable', 
                "--runtime=$timeout", 
                '--outfile-format=2,6', 
                $hashes[$alg], 
                '-1', $charset, 
                $mask)
            if ($charset -eq '?a' -and $alg -eq 'SHA1' -and $timeoutFlags['SHA1_?a']) {
                $result.SHA1_Time_a = $timeout * 2
                Write-Host "Not cracked within time limit."
                continue
            }
            if ($charset -eq '?a' -and $alg -eq 'SHA512' -and $timeoutFlags['SHA512_?a']) {
                $result.SHA512_Time_a = $timeout * 2
                Write-Host "Not cracked within time limit."
                continue
            }
             if ($charset -eq '?l?d' -and $alg -eq 'SHA1' -and $timeoutFlags['SHA1_?l?d']) {
                $result.SHA1_Time_ld = $timeout * 2
                Write-Host "Not cracked within time limit."
                continue
            }
            if ($charset -eq '?l?d' -and $alg -eq 'SHA512' -and $timeoutFlags['SHA512_?l?d']) {
                $result.SHA512_Time_ld = $timeout * 2
                Write-Host "Not cracked within time limit."
                continue
            }
            $hashcatOutput = & C:\Utils\hashcat-7.1.2\hashcat @hashcatArgs 2>$null
            Write-Debug "Hashcat Output: $hashcatOutput"
            Write-Debug "Hashcat Exit Code: $LASTEXITCODE"
            if ( $LASTEXITCODE -eq 0 ) {
                [int]$time, [string]$text = $hashcatOutput -split ":"
                if ($text -ne $RandomString) {
                    Write-Host "Mismatch in cracked text. Expected: $RandomString, Got: $text"
                    $time =  0 - $time
                } else {
                    Write-Host  "Cracked in $time seconds: $text"
                }
            }
            elseif ($LASTEXITCODE -eq 4) {
                $time = $timeout * 2
                $text = "NOT FOUND (Timeout)"
                Write-Host "Not cracked within time limit."
            }
            else {
                $ErrNo += 1
                $time = -1
                $text = "ERROR"
                Write-Error "ERROR:"
                Write-Error "Exit code: $LASTEXITCODE"
                Write-Error "Output: $hashcatOutput"
            }

        switch ($alg) {
            'SHA1' {
                if ($charset -eq '?l?d') {
                    $result.SHA1_Time_ld = $time
                } elseif ($charset -eq '?a') {
                    $result.SHA1_Time_a = $time
                }
            }
            'SHA512' {
                if ($charset -eq '?l?d') {
                    $result.SHA512_Time_ld = $time
                } elseif ($charset -eq '?a') {
                    $result.SHA512_Time_a = $time
                }
            }
        }
         if ($result.SHA1_Time_ld -ge $timeout) {
        $timeoutFlags['SHA1_?l?d'] = $true
        }
        if ($result.SHA1_Time_a -ge $timeout) {
            $timeoutFlags['SHA1_?a'] = $true
        }
        if ($result.SHA512_Time_ld -ge $timeout) {
            $timeoutFlags['SHA512_?l?d'] = $true
        }
        if ($result.SHA512_Time_a -ge $timeout) {
            $timeoutFlags['SHA512_?a'] = $true
        }
    }}
    if ( $timeoutFlags['SHA1_?l?d'] -and
         $timeoutFlags['SHA1_?a'] -and
         $timeoutFlags['SHA512_?l?d'] -and
         $timeoutFlags['SHA512_?a'] ) {
        $MainFlag = $false
    }
    $results += $result
    $result | Format-List
    $i++
}
$results | Export-Csv -Path "Hashcat_Performance_Results.csv" -NoTypeInformation -Delimiter ';'