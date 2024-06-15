import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import base64

# szyfrowanie za pomoca XOR
def encrypt_xor(message, key):
    ciphertext = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, key))
    return ciphertext

# dszyfrowanie za pomoca XOR
def decrypt_xor(ciphertext, key):
    plaintext = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(ciphertext, key))
    return plaintext

# wysylanie e-maila z zalacznikiem
def send_email_with_attachment(to_email, subject, body, file_path):
    # to jest moje prywatne konto, prosze uzywac tylko w celach testowania projektu
    from_email = "nope@gmail.com"  
    password = "wywrotka" 

    # Tworzenie obiektu MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Dodanie tresci wiadomosci
    msg.attach(MIMEText(body, 'plain'))

    # Zalaczenie pliku
    with open(file_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {file_path}")
        msg.attach(part)

    # Konfiguracja serwera SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)

    # Wyslanie e-maila
    server.send_message(msg)
    server.quit()

password = input("Podaj haslo: ")
email = input("Podaj email: ")

# Klucz do szyfrowania
key = "b45614894561456aefsafa45544456"  # Klucz

# Szyfrowanie wiadomosci
ciphertext = encrypt_xor(password, key)

# Kodowanie zaszyfrowanej wiadomosci w Base64
encoded_ciphertext = base64.b64encode(ciphertext.encode('utf-8')).decode('utf-8')
print("Zakodowana zaszyfrowana wiadomosc (Base64):", encoded_ciphertext)

decrypt_script = f"""
import base64

def decrypt_xor(ciphertext, key):
    ciphertext = base64.b64decode(ciphertext).decode('utf-8')
    plaintext = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(ciphertext, key))
    return plaintext

ciphertext = '{encoded_ciphertext}'
key = input("Podaj klucz: ")
print("Odszyfrowana wiadomosc:", decrypt_xor(ciphertext, key))
"""

# Zapisywanie skryptu do pliku
with open('decrypt.py', 'w') as f:
    f.write(decrypt_script)

# Wysylanie e-maila
email_body = f"Zaszyfrowana wiadomosc (Base64): {encoded_ciphertext}\nW zalaczniku znajdziesz plik z kodem do jej odszyfrowania."
send_email_with_attachment(email, "Zaszyfrowana wiadomosc i klucz", email_body, "decrypt.py")
