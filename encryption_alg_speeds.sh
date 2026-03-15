#!/usr/bin/env bash

# ===== USTAWIENIA =====

PLAINTEXT="bigFile.txt"
OUTDIR="wyniki_szyfrowania"
mkdir -p "$OUTDIR"

CSV_SYM="$OUTDIR/symetryczne.csv"
CSV_RSA="$OUTDIR/rsa.csv"

# rozmiar pliku w bajtach
FILESIZE=$(stat -c%s "$PLAINTEXT")

echo "Algorytm,Wariant_bit,Tryb,Real_s,User_s,Sys_s,Mbit_s" > "$CSV_SYM"
echo "Algorytm,Dlugosc_klucza_bit,Operacja,Real_s,User_s,Sys_s" > "$CSV_RSA"

# ===== FUNKCJE =====

gen_bytes () {
  local len="$1"
  head -c "$len" /dev/urandom
}

print_cmd () {
  echo
  echo ">>> Uruchamiam:"
  printf '    %q' "$@"
  echo
}

# pomiar dla szyfrów symetrycznych
measure_and_log_sym () {
  local alg="$1"     # AES / 3DES / DES / RC2 / RC4
  local variant="$2" # długość klucza w bitach
  local mode="$3"    # ECB / CBC / -
  local outfile="$4"
  shift 4

  print_cmd "$@"

  # używamy wbudowanego time; wyjście stdout jest wyciszone, stderr widoczne
  local real_t user_t sys_t
  # zsh/bash: time drukuje na stderr; parsujemy to prostym awk
  # zapisujemy do tymczasowego pliku, żeby nie kombinować z eval
  { time "$@" >"$outfile"; } 2>time_tmp.log
  
  echo "=== Wynik time (sym):"
  cat time_tmp.log

  real_t=$(awk '/^real/ {gsub("s","",$2); sub("0m","",$2); print $2}' time_tmp.log)
  user_t=$(awk '/^user/ {gsub("s","",$2); sub("0m","",$2); print $2}' time_tmp.log)
  sys_t=$(awk  '/^sys/  {gsub("s","",$2); sub("0m","",$2); print $2}' time_tmp.log)

  rm -f time_tmp.log
  rm -f "$outfile"

  if [ -z "$real_t" ] || [ "$real_t" = "0" ] || [ "$real_t" = "0.00" ]; then
    # pomiar się nie udał (błąd komendy) – wpisujemy 0
    mbit_s=0
  else
    mbit_s=$(awk -v size="$FILESIZE" -v t="$real_t" 'BEGIN {print (size*8)/(t*1000000)}')
  fi
  echo "speed   $mbit_s Mbit/s"
  

  echo "$alg,$variant,$mode,$real_t,$user_t,$sys_t,$mbit_s" >> "$CSV_SYM"
}

# pomiar dla RSA (na małym pliku)
measure_and_log_rsa () {
  local bits="$1"
  local op="$2"
  local outfile="$3"
  shift 3

  print_cmd "$@"

  { time "$@" >"$outfile"; } 2>time_tmp.log
  
  echo "=== Wynik time (RSA $bits $op):"
  cat time_tmp.log

  local real_t user_t sys_t
  real_t=$(awk '/^real/ {gsub("s","",$2); sub("0m","",$2); print $2}' time_tmp.log)
  user_t=$(awk '/^user/ {gsub("s","",$2); sub("0m","",$2); print $2}' time_tmp.log)
  sys_t=$(awk  '/^sys/  {gsub("s","",$2); sub("0m","",$2); print $2}' time_tmp.log)

  rm -f time_tmp.log
  rm -f "$outfile"

  echo "RSA,$bits,$op,$real_t,$user_t,$sys_t" >> "$CSV_RSA"
}

# ===== 1. SZYFRY SYMETRYCZNE =====

echo "=== Szyfry symetryczne (AES, 3DES, DES, RC2, RC4) ==="

# AES: 128, 192, 256 bit
for bits in 128 192 256; do
  key_bytes=$((bits / 8))
  KEY_HEX=$(gen_bytes "$key_bytes" | xxd -p | tr -d '\n')

  # ECB (bez IV)
  OUT="$OUTDIR/aes_${bits}_ecb.bin"
  measure_and_log_sym "AES" "$bits" "ECB" "$OUT" \
    openssl enc -aes-"$bits"-ecb -e \
      -in "$PLAINTEXT" -out "$OUT" \
      -K "$KEY_HEX" -nosalt

  # CBC (IV 16 bajtów)
  IV_HEX=$(gen_bytes 16 | xxd -p | tr -d '\n')
  OUT="$OUTDIR/aes_${bits}_cbc.bin"
  measure_and_log_sym "AES" "$bits" "CBC" "$OUT" \
    openssl enc -aes-"$bits"-cbc -e \
      -in "$PLAINTEXT" -out "$OUT" \
      -K "$KEY_HEX" -iv "$IV_HEX" -nosalt
done

