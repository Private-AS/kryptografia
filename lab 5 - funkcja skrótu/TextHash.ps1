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

$hashLengthBytes = $hashBytes.Length
$hashLengthBits = $hashLengthBytes * 8

Write-Output "Hash: $hashString"
Write-Output "Length (bytes): $hashLengthBytes"
Write-Output "Length(bits): $hashLengthBits"
