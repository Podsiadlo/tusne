# The Ultimate Śpiewnik Nowej Ewangelizacji
Śpiewnik zbiera teksty pieśni religijnych w formacie [OpenLyrics](https://github.com/openlyrics/openlyrics), który można otworzyć wielu programach do ich wyświetlania takich jak np. [OpenLP](https://openlp.org/).

### Parser
W katalogu parser znajduje się prosty skrypt języka Python, który pozwala na łatwe przerobienie piosenek na format OpenLyrics z zadanego formatu wejściowego. Składnia polecenia wygląda następująco:

`python parser.py -i <plik_wejsciowy> -o <katalog_gdzie_pojawia_sie_piesni>`

*W obecnej wersji wymagane jest istnienie wyjściowego katalogu.*

### Format wejściowy parsera
Parser przyjmuje teksty piosenek w ściśle zadanym formacie.
* Piosenka zaczyna się od **tytułu** napisanego w osobnej linii w **klamrach** `{}`.
* Każdy **ekran** zaczyna się od wiersza oznaczającego jego typ i numer **zakończonego dwukropkiem**. Np. `v1:`
* Zwrotki oznaczamy jako `v`, refreny jako `c`, bridge jako `b`.
* Jeśli w danej zwrotce jest kilka ekranów można je numerować stosując kolejne małe litery w kolejności alfabetycznej. Np. `v1a`, `v1b`, `v1c`
* Jeśli chcemy, aby została dodana nieliniowa kolejność ekranów, np. refren `c1` ma występować po każdej zwrotce, należy dopisać jego numer zakończony dwukropkiem pomiędzy kolejnymi ekranami.
* W jednym pliku może być dowolnie dużo pieśni.
* Puste linie oraz białe znaki na początku i końcu wierszy są pomijane. Aby wymusić dodanie dwóch pustych wierszy można stworzyć wiersz z frazą `<br/>`
* Niemożliwe jest nadpisanie raz zakończonego ekranu. Należy wtedy stworzyć nowy o innej nazwie.

Przykładowa piosenka:
```
{Bo góry mogą ustąpić}
v1:
Bo góry mogą ustąpić i pagórki się zachwiać     x2
Ale miłość moja nie odstąpi od ciebie.
c1:
Tak mówi Pan, tak mówi Pan
Tak mówi Pan, który kocha ciebie, ciebie, ciebie i mnie!
v2:
Choćby matka, która kocha dziecko swego łona opuściła je,   x2
To ja Bóg Ojciec wszechmogący nigdy, nigdy nie opuszczę cię!
c1:
v3:
Bóg kocha cię osobiście, bezwarunkowo kocha cię!   x2
Bóg kocha cię miłością Ojca dlatego, że jesteś Jego dzieckiem!
c1:
```
