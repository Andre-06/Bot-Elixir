from main import *
from main import client
from functions import *


@client.event
async def on_ready():
    print(f"Bot ON\nUser: {client.user} | Name: {client.user.name} | ID:{client.user.id}")
    try:
        Connector()
    except mysql.connector.errors.InterfaceError:
        print('Conexão não estabelecida')
    else:
        print('Conexão estabelecida')


@client.event
async def on_member_join(member):
    embed = discord.Embed(
        title=f'Olá {member.name} :man_mage:',
        description=f'Seja muito bem vindo ao reino de Impéria, {member.mention}\num lugar mágico criado por <@621664265907994624>.\nSinta-se a vontade para explorar o sevidor.\nQualquer dúvida fique livre para perguntar, \nsempre tem gente online para responder\n',
        color=corConvert('roxo')
    )

    embed.set_author(name=member.guild.name, icon_url=member.guild.icon_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(
        text='Meu criador: Mestre dos magos#0112 (que não ganhou meio centavo pra faze esse bot cof cof mextre cof cof)')
    embed.set_image(
        url="https://media3.giphy.com/media/3oriNPdeu2W1aelciY/giphy.gif?cid=790b7611fe70bf47d18dd4dd5b087742f07aaee586385d44&rid=giphy.gif&ct=g")
    channel = client.get_guild(member.guild.id).get_channel(get(member.guild.text_channels, position=0).id)
    print(channel)
    print(embed)
    await channel.send(embed=embed)
    """
    if member.bot:
      print('não coisou')
      return
    else:
      print('coisou')
      await channel.send(embed=embed)
    """


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content == 'm!xingar <@873979047640711188>':
        await ctx.send('Nao ouse xingar jorginho a lenda, mortal')

    if message.content == 'VAI XINGAR SEU PAI':
        xingamentos = ['você é um cara de mamão', 'você é um bananao', 'você é um fedido, ve se toma um banho',
                       'você é um intrometido, vai varrer uma calçada', 'voce é um bolsonarista',
                       'ado ado ado comi o cu de quem ta marcado',
                       'invejoso morre cedo']
        qualXingamento = random.choice(xingamentos)
        await message.reply(f'QUANTO DESAFORO\n{qualXingamento}')

    if message.content.startswith('.'):
        cRolarAtributos = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA', 'HAB', 'POD', 'PSTR', 'PDEX', 'PCON', 'PINT', 'PWIS', 'PCHA', 'PHAB', 'PPOD']
        try:
            splitado = message.content.upper().replace('.', '').split(' ')

            try:
                if '<@!' in splitado[1]:
                    id = splitado[1].replace('>', '').replace('<@!', '')
            except IndexError: id = message.author.id

            token = idPersonagem(id)

            if splitado[0].lower().startswith('p') and splitado[0].lower() != 'pod':
                pericia = 'p'
                teste = splitado[0][1:][:3].upper()
            else:
                pericia = 'o'
                teste = splitado[0][:3].upper()

            if token[1] == '0':
                await rolagemAtributo(message, token[0], teste, pericia)
            if token[1] == 1:
                await message.reply(token[0])
        except:
            await client.process_commands(message)

    elif message.content.lower().startswith('desv'):
        dado = message.content.lower().replace('desv ', '')

        rolarDado = rolagemTag(dado)
        rolarDado1 = rolagemTag(dado)
        primeiro = rolarDado[1]
        segundo = rolarDado1[1]
        print(f'primeiro: {primeiro}')
        print(f'segundo {segundo}')

        primeiroCtx = rolarDado[0]
        segundoCtx = rolarDado1[0]
        print(f'primeiroCtx: {primeiroCtx}')
        print(f'segundoCtx: {segundoCtx}')

        for i in rolarDado1[2]:
            if '**17**' in str(i):
                segundo = -1000000000000000000
        for i in rolarDado[2]:
            if '**17**' in str(i):
                primeiro = -1000000000000000000

        if segundo < primeiro:
            primeiroCtx = f'~~{primeiroCtx}~~'
        elif primeiro < segundo:
            segundoCtx = f'~~{segundoCtx}~~'

        await message.reply(primeiroCtx + '\n' + segundoCtx)


    elif message.content.lower().startswith('van'):
        dado = message.content.lower().replace('van ', '')

        rolarDado = rolagemTag(dado)
        rolarDado1 = rolagemTag(dado)
        primeiro = rolarDado[1]
        segundo = rolarDado1[1]
        print(f'primeiro: {primeiro}')
        print(f'segundo {segundo}')

        primeiroCtx = rolarDado[0]
        segundoCtx = rolarDado1[0]
        print(f'primeiroCtx: {primeiroCtx}')
        print(f'segundoCtx: {segundoCtx}')

        for i in rolarDado1[2]:
            if '**17**' in str(i):
                segundo = -1000000000000000000
        for i in rolarDado[2]:
            if '**17**' in str(i):
                primeiro = -1000000000000000000

        if segundo > primeiro:
            primeiroCtx = f'~~{primeiroCtx}~~'
        elif primeiro > segundo:
            segundoCtx = f'~~{segundoCtx}~~'

        await message.reply(primeiroCtx + '\n' + segundoCtx)


    elif 'd' in message.content.lower() and len(message.content) <= 32 and any(
            chr.isdigit() for chr in message.content):
        try:
            print('*************** ' + str(message.channel) + ' *****************')
            print('*************** ' + str(message.guild.name) + ' *****************')
            dado = rolagemTag(message.content.lower())[0]
        except ValueError:
            return
        else:
            if message.author.id == 621664265907994624:
                add = ''
            else:
                add = ''
            await message.reply(dado + add, mention_author=True)
