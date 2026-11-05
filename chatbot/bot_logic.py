import os
import random
import discord
import requests

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  # Comando para generar una contraseña
  if message.content.startswith('!password'):
    password = gen_pass(10)
    await message.channel.send(f'Tu contraseña generada es: {password}')

  # La función de emoji aleatorio
  if message.content.startswith('!emoji'):
    emoji = gen_emoji()
    await message.channel.send(emoji)

  # Juego de adivinanzas
  if message.content.startswith('!adivina'):
    try:
      partes = message.content.split()
      if len(partes) < 2:
        await message.channel.send(
            'Debes escribir un numero del 1 al 10. Ejemplo: `!adivina 5`'
        )
        return

      intento_usuario = int(partes[1])
      numero_secreto = random.randint(1, 10)

      if intento_usuario == numero_secreto:
        await message.channel.send(
            f'Felicidades {message.author.mention}! Adivinaste el número'
            f' secreto **{numero_secreto}**.'
        )
      else:
        await message.channel.send(
            f'Lo siento, el numero secreto era **{numero_secreto}**. '
            '¡Inténtalo de nuevo!'
        )
    except ValueError:
      await message.channel.send(
          'Por favor, ingresa un numero valido. Ejemplo: `!adivina 3`'
      )

  # Comando para enviar una imagen aleatoria desde una carpeta 
  if message.content.startswith('!meme'):
    nombre_carpeta = 'images'
    
    if os.path.exists(nombre_carpeta):
      lista_archivos = os.listdir(nombre_carpeta)
      
      if len(lista_archivos) > 0:
        archivo_aleatorio = random.choice(lista_archivos)
        ruta_archivo = os.path.join(nombre_carpeta, archivo_aleatorio)
        
        imagen = discord.File(ruta_archivo)
        await message.channel.send(file=imagen)
      else:
        await message.channel.send('La carpeta de imágenes está vacía.')
    else:
      await message.channel.send(f'No se encontró la carpeta "{nombre_carpeta}".')

  # Comando para enviar una imagen aleatoria de la API del perro
  if message.content.startswith('!perro'):
    try:
      respuesta = requests.get('https://random.dog/woof.json')
      
      if respuesta.status_code == 200:
        datos = respuesta.json()
        url_imagen = datos['url']
        
        await message.channel.send(url_imagen)
      else:
        await message.channel.send('Hubo un error al conectar con la API de perritos.')
    except Exception as e:
      await message.channel.send('Ocurrio un error inesperado al buscar la imagen.')

  #Acciones para cuidar el medio ambiente
  if message.content.startswith('!naturaleza'):
    acciones = [
        "1. **Reduce el uso de plásticos de un solo uso:** Prefiere bolsas de tela y botellas reutilizables.",
        "2. **Ahorra agua:** Cierra el grifo mientras te cepillas los dientes o lavas platos.",
        "3. **Desconecta aparatos que no uses:** Evita el consumo fantasma de energía apagando cargadores.",
        "4. **Separa los residuos:** Recicla correctamente el papel, cartón, plástico y vidrio.",
        "5. **Usa transporte sostenible:** Camina, usa la bicicleta o comparte vehículo siempre que puedas.",
        "6. **Cuida y planta areas verdes:** Fomenta la biodiversidad local cultivando plantas en casa.",
        "7. **Ahorra electricidad:** Apaga las luces de las habitaciones que no estés utilizando.",
        "8. **Consume local y de temporada:** Disminuye la huella de carbono asociada al transporte.",
        "9. **Evita el desperdicio de comida:** Planifica tus compras y aprovecha al máximo los alimentos.",
        "10. **Reutiliza y repara:** Da una segunda oportunidad a los objetos antes de desecharlos."
    ]
client.run("TU_TOKEN_AQUI")
