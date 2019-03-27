import speech_recognition as sr
import time
print("oi")
active = False

def get_voice_command(t=2.0):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("ouvindo...")
        audio = r.listen(source, timeout= t)
    try:
        return r.recognize_google(audio, language="pt-BR")
    except sr.UnknownValueError:
        print("que diabos vc tá falando meow")
        return ''
    except sr.RequestError as e:
        print("erro bizarro: {}".format(e))
        return ''

a = True

while a:
    print('Esperando ser ativada...')
    command = get_voice_command()
    inp = command.split()
    for word in inp:
        if word == "Olá" or word == "Oi":
            print("O que voce quer?")
            p= get_voice_command(7)
            n = p.split()
            for w in n:
                if w == "primeiro":
                    print('Primeiro andar eh pra ja')
                    time.sleep(3)
                    print('você chegou')
                    time.sleep(3)
                    break
                if w == "segundo":
                    print('Segundo andar eh pra ja') 
                    time.sleep(3)
                    print('Você chegou')
                    time.sleep(3)
                    break
            break