# 3DES: 112, 168 bit
echo "=== 3DES ==="
for bits in 112 168; do
  case "$bits" in
    112) key_bytes=16 ;;
    168) key_bytes=24 ;;
  esac
  KEY_HEX=$(gen_bytes "$key_bytes" | xxd -p | tr -d '\n')

  OUT="$OUTDIR/3des_${bits}_ecb.bin"
  measure_and_log_sym "3DES" "$bits" "ECB" "$OUT" \
    openssl enc -des-ede3-ecb -e \
      -in "$PLAINTEXT" -out "$OUT" \
      -K "$KEY_HEX" -nosalt \
      -provider legacy -provider default

  IV_HEX=$(gen_bytes 8 | xxd -p | tr -d '\n')
  OUT="$OUTDIR/3des_${bits}_cbc.bin"
  measure_and_log_sym "3DES" "$bits" "CBC" "$OUT" \
    openssl enc -des-ede3-cbc -e \
      -in "$PLAINTEXT" -out "$OUT" \
      -K "$KEY_HEX" -iv "$IV_HEX" -nosalt \
      -provider legacy -provider default
done

# DES: 56 bit
echo "=== DES ==="
bits=56
KEY_HEX=$(gen_bytes 8 | xxd -p | tr -d '\n')

OUT="$OUTDIR/des_${bits}_ecb.bin"
measure_and_log_sym "DES" "$bits" "ECB" "$OUT" \
  openssl enc -des-ecb -e \
    -in "$PLAINTEXT" -out "$OUT" \
    -K "$KEY_HEX" -nosalt \
    -provider legacy -provider default

IV_HEX=$(gen_bytes 8 | xxd -p | tr -d '\n')
OUT="$OUTDIR/des_${bits}_cbc.bin"
measure_and_log_sym "DES" "$bits" "CBC" "$OUT" \
  openssl enc -des-cbc -e \
    -in "$PLAINTEXT" -out "$OUT" \
    -K "$KEY_HEX" -iv "$IV_HEX" -nosalt \
    -provider legacy -provider default

# RC2: 40, 64 bit
echo "=== RC2 ==="
for bits in 40 64; do
  key_bytes=$((bits / 8))
  KEY_HEX=$(gen_bytes "$key_bytes" | xxd -p | tr -d '\n')

  OUT="$OUTDIR/rc2_${bits}_ecb.bin"
  measure_and_log_sym "RC2" "$bits" "ECB" "$OUT" \
    openssl enc -rc2-ecb -e \
      -in "$PLAINTEXT" -out "$OUT" \
      -K "$KEY_HEX" -nosalt \
      -provider legacy -provider default

  IV_HEX=$(gen_bytes 8 | xxd -p | tr -d '\n')
  OUT="$OUTDIR/rc2_${bits}_cbc.bin"
  measure_and_log_sym "RC2" "$bits" "CBC" "$OUT" \
    openssl enc -rc2-cbc -e \
      -in "$PLAINTEXT" -out "$OUT" \
      -K "$KEY_HEX" -iv "$IV_HEX" -nosalt \
      -provider legacy -provider default
done

# RC4: 128 bit, brak IV
echo "=== RC4 ==="
bits=128
KEY_HEX=$(gen_bytes 16 | xxd -p | tr -d '\n')

OUT="$OUTDIR/rc4_${bits}.bin"
measure_and_log_sym "RC4" "$bits" "-" "$OUT" \
  openssl enc -rc4 -e \
    -in "$PLAINTEXT" -out "$OUT" \
    -K "$KEY_HEX" -nosalt \
    -provider legacy -provider default

# ===== RSA (mały plik) =====

echo
echo "=== RSA (mały plik 1024 B) ==="

SMALLFILE="$OUTDIR/maly_plik.bin"
head -c 1024 /dev/urandom > "$SMALLFILE"

for bits in 1024 2048 3072 4096; do
  KEY_PRIV="$OUTDIR/rsa_${bits}_priv.pem"
  KEY_PUB="$OUTDIR/rsa_${bits}_pub.pem"

  measure_and_log_rsa "$bits" "genkey" "/dev/null" \
    openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:$bits \
      -out "$KEY_PRIV"

  openssl pkey -in "$KEY_PRIV" -pubout -out "$KEY_PUB"

  OUT="$OUTDIR/rsa_${bits}_enc.bin"
  measure_and_log_rsa "$bits" "encrypt" "$OUT" \
    openssl pkeyutl -encrypt \
      -inkey "$KEY_PUB" -pubin \
      -in "$SMALLFILE" -out "$OUT"

  OUT_DEC="$OUTDIR/rsa_${bits}_dec.bin"
  measure_and_log_rsa "$bits" "decrypt" "$OUT_DEC" \
    openssl pkeyutl -decrypt \
      -inkey "$KEY_PRIV" \
      -in "$OUT" -out "$OUT_DEC"
done

echo
echo "Zakończono testy. Wyniki w:"
echo "  $CSV_SYM"
echo "  $CSV_RSA"
