# 1.1
## Format wysyłanej wiadomości o długości n
    [2 bajty][n-3 bajty treści: ABC...XYZABC...][1 bajt '\0']

## Sprawdzenie poprawności
    
1. długość wiadomości >= 3 (obowiązkowa pierwsza i ostatnia część np b'x00\x03\x00')
2. obecność '\0' na końcu
3. poprawna długość czyli długość odczytana z pierwszych 2 bajtów == długość całej wiadomości
4. środkowa część zawiera tylko znaki A-Z
5. znaki w środkowej części są ułożone w porządku ABC...XYZABC...

## Kompilacja
    cd c
    makedir build obj
    cd src
    make server
    make client

## Uruchomienie
    cd build
    ./client
    ./server
