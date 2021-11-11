import socket as sck

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.connect(('192.168.0.129', 5000))

    while True:
        messaggio = input("Messaggio: ")
        s.sendall(messaggio.encode())


        if messaggio == "exit":
            print("Chiusura connessione")
            break

    s.close()

main()