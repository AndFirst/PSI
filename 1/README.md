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

# 1.2

Jak widać, podczas wysłania pakietu o rozmiarze 65508 wystąpił błąd. Przyczyną jest ograniczenie protokołu UDP, który pozwala na wysłanie pakietów o długości do 65507 bajtów włącznie.
16 bitowe pole Total Length w protokole IPv4 określa rozmiar pakietu w bajtach, z których 8 bajtów zajmuje nagłówek UDP i 20 bajtów nagłówek IPv4, w wyniku mamy 65535 – (20+8) = 65507 bajty przeznaczone na dane.