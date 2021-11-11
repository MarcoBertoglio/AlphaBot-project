# AlphaBot-project

L'AlphaBot funziona tramite la comunicazione di un client e di un server e con l'integrazione di un database nel lato server, in questo database ci sono delle istruzioni per far muovere robot.

![image](https://user-images.githubusercontent.com/72200894/141262474-5249d859-4c14-4d2a-9104-68312d4e1900.png)

## Lato client-server

con le librerie base dell'AlphaBot siamo riusciti a far muovere il robot con delle istruzioni base come ad esempio avanti, destra ecc...
Nella seconda parte abbiamo usato comandi più complessi tipo: ZIG-ZAG, GIRA_ORARIO ecc....
Questo lo si è fatto interrogando il database ed estraendo le istruzioni semplici che formavano quelle complesse. 

## Database

il database è formato da 3 campi:
### ID
### Nome
### Istruzione
