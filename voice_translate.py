import googletrans
import speech_recognition as sr
from googletrans import Translator
import time
import pyautogui as pg

translator = Translator()
rec = sr.Recognizer()

lang = "en"
count = 0
auto_writing = False
auto_send = False

print("Comandos: \n 1- Ativar envio automático: Ativa modo que pressiona tecla ENTER após a mensagem ser escrita(Apenas com o digitar automático ativo) \n 2- Trocar idioma: Realiza a troca para um novo idioma. \n 3- Parar/Stop: Fecha o programa.")
time.sleep(5)

with sr.Microphone() as mic:
    try:
        rec.adjust_for_ambient_noise(mic)
        print("Deseja digitar automaticamente?(Sim/Não)")
        audio_writing = rec.listen(mic)
        time.sleep(2)
        resposta = rec.recognize_google(audio_writing, language="pt-BR", show_all=True)['alternative'][0]['transcript'].capitalize()
        if resposta == "Sim" or resposta == "Yes":
            auto_writing = True
            print("Função habilitada com sucesso!")
    except:
        print("Não entendi! Escrita automática desabilitada")

time.sleep(1)

with sr.Microphone() as mic:
    while True:
        try:
            rec.adjust_for_ambient_noise(mic)
            print("Ouvindo...")
            audio = rec.listen(mic)
            time.sleep(2)
            fala = rec.recognize_google(audio, language="pt-BR", show_all=True)['alternative'][0]['transcript'].capitalize()
            if fala == "Parar" or fala == "Stop":
                print("Parando operação.")
                break
            if fala == "Trocar idioma" or fala == "Trocar o idioma":
                try:
                    print("Qual o novo idioma?")
                    audio_lang = rec.listen(mic)
                    time.sleep(2)
                    change_lang = rec.recognize_google(audio_lang, language="pt-BR", show_all=True)['alternative'][0]['transcript']
                    traduzido_lang = translator.translate(change_lang, dest="en", src="pt").text.lower()
                    lang = googletrans.LANGCODES[traduzido_lang]
                    print(f"Idioma {change_lang.capitalize()} selecionado com sucesso!")
                    time.sleep(1)
                except:
                    print("Não entendi! Inglês selecionado automáticamente.")
            traduzido = translator.translate(fala, dest=lang, src="pt").text
            if auto_writing:
                if fala == "Ativar envio automático" or fala == "Ativar envio automatico":
                    auto_send = True
                    print("Envio automático habilitado!")
                    continue
                if fala == "Trocar idioma":
                    continue
                time.sleep(3)
                print("Digitando...")
                time.sleep(1)
                pg.write(traduzido.capitalize(), interval=0.25)
                if auto_send:
                    pg.hotkey("enter")
                count = 0
            else:
                if fala == "Trocar idioma":
                    continue
                print(f"A tradução para o {change_lang} é: {traduzido}")
                close = input("Continuar?(S/N): ")
                if close[0].upper() == "S":
                    continue
                else:
                    break
        except:
            count += 1
            if count < 3:
                print("Não entendi, tente novamente!")
                time.sleep(2)
            else:
                print("Limite de tentativas excedido! Verifique: \n- Conexão com a internet \n- Conexão do microfone \n- Lugar barulhento")
                close = input("Continuar?(S/N): ")
                if close[0].upper() == "S":
                    continue
                else:
                    break
