# -------------BIBLIOTECAS---------#
import data_base
from atributos import *
from data_base import *
import events
from connection import *

@client.command(aliases=['r'])
async def roll(ctx, *, dado):
    await ctx.send(rolagemTag(dado))

@client.command()
async def count(ctx, num, *, frase):
    x = 0
    if frase == 'x':
        numM = int(num) + 1
        while x < numM:
            print(x)
            await ctx.send(x)
            x = x + 1
    else:
        numM = int(num) + 1
        while x < numM:
            print(x)
            await ctx.send(frase)
            x = x + 1


@client.command()
async def xingar(ctx, nickA: discord.Member):
    nick = nickA.id
    xingamentos = ['você é um cara de mamão', 'você é um bananao', 'você é um fedido, ve se toma um banho',
                   'você é um intrometido, vai varrer uma calçada', 'voce é um bolsonarista',
                   'ado ado ado olha o gay que ta marcado', 'ado ado ado comi o cu de quem ta marcado',
                   'invejoso morre cedo']
    print(f'nome do xingado {nickA}')
    qualXingamento = None
    if nick == 873979047640711188:
        await ctx.send('Nao ouse xingar jorginho a lenda, mortal')
    else:
        qualXingamento = random.choice(xingamentos)
        await ctx.send(f'{nickA.mention}, {qualXingamento}')


@client.command(help='Comando Para testes')
async def teste(ctx):
    '''
    await ctx.send(ctx.guild.owner)
    members = ctx.guild.members
    for member in members:
      print(member)
      if member.guild_permissions.administrator:
        print('entro')
        await ctx.send(member)
      else:
        print('nn entro')
    '''
    # channel_id = get(ctx.guild.text_channels, position=0)
    # print(ctx.guild.text_channels)
    await  ctx.send('<@873979047640711188>')


@client.command()
async def ficha(ctx, new_token):
    await ctx.send(
        f'Arquivo `"Ficha {new_token}"` criada com sucesso! \nPara adicionar atributos digite o comando `.novo_atributo`, em seguida coloque o nome do seu pernsonagem e o atributo que você quer adicionar(STR, DEX, CON, INT, WIS, CHA, HAB) \n Exemplo: Maugrin HAB=30+10\nPara ver sua ficha use o comando `.verFicha <nome do seu personagem>` ')


@client.command()
async def select(ctx, player: discord.Member, token):
    arq = open('id e personagens.txt', 'a')
    lerArq = open('id e personagens.txt', 'r').readlines()
    print(lerArq)
    count = 0
    loop = False
    while count < len(lerArq):
        if str(player.id) in lerArq[count] or token in lerArq[count]:
            loop = True
            count = count + len(lerArq) + 1
        else:
            count = count + 1
    if loop == True:
        await ctx.reply(
            f'Esse personagem/player ja foi adicionado, para remove-lo e adicionar outro use o comando `.desselect <player>`',
            mention_author=True)
    else:
        lista = list()
        lista.append(f'{token} = {player.id} \n')
        arq.writelines(lista)
        await ctx.send(f'Personagem {token} selecionado para {player.mention}! ')


@client.command()
async def desselect(ctx, player):
    arq = open('id e personagens.txt', 'a')
    lerArq = open('id e personagens.txt', 'r').readlines()
    count = 0
    linha = 'x'
    while count < len(lerArq):
        if str(player) in lerArq[count]:
            linha = count
            count = count + len(lerArq) + 1
        else:
            count = count + 1
    if linha == 'x':
        await ctx.send('Esse player não esta adicionado ou ja foi excluido')
    else:
        excluido = lerArq[linha].split('=')[0]
        arroba = str(lerArq[linha].split('=')[1]).replace(' ', '')
        del (lerArq[linha])
        arq.truncate(0)
        arq.write(''.join(lerArq))
        await ctx.send(f'Personagem {excluido} dessecionado para <@!{arroba}> com sucecesso')


@client.command()
async def selectAtual(ctx, player: discord.Member):
    arq = open('id e personagens.txt', 'a')
    lerArq = lerArq = open('id e personagens.txt', 'r').readlines()
    linha = acharLinha('id e personagens.txt', str(player.id))
    if linha == IndexError:
        await ctx.send('Nenhum personagem selecionado')
    personagem = lerArq[linha].split('=')[0]
    await ctx.send(f'Personagem "{personagem}" selecionado para {player.mention}')


@client.command(aliases=['limpIvt'])
async def limparInventario(ctx, token):
    cursor.execute(f"DELETE FROM inventario WHERE (personagemitem = '{token}')")
    await ctx.send(f'Inventário de {token} foi limpo com sucesso')


@client.command(aliases=['ivt', 'invent', 'addIvt'])
async def inventario(ctx, token, *, item):
    print(token)
    if data_base.val_personagem_existe(token) != True:
        await ctx.send('Insira um personagem válido')
        return

    if '-' in item:
        kilos = item.split('-')[1]
        item = item.split('-')[0]
        id_ = id_name_db(name=token)
        cursor.execute(
            f"INSERT INTO inventario(item, peso, idpersonagem) VALUES ('{item}', '{kilos}', '{id_}')")
        await ctx.send(f'"{item}" adicionado ao inventario de {token}')
    else:
        await ctx.send('Adicone o peso no final do comando depois de um "-"\nExemplo: 3 cadeiras gamer -5')


@client.command(aliases=['ivtR', 'inventR'])
async def inventarioRemove(ctx, token, *, item):
    if val_personagem_existe(token) != True:
        await ctx.send("Insira um personagem válido")

    itemRemovido = data_base.inventario(token, acharItem=item, idinventario=True)
    print(itemRemovido)
    print(f'leght {len(itemRemovido)}')
    if itemRemovido == []:
        await ctx.send('Esse item não existe na ficha')
    idRemovido = itemRemovido[0][1]
    print(idRemovido)
    data_base.script_sql(f'delete from inventario where idinventario = {idRemovido}')
    await ctx.send(f'{str(itemRemovido[0][0])} foi removido com sucesso')


# -------------NOVA ARMA---------#

@client.command(aliases=['atc', 'ataque'])
async def atack(ctx, *, arma):
    print(arma)
    if arma.startswith('<@!'):
        id_ = int(arma.split(" ")[0].replace('<@!', '').replace('>', ''))
        print(id_)
        token = idPersonagem(id_)
        arma = arma.split(' ')[1]
    else:
        token = idPersonagem(ctx.author.id)

    if token[1] == 1:
        await ctx.send(token[0])
    else:
        token = token[0]
    arma = data_base.arma(token, acharArma=arma, dano=True)
    print(arma)
    if arma == []:
        await ctx.send(f"{token}, não reconheci sua arma")

    armaDano = arma[0][1]
    armaMod = ''

    sinal = qualSinal(armaDano)

    if sinal == IndexError:
        armaMod = ''
        sinal = ''
    else:
        armaMod = armaDano.split(sinal)[1]

    validaçãoAtributo = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA', 'HAB', 'POD']
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    print(armaDano)
    print(armaMod)
    print('entro')
    for atb in validaçãoAtributo:
        if str(armaMod).upper().replace(' ', '') in atb and armaMod != '':
            modificador = data_base.atributo_db(armaMod, token, get_mod=True)
            armaDano = armaDano.replace(armaMod, str(modificador))
    print('neeeewwwww')
    print(armaDano)

    rolarDado = rolagem(ctx, armaDano)

    await ctx.reply(f"{token.title()}: {arma[0][0]} = {armaDano}\n{rolarDado[2]}", mention_author=True)

# -------------NOVA ARMA---------#

@client.command(aliases=['addArma', 'novaArma', 'newA'])
async def nova_arma(ctx, token, *, arma):
    id_ = id_name_db(name=token)
    print("ASDKLAJFOAKFNANM FDAOISDFNAIOPHNFAFAPSOJNFA")
    print(id_)
    print("ASDKLAJFOAKFNANM FDAOISDFNAIOPHNFAFAPSOJNFA")
    temDado = False
    temPeso = False
    palavraS = arma.split(' ')
    print(palavraS)
    print(len(palavraS))
    count = 0
    # teste aaa aaa aa 1d20 2
    # 6
    # if len == 6 or == 5
    #
    while len(palavraS) > count:
        palavra = palavraS[count]
        print(f'palavra: {palavra}')
        cNums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        if count >= len(palavraS) - 2 and any(chr.isdigit() for chr in palavra) or 'd' in palavra or '-' in palavra:
            try:
                print(palavra.replace('-', '').split('+')[0])
                rolagem(ctx, palavra.replace('-', '').split('+')[0])
            except (ValueError, IndexError):
                print('deu ruim 1')
                try:
                    peso = int(palavra.replace('-', ''))
                except:
                    print('deu ruim 2')
                else:
                    print('deu bom 2')
                    print(peso)
                    del (palavraS[count])
                    count = count - 1
                    temPeso = True
            else:
                print('deu bom 1')
                dado = palavra.replace('-', '').replace(' ', '')
                del (palavraS[count])
                count = count - 1
                print(palavraS)
                print(dado)
                temDado = True
        else:
            print('nem tinha hifen')
        count = count + 1
    if temPeso == False:
        await ctx.send('Adicone o peso no final do comando\nExemplo: espada 1d6 3')
    elif temDado == False:
        await ctx.send('Adicone o dano no final do comando\nExemplo: espada 1d6 5')
    else:
        palavraS = str(palavraS).replace("'", '').replace(',', '').replace('[', '').replace(']', '')
        print(palavraS)
        armaFicha = f'{palavraS} -{dado} -{peso}'
        print(armaFicha)
        data_base.script_sql(f"INSERT INTO armas(idpersonagem, item, peso, dano) VALUES ('{int(id_)}', '{palavraS}', '{peso}', '{dado}')")
        await ctx.send(f'Nova arma adicionada! {armaFicha}')


@client.command(aliases=['remArma'])
async def armaRemove(ctx, token, arma):
    if data_base.val_personagem_existe(token) != True:
        await ctx.send('Insira um personagem válido')

    armaRem = data_base.arma(token, arma, idarma=True)

    if armaRem == []:
        await ctx.send('Essa arma nao existe ou ja foi excluida')
        return

    try:
        data_base.script_sql(f"DELETE FROM armas WHERE idarmas = {int(armaRem[0][1])} ")
    except FileNotFoundError:
        await  ctx.send("Ocorreu um erro")
        return
    else:
        await ctx.send(f'"{str(armaRem[0][0])}" excluido com sucesso!')


# -------------CRIANDO NOVO ATRIBUTO---------#

@client.command(aliases=['tdsAtb'])
async def todosAtributos(ctx, token, *, atribute):
    atributo = atribute.split('\n')
    count = 0
    while count < len(atributo):
        await novo_atributo(ctx, token, atributo[count])
        count = count + 1


@client.command(aliases=['editTdsAtb'])
async def editarTodosAtributos(ctx, token, *, atribute):
    atributo = atribute.split('\n')
    count = 0
    while count < len(atributo):
        await editar_atributo(ctx, token, atributo[count])
        count = count + 1


@client.command(aliases=['compF'])
async def fichaCompleta(ctx, *, fichaInteira):
    await fichaCompletaCodigo(ctx, fichaInteira, nova=True, editar=False)


@client.command(aliases=['editCompF'])
async def editarFichaCompleta(ctx, *fichaInteira):
    await fichaCompletaCodigo(ctx, fichaInteira, nova=False, editar=True)


@client.command(aliases=['addAtb'])
async def novo_atributo(ctx, token, atribute):
    if '+' in atribute:
        sinal = '+'
        modificador = atribute.split('+')[1]
        quasePntsAtributo = atribute.split('+')[0]
        print(quasePntsAtributo)
        pntsAtributo = quasePntsAtributo.split('=')[1]
    elif '-' in atribute:
        sinal = '-'
        modificador = atribute.split('-')[1]
        quasePntsAtributo = atribute.split('-')[0]
        pntsAtributo = quasePntsAtributo.split('=')[1]
    else:
        sinal = '+'
        modificador = 0
        pntsAtributo = atribute.split('=')[1]

    atributo = atribute[:3].upper()
    print(atributo)
    atributoFicha = f'{atributo} = {pntsAtributo} {sinal} {modificador}'
    try:
        leituraFicha = open(f'ficha {token}.txt', 'r')
    except FileNotFoundError:
        await  ctx.send('Essa ficha ainda não foi criada, use o comando `.ficha <personagem>` para criá-la')
    validaçãoAtributo = str(leituraFicha.readlines())
    print(validaçãoAtributo)
    cAtributos = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA', 'HAB', 'POD']

    if atributo in validaçãoAtributo:
        await ctx.send(f'Esse atributo ja foi adicionado! Caso deseje editá-lo digite o comando `editar_atributo`')
    else:
        if atributo in cAtributos:
            ficha = open(f'ficha {token}.txt', 'a')
            ficha.write(f'{atributoFicha} \n')
            await ctx.send(f'Novo atributo adicionado! {atribute}')
        else:
            await ctx.send(f'Esse atributo não existe, por favor inseira um válido (STR, DEX, CON, INT, WIS, CHA, HAB)')


@client.command()
async def icon_user(ctx, user: discord.Member):
    await ctx.send(user.avatar_url)


@client.command()
async def xp(ctx, token, maisXp, primeiraVez=None):
    if primeiraVez == '!':
        arq = open(f'xp e sanidade {token}.txt', 'a')
        arq.write('XP = 0 \nSANIDADE = 0 \n')
    try:
        arq = open(f'xp e sanidade {token}.txt', 'r')
    except FileNotFoundError:
        await ctx.send(
            'Insira um personagem válido ou coloque "!" (exclamação) ao fim do comando caso seja a primeira vez que adiciona Exposição Mágica a este player\nExemplo: .xp Jorginho +20 !')

    lerArq = arq.readlines()
    xp = int(lerArq[item_lista(lerArq, 'XP')].split('=')[1].replace(' ', '').replace('\n', ''))
    xpNovo = f'XP = {xp + int(maisXp)} \n'
    del (lerArq[item_lista(lerArq, 'XP')])
    lerArq.append(xpNovo)
    print(lerArq)
    arq = open(f'xp e sanidade {token}.txt', 'w')
    arq.truncate(0)
    arq.writelines(''.join(lerArq))
    maisXp = maisXp.replace(" ", "")
    if qualSinal(maisXp) == '+':
        await ctx.send(f"{maisXp} adicionado a Exposição Mágica de {token}")
    elif qualSinal(maisXp) == '-':
        await ctx.send(f"{maisXp} removido a Exposição Mágica de {token}")
    else:
        await ctx.send(f"+{maisXp} adicionado a Exposição Mágica de {token}")


# -------------EDITAR ATRIBUTOS---------#

@client.command(aliases=['editAtb'])
async def editar_atributo(ctx, token, atribute):
    ficha = open(f'ficha {token}.txt', 'r')
    lerFicha = ficha.readlines()
    atributo = str(atribute[:3].upper())
    count = 0
    linhaAttb = 0
    while count < len(lerFicha):
        if atributo in lerFicha[count]:
            print(f'entramos {lerFicha[count]}')
            linhaAttb = count
            count = count + len(lerFicha) + 1
        else:
            print(lerFicha[count])
            count = count + 1

    if '+' in lerFicha[linhaAttb]:
        sinal = '+'
    elif '-' in lerFicha[linhaAttb]:
        sinal = '-'
    else:
        sinal = '+'

    del (lerFicha[linhaAttb])
    arq = open(f'ficha {token}.txt', 'a')
    arq.truncate(0)
    arq.write(''.join(lerFicha))
    await novo_atributo(ctx, token, atribute)
    await ctx.send(f'Atributo {atributo} excluido com sucesso')


# -------------COMANDO PARA ROLAGEM DE CADA ATRIBUTO---------#

@client.command()
async def editarFicha(ctx, token, color, imagem):
    arq = open(f'embedFicha {token}.txt', 'a')
    arq.truncate(0)
    cor = corConvert(color)
    if type(cor) == str:
        await ctx.send(cor)
    else:
        arq.write(f'cor = {cor}\nimagem = {imagem}')
        await ctx.send(f'Cor alterada para {cor}({color}) e imagem alterada para {imagem}')


@client.command()
async def toMember(ctx, iD: discord.Member.id):
    print(iD)
    return iD.nick

@client.command()
async def refresh(ctx):
    set_conection()
    await ctx.send('Conecção estabelecida novamente')

def toMemberCod(iD: discord.Member):
    print(f"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA {iD}")
    return iD


@client.command(aliases=['verF', 'verFicha'])
async def ver_ficha(ctx, token):
    jaEntendi = False
    try:
        id_ = id_name_db(name=token)
    except IndexError:
            await ctx.send('Essa ficha não existe. Para criar uma ficha utilize o comando `.ficha <nome do personagem>`')
            jaEntendi = True

    v = val_personagem_existe(token)
    print(v)
    if v != True and jaEntendi == False:
        await ctx.send('Essa ficha não existe. Para criar uma ficha utilize o comando `.ficha <nome do personagem>`')

    cor = return_fetchall(f'select p.embedCor from personagem as p where idpersonagem = {id_}')[0][0]
    icon = return_fetchall(f'select p.embedIcon from personagem as p where idpersonagem = {id_}')[0][0]

    if icon == 'ctx.guild.icon_url':
        icon = ctx.guild.icon_url

    força = atributo_db('str', id_=id_, get_atb=True)
    modificadorForça = atributo_db('str', token=token, get_mod=True)
    constituicao = atributo_db('con', id_=id_, get_atb=True)
    destreza = atributo_db('dex', token=token, get_atb=True)

    hp = f'HP: {int(constituicao) + int(força)}'
    if int(constituicao) + int(força) > 40:
        hp = f'HP: 40'

    locomoção = round(6 * (int(destreza) / 10) - 0.5, 0)
    print(locomoção)

    cargaMaxima = int(força) + int(modificadorForça)

    embedFicha = discord.Embed(
        title=f'Ficha de {token.title()}\n{hp}\nMovimento: {locomoção}\n',
        description='',
        color=int(cor)
    )

    iconServer = ctx.guild.icon_url
    nome = ctx.guild.name
    embedFicha.set_author(name=nome, icon_url=iconServer)
    embedFicha.set_thumbnail(url=icon)
    # return(nomeAtributo, pntsAtributo, modificadorAtributo, sinal, normal, bom, extremo, emoji, muitoBom, ótimo)

    cAtributos = ['STR', 'DEX', 'CON', 'INTE', 'WIS', 'CHA', 'POD']
    for atb in cAtributos:
        print(atb)
        status = atributosModi(atb, token)
        if status[8] == '':
            valor = f"Normal: {status[4]} | Bom: {status[5]} | Extremo: {status[6]}"
        else:
            valor = f"Normal: {status[4]} | Bom: {status[5]} | Muito Bom: {status[8]}\nÓtimo: {status[9]}    | Extremo: {status[6]}"

        embedFicha.add_field(name=f'{status[7]} {status[0]} {status[1]}{status[3]}{status[2]}', value=valor,
                             inline=False)

    db = return_fetchall(f"""
                        select i.item, i.peso
                        from inventario as i
                        join personagem as p
                        on p.idpersonagem = i.idpersonagem
                        where i.idpersonagem = {id_}
                        """)
    inventario = []
    pesoInventario = [0]
    if db == []:
        inventario.append('Nenhum item adicinado ao inventario')
    else:
        for row in db:
            item = row[0]
            peso = row[1]
            pesoInventario.append(int(peso))
            itemCompleto = f'{item} -{peso}'
            inventario.append(itemCompleto)

    print(inventario)

    db = return_fetchall(f"""
                        select a.item, a.dano, a.peso
                        from armas as a
                        join personagem as p
                        on p.idpersonagem = a.idpersonagem
                        where a.idpersonagem = {id_}""")
    armas = []
    pesoArmas = [0]


    if db == []:
        armas.append('Nenhuma arma adicinada até agora')
    else:
        for row in db:
            item = row[0]
            dano = row[1]
            peso = row[2]
            pesoArmas.append(int(peso))
            itemCompleto = f'{item} -{dano} -{peso}'
            armas.append(itemCompleto)

    if armas == []:
        armas = 'Nenhuma Arma Adicionada'

    pesoTotal = sum(pesoArmas) + sum(pesoInventario)

    embedFicha.add_field(name=f':school_satchel: Inventario {pesoTotal}/{cargaMaxima}', value='\n'.join(inventario), inline=False)
    embedFicha.add_field(name=f':dagger: Armas', value='\n'.join(armas), inline=False)
    await ctx.send(embed=embedFicha)


@client.command(aliases=['iconServer'])
async def icon_server(ctx):
    await ctx.send(ctx.guild.icon_url)


# .ini call, inimigo 1, inimigo 2, bruxas-3
@client.command(aliases=['ini'])
async def iniciativa(ctx, *, iniciativa):
    # cria uma lista com o que passram na iniciativa e seta as variaveis
    jogador = iniciativa.split(',')
    ordem = []
    ordemToNext = list()
    print(jogador)

    # verifica se estao pedindo uma iniciativa com a galera da call
    if 'call' in iniciativa:
        # deleta call da lista e acha a call em que a pessoa esta conectada
        del (jogador[item_lista(jogador, 'call')])
        idCanal = ctx.author.voice.channel.id
        print(idCanal)
        canal = client.get_guild(ctx.guild.id).get_channel(idCanal)
        print(canal.members[3].nick)
        for member in canal.members:
            # ignora se o nick da pessoa nn estiver jogando
            validaçãoEspec = ['MESTRE', 'ESPECTADOR', 'ESPECTANDO', 'OUVINTE', 'OUVINDO']
            if member.nick == None or '|' not in member.nick or 'MESTRE' in member.nick.upper() or 'ESPECTANDO' in member.nick.upper() or 'ESPECTADOR' in member.nick.upper() or 'OUVINTE' in member.nick.upper() or 'OUVINDO' in member.nick.upper():
                a = ''
            else:
                jogador.append(acharNoNick(member.nick, 'nome').replace(' |', '').replace('|', ''))

    # verifica se tem mais de um elemebnto e coloca a quantiade que tiver
    if '-' in iniciativa:
        count = 0
        while count < len(jogador):
            print('AAAAAAAAAAAAAAAAAAA' + jogador[count])
            if '-' in jogador[count]:
                inmigos = jogador[count]
                quantidade = int(jogador[count].split('-')[1])
                print(quantidade)
                countinho = 0
                del (jogador[count])
                while countinho < quantidade:
                    jogador.append(f'{inmigos.split("-")[0]} {countinho + 1}')
                    countinho = countinho + 1
            else:
                count = count + 1

    # remove os espaços que tem no inicio e final
    for player in jogador:
        player = player[:len(player) - 1].replace(' ', '')
        player = player[0:].replace(' ', '')

    # definia a ordem de iniciativa aleatoriamente sem deixar que se repita
    count = 0
    while count < len(jogador):
        alea = random.choice(jogador)
        while f'{alea.title()}, ' in ordem:
            alea = random.choice(jogador)
            print(alea)
        ordem.append(f'{alea.title()}, ')
        ordemToNext.append(f'{alea.title()} \n')
        count = count + 1
        print(ordem)

    # muda o ultimo item para '.' ao inves de ','
    ordem[len(ordem) - 1] = ordem[len(ordem) - 1].replace(',', '.')

    # coloca, em negritro, a ordem de iniciativa no docs
    ordinha = ''.join(ordem)
    arq = open('iniciativa temp.txt', 'a')
    arq.truncate(0)
    celula = ordemToNext[0]
    caracter = len(celula) - 2
    ordemToNext[0] = f'**{celula[:caracter]}** \n'
    arq.writelines(ordemToNext)

    # envia a ordem de iniciativa
    await ctx.reply(f'Ordem de iniciativa: {str(ordinha)}', mention_author=True)


@client.command(aliases=['addIni'])
async def addIniciativa(ctx, *, player):
    arq = open('iniciativa temp.txt', 'a')
    arq.writelines(player + ' \n')
    await ctx.send(player + ' adicionado a iniciativa')


@client.command(aliases=['remIni'])
async def remIniciativa(ctx, *, playerRemove):
    arq = open('iniciativa temp.txt', 'r')
    iniciativa = arq.readlines()
    count = 0
    while count < len(iniciativa):
        print(iniciativa[count].upper())
        print(playerRemove.upper())
        if playerRemove.lower().replace(' ', '') in iniciativa[count].lower().replace(' ', ''):
            if '**' in iniciativa[count]:
                print('tava com **')
                Next(ctx)
                count = count + 1
            else:
                iniciativa[count] = ''
                linha = count
                print(f'linha: {linha}')
                count = count + len(iniciativa) + 2
                print(f'apagado {iniciativa[linha]}')
        else:
            count = count + 1
            print('num achei nn')
    arq2 = open('iniciativa temp.txt', 'w')
    arq2.truncate(0)
    arq2.writelines(iniciativa)
    player = iniciativa[linha].replace('\n', '')
    await ctx.send(f"{player} foi removido")


@client.command()
async def paror(ctx):
    await ctx.send('parorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr meoooooooooooooooooooooooooooo')


@client.command()
async def eéaqui(ctx):
    await ctx.send(
        'E é aqui.........................................................................................................................................................................')


@client.command()
async def deleteFicha(ctx, token):
    deuRuim = 0
    try:
        os.remove(f"ficha {token}.txt")
    except FileNotFoundError:
        await ctx.send(
            f'{token} ja foi para o Pós-Vida ou nunca nem saiu de lá. Por favor selecione um personagem que esteja entre os mortais')
    else:
        try:
            os.remove(f"embedFicha {token}.txt")
        except FileNotFoundError:
            deuRuim = deuRuim + 1
        try:
            os.remove(f"ficha arma {token}.txt")
        except FileNotFoundError:
            deuRuim = deuRuim + 1
        try:
            os.remove(f"inventario {token}.txt")
        except FileNotFoundError:
            deuRuim = deuRuim + 1
        await ctx.send(f'Adeus {token}, que sua jornada ao além seja gloriosa\nPress F for respect')


@client.command()
async def dltF(ctx, token):
    await deleteFicha(ctx, token)


@client.command()
async def hm(ctx):
    await ctx.send(
        'HUMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM')


@client.command()
async def analise(ctx):
    await ctx.send('Ué, Analisekkkkkk')


@client.command()
async def Next(ctx):
    arq = open('iniciativa temp.txt', 'r')
    lerArq = arq.readlines()
    print(lerArq)

    count = 0
    while count < len(lerArq):
        if f"**" in lerArq[count]:
            print(f'entramnos {lerArq[count]}')
            vezAtual = count
            count = count + len(lerArq) + 1
        else:
            print(lerArq[count])
            count = count + 1
            vezAtual = 0

    vezProx = vezAtual + 1
    print(vezAtual)
    lerArq[vezAtual] = lerArq[vezAtual].replace('*', '')
    print(vezProx)
    if vezAtual >= len(lerArq) - 1:
        vezAtual = 0
        vezProx = 0

    celula = lerArq[vezProx]
    caracter = len(celula) - 2
    lerArq[vezProx] = f'**{celula[:caracter]}** \n'
    print(lerArq)
    arq = open('iniciativa temp.txt', 'a')
    count = 0
    ordemToNext = list()
    ordemToNext.append(lerArq)
    arq.truncate(0)
    arq.writelines(lerArq)
    ordem = ''.join(lerArq)
    while count < len(lerArq):
        celula = lerArq[count]
        caracter = len(celula) - 2
        lerArq[count] = f'{celula[:caracter]}, '
        count = count + 1
    print(lerArq)
    lerArq[len(lerArq) - 1] = lerArq[len(lerArq) - 1].replace(',', '.')
    await ctx.reply(
        f"Ordem de Iniciativa: {''.join(lerArq)} \nVez Passada: {''.join(lerArq[vezAtual]).replace(',', '').replace('*', '')}\nVez Atual: {''.join(lerArq[vezProx]).replace(',', '')}",
        mention_author=True)


@client.command(pass_context=True)
async def end(ctx):
    arq = open('iniciativa temp.txt', 'a')
    arq.truncate(0)
    await ctx.send("Combate encerrado")


@client.command(pass_context=True, aliases=['d'])
async def dano(ctx, dado, member: discord.Member):
    print(member)
    rolarDado = rolagem(ctx, dado)
    danoDado = rolarDado[1]
    nickAtual = member.nick

    if "|" in nickAtual:
        partesNick = nickAtual.split('|')
        print(partesNick)
    else:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    # Maugrin Maugrin , 40/40 , f 20/20
    nome = acharNoNick(nickAtual, 'nome')
    hpAtual = acharNoNick(nickAtual, 'hpAtual')
    hpTotal = acharNoNick(nickAtual, 'hpTotal')
    hpSubtraido = int(hpAtual) - int(danoDado)
    hpFinal = f" {hpSubtraido}/{hpTotal}|"
    flechas = acharNoNick(nickAtual, 'flechas')
    mana = acharNoNick(nickAtual, 'mana')

    nickFinal = f"{nome}{hpFinal}{mana}{flechas}"
    print(nickFinal)

    if hpSubtraido < -6:
        await ctx.reply(
            f"**Dano:** {rolarDado[2]} \n **HP:** {hpAtual} - {danoDado} = **{hpSubtraido}**\n*Press F to pay respect*")
    else:
        await ctx.reply(f"**Dano:** {rolarDado[2]} \n **HP:** {hpAtual} - {danoDado} = **{hpSubtraido}**")

    await member.edit(nick=nickFinal)


@client.command(pass_context=True)
async def mute(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 675407695729131527:
        if member.id != ctx.guild.owner.id and member.bot != True:
            await member.edit(mute=True)
            await ctx.send(f'{member.nick} calou a boquinha com sucesso')
    else:
        await ctx.send('Quem você pensa que é?')


@client.command(pass_context=True, aliases=['desmute'])
async def unmute(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 675407695729131527:
        await member.edit(mute=False)
        await ctx.send(f'{member.nick} voltou a falar merda com sucesso')
    else:
        await ctx.send('Quem você pensa que é?')


@client.command(pass_context=True)
async def muteAll(ctx):
    print(ctx.guild.voice_channels)
    canal = discord.utils.get(ctx.guild.voice_channels, id=ctx.author.voice.channel.id)
    print(canal.members)
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 675407695729131527:
        for member in canal.members:
            if member.id != ctx.guild.owner.id and member.bot != True:
                await member.edit(mute=True)
        else:
            await ctx.send('Todo mundo ficou com a boquinha calada')
    else:
        await ctx.send('Quem você pensa que é?')


@client.command(pass_context=True, aliases=['desmuteall'])
async def unmuteAll(ctx):
    canal = discord.utils.get(ctx.guild.voice_channels, id=ctx.author.voice.channel.id)
    if ctx.message.author.guild_permissions.administrator or ctx.message.author.id == 675407695729131527:
        for member in canal.members:
            await member.edit(mute=False)
        else:
            await ctx.send('Todo mundo voltou a falar merda')
    else:
        await ctx.send('Quem você pensa que é?')


"""
  count = 0
  while count < len(canal.members):
    if salvos in member:
      count = count + 1
    else:
      await member.edit(mute=True)
      count = count + 1
"""


@client.command(pass_context=True, aliases=['c'])
async def cura(ctx, dado, member: discord.Member):
    rolarDado = rolagem(ctx, dado)
    danoDado = rolarDado[1]
    nickAtual = member.nick
    if "|" in nickAtual:
        partesNick = nickAtual.split('|')
        print(partesNick)
    else:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    # Maugrin Maugrin , 40/40 , f 20/20
    nome = acharNoNick(nickAtual, 'nome')
    hpAtual = acharNoNick(nickAtual, 'hpAtual')
    hpTotal = acharNoNick(nickAtual, 'hpTotal')
    hpAdicionado = int(hpAtual) + int(danoDado)
    hpFinal = f" {hpAdicionado}/{hpTotal}|"
    mana = acharNoNick(nickAtual, 'mana')
    flechas = acharNoNick(nickAtual, 'flechas')

    nickFinal = f"{nome}{hpFinal}{mana}{flechas}"
    print(nickFinal)

    if int(hpAdicionado) >= int(hpTotal):
        hpFinal = f" {hpTotal}/{hpTotal}|"
        nickFinal = f"{nome}{hpFinal}{mana}{flechas}"
        print(nickFinal)
        await ctx.reply(f"**Cura:** {rolarDado[2]} \n **HP:** {hpAtual} + {danoDado} = **{hpAdicionado}**")
    else:
        await ctx.reply(f"**Cura:** {rolarDado[2]} \n **HP:** {hpAtual} + {danoDado} = **{hpAdicionado}**")

    await member.edit(nick=nickFinal)


@client.command(pass_context=True)
async def hp(ctx, dano, member: discord.Member = None):

    if member == None: member = ctx.author
    nickAtual = member.nick

    if 'd' in dano:
        if dano.startswith('-'):
            dano = dano[1:]
            print(dano)
            sinal = '-'
            rolarDado = rolagemTag(dano)
            danoDado = rolarDado[1] * -1
        else:
            sinal = '+'
            rolarDado = rolagemTag(dano[1:])
            danoDado = rolarDado[1]
        ctxReturn = rolarDado[0]
    else:
        danoDado = eval(dano)
        sinal = qualSinal(str(danoDado))
        if sinal == IndexError: sinal = '+'
        ctxReturn = str(danoDado).replace(sinal, '')

    if "|" in nickAtual:
        partesNick = nickAtual.split('|')
        print(partesNick)
    else:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)f')

    # Maugrin Maugrin , 40/40 , f 20/20
    nome = acharNoNick(nickAtual, 'nome')
    hpAtual = acharNoNick(nickAtual, 'hpAtual')
    hpTotal = acharNoNick(nickAtual, 'hpTotal')
    hpSubtraido = int(hpAtual) + int(danoDado)
    if hpSubtraido > int(hpTotal): hpSubtraido = int(hpTotal)
    hpFinal = f" {hpSubtraido}/{hpTotal}|"
    flechas = acharNoNick(nickAtual, 'flechas')
    mana = acharNoNick(nickAtual, 'mana')

    nickFinal = f"{nome}{hpFinal}{mana}{flechas}"
    if hpSubtraido <= 0:
        await ctx.reply(f"**HP:** {hpAtual} {sinal} {ctxReturn} = **{hpSubtraido}**\n*Press F to pay respect*")
    else:
        await ctx.reply(f"**HP:** {hpAtual} {sinal} {ctxReturn} = **{hpSubtraido}**")

    await member.edit(nick=nickFinal)

@client.command(pass_context=True, aliases=['ml'])
async def magiaLeve(ctx, nick: discord.Member = None):
    print(nick)
    rolarDado = rolagem(ctx, '2d10')
    manaGasta = rolarDado[1]
    c1d6 = [1, 2, 3, 4, 5]
    c1d8 = [6, 7, 8, 9, 10]
    c1d10 = [11, 12, 13, 14, 15]
    c2d8 = [16, 17, 18, 19, 20]
    if manaGasta in c1d6:
        dadoMagia = '1d6'
        estagio = '1/4'
    if manaGasta in c1d8:
        dadoMagia = '1d8'
        estagio = '2/4'
    if manaGasta in c1d10:
        dadoMagia = '1d10'
        estagio = '3/4'
    if manaGasta in c2d8:
        dadoMagia = '2d8'
        estagio = '**4/4**'

    nickAtual = ctx.message.author.nick
    member = ctx.author
    if nick != None:
        print('entrei')
        nickAtual = nick.nick
        member = nick
    try:
        manaAtual = acharNoNick(nickAtual, 'manaAtual')
        manaTotal = acharNoNick(nickAtual, 'manaTotal')
        nome = acharNoNick(nickAtual, 'nome')
        flechas = acharNoNick(nickAtual, 'flechas')
        hp = acharNoNick(nickAtual, 'hp')
    except:
        await ctx.send(
            'Não consegui reconhecer seu nick, verifique se esta no modelo certo: \nNome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    if manaAtual == None or manaTotal == None:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')
        return

    mana = f"{int(manaAtual) - int(manaGasta)}/{manaTotal}|"
    nickFinal = f"{nome}{hp}{mana}{flechas}"
    print(nickFinal)
    await ctx.reply(
        f"Mana Gasta: {rolarDado[2]} \nMana Total: {manaAtual} - {manaGasta} = **{int(manaAtual) - int(manaGasta)}** \nEstágio {estagio} = {dadoMagia}")
    await member.edit(nick=nickFinal)


@client.command(pass_context=True, aliases=['mm'])
async def magiaModerada(ctx, nick: discord.Member = None):
    print(nick)
    rolarDado = rolagem(ctx, '2d30')
    manaGasta = rolarDado[1]

    c1d8 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    c1d10 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    c2d8 = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    c2d10 = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    c2d12 = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    c4d8 = [51, 52, 53, 54, 55, 56]
    c2d20 = [57, 58, 59, 60]
    if manaGasta in c1d8:
        dadoMagia = '1d8'
        estagio = '1/7'
    elif manaGasta in c1d10:
        dadoMagia = '1d10'
        estagio = '2/7'
    elif manaGasta in c2d8:
        dadoMagia = '2d8'
        estagio = '3/7'
    elif manaGasta in c2d10:
        dadoMagia = '2d10'
        estagio = '4/7'
    elif manaGasta in c2d12:
        dadoMagia = '2d12'
        estagio = '5/7'
    elif manaGasta in c4d8:
        dadoMagia = '4d8'
        estagio = '6/7'
    elif manaGasta in c2d20:
        dadoMagia = '2d20'
        estagio = '**7/7**'
    nickAtual = ctx.message.author.nick
    member = ctx.author
    if nick != None:
        nickAtual = nick.nick
        member = nick
    try:
        manaAtual = acharNoNick(nickAtual, 'manaAtual')
        manaTotal = acharNoNick(nickAtual, 'manaTotal')
        nome = acharNoNick(nickAtual, 'nome')
        flechas = acharNoNick(nickAtual, 'flechas')
        hp = acharNoNick(nickAtual, 'hp')
    except:
        await ctx.send(
            'Não consegui reconhecer seu nick, verifique se esta no modelo certo: \nNome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    if manaAtual == None or manaTotal == None:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')
        return

    mana = f"{int(manaAtual) - int(manaGasta)}/{manaTotal}|"

    nickFinal = f"{nome}{hp}{mana}{flechas}"
    print(nickFinal)
    await ctx.reply(
        f"Mana Gasta: {rolarDado[2]} \nMana Total: {manaAtual} - {manaGasta} = **{int(manaAtual) - int(manaGasta)}** \nEstágio {estagio} = {dadoMagia}")
    await member.edit(nick=nickFinal)


@client.command(pass_context=True, aliases=['me'])
async def magiaExtrema(ctx, nick: discord.Member = None):
    rolarDado = rolagem(ctx, '2d50')
    manaGasta = rolarDado[1]

    c2d8menos15 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    c2d12menos10 = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    c2d16menos10 = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    c2d20menos5 = [51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
    c2d20mais5 = [61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
    c2d20mais7 = [71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
    c2d20mais10 = [81, 82, 83, 84, 85, 86, 87, 88, 89]
    c1d50menos15 = [90, 91, 92, 93, 94, 95]
    c1d100menos25 = [96, 97, 98, 99, 100]

    if manaGasta in c2d8menos15:
        dadoMagia = '2d8'
        manaExtrema = 15
        estagio = '1/9'
    elif manaGasta in c2d12menos10:
        dadoMagia = '2d12'
        manaExtrema = 10
        estagio = '2/9'
    elif manaGasta in c2d16menos10:
        dadoMagia = '2d16'
        manaExtrema = 10
        estagio = '3/9'
    elif manaGasta in c2d20menos5:
        dadoMagia = '2d20'
        manaExtrema = 5
        estagio = '4/9'
    elif manaGasta in c2d20mais5:
        dadoMagia = '2d20+5'
        manaExtrema = 0
        estagio = '5/9'
    elif manaGasta in c2d20mais7:
        dadoMagia = '2d20+7'
        manaExtrema = 0
        estagio = '6/9'
    elif manaGasta in c2d20mais10:
        dadoMagia = '2d20+10'
        manaExtrema = 0
        estagio = '7/9'
    elif manaGasta in c1d50menos15:
        dadoMagia = '5d10'
        manaExtrema = 15
        estagio = '8/9'
    elif manaGasta in c1d100menos25:
        dadoMagia = '5d20'
        manaExtrema = 25
        estagio = '**9/9**'

    if manaExtrema == 0:
        streManaExtrema = ''
    else:
        streManaExtrema = f'**- {manaExtrema}**'

    nickAtual = ctx.message.author.nick
    member = ctx.author
    if nick != None:
        nickAtual = nick.nick
        member = nick
    try:
        manaAtual = acharNoNick(nickAtual, 'manaAtual')
        manaTotal = acharNoNick(nickAtual, 'manaTotal')
        nome = acharNoNick(nickAtual, 'nome')
        flechas = acharNoNick(nickAtual, 'flechas')
        hp = acharNoNick(nickAtual, 'hp')
    except:
        await ctx.send(
            'Não consegui reconhecer seu nick, verifique se esta no modelo certo: \nNome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')

    if manaAtual == None or manaTotal == None:
        await ctx.send(
            'Seu nick não esta no formato certo: Nome | HP/HP | Mana/Mana(se tiver mana) | flecha/flecha(se tiver flecha)')
        return

    mana = f" {int(manaAtual) - int(manaGasta) - manaExtrema}/{manaTotal}|"

    nickFinal = f"{nome}{hp}{mana}{flechas}"
    print(nickFinal)
    await ctx.reply(
        f"Mana Gasta: {rolarDado[2]} \nMana Total: {manaAtual} - {manaGasta} {streManaExtrema} = **{int(manaAtual) - int(manaGasta) - manaExtrema}** \nEstágio {estagio} = {dadoMagia}")
    await member.edit(nick=nickFinal)


@client.command()
async def flecha(ctx, quantidade):
    nickAtual = ctx.message.author.nick

    flechaAtual = acharNoNick(nickAtual, 'flechasAtual')
    flechasTotal = acharNoNick(nickAtual, 'flechasTotal')
    nome = acharNoNick(nickAtual, 'nome')
    hp = acharNoNick(nickAtual, 'hp')
    mana = acharNoNick(nickAtual, 'mana')

    flechaOperada = int(flechaAtual) + int(quantidade)
    print(f'flecha operdaa: {flechaOperada}')
    if flechaOperada > int(flechasTotal.replace('f', '')) and int(flechaAtual) >= int(
            flechasTotal.replace('f', '')) and quantidade.count('+') == 1:
        flechaOperada = flechasTotal.replace('f', '')
        await ctx.reply('Sua aljava ja esta cheia')
    elif flechaOperada < 0 and int(flechaAtual) <= 0 and quantidade.count('-') == 1:
        await ctx.reply('Ops, acabaram-se as flechas, taca o arco mesmo')
    else:
        if flechaOperada < 0:
            flechaOperada = 0
        elif flechaOperada > int(flechasTotal.replace('f', '')):
            flechaOperada = int(flechasTotal.replace('f', ''))

        flechaFinal = f' {flechaOperada}/{flechasTotal}'
        nickFinal = f"{nome}{hp}{mana}{flechaFinal}"
        print(nickFinal)
        await ctx.reply(f'{quantidade} flecha na sua aljava\n{flechaAtual}{quantidade} = {flechaOperada}')
        await member.edit(nick=nickFinal)


@client.command()
async def f(ctx, quantidade):
    await flecha(ctx, quantidade)


@client.command()
async def full(ctx, token: discord.Member = ''):
    if token == '':
        nickAtual = ctx.message.author.nick
        nickEditar = ctx.message.author
    else:
        nickAtual = token.nick
        nickEditar = token

    nome = acharNoNick(nickAtual, 'nome')
    hp = acharNoNick(nickAtual, 'hp')
    mana = acharNoNick(nickAtual, 'mana')
    hpAtual = acharNoNick(nickAtual, 'hpAtual')
    hpTotal = acharNoNick(nickAtual, 'hpTotal')
    manaAtual = acharNoNick(nickAtual, 'manaAtual')
    manaTotal = acharNoNick(nickAtual, 'manaTotal')
    flecha = acharNoNick(nickAtual, 'flechas')

    if hp != '' and mana != '':
        nick = f"{nome} {hpTotal.replace(' ', '')}/{hpTotal}| {manaTotal.replace(' ', '')}/{manaTotal}|{flecha}"
        final = f'Elixir esta enchendo sua HP e mana `glub glub glub`\nHP: {hpAtual} + {int(hpTotal) - int(hpAtual)} = {hpTotal}\nMana: {manaAtual} + {int(manaTotal) - int(manaAtual)} = {manaTotal}'
    elif hp != '' and mana == '':
        nick = f"{nome} {hpTotal.replace(' ', '')}/{hpTotal}|{mana}{flecha}"
        final = f'Elixir esta enchendo sua HP `glub glub glub`\nHP: {hpAtual} + {int(hpTotal) - int(hpAtual)} = {hpTotal}'
    elif hp == '' and mana == '':
        nick1 = f'HP e Mana nao estao em seu nick'
        await ctx.send(nick1)
    print(nickEditar)
    try:
        await nickEditar.edit(nick=nick)
    except discord.errors.Forbidden:
        await ctx.send('Sou fraco, me falta permissão')
    else:
        await ctx.reply(final)

"""
@client.command(aliases=['tr'])
async def tdasRolagens(ctx, token: discord.Member = None):
    await stre(ctx, token)
    await dex(ctx, token)
    await con(ctx, token)
    await wis(ctx, token)
    await inte(ctx, token)
    await cha(ctx, token)
    await hab(ctx, token)
    await pstre(ctx, token)
    await pdex(ctx, token)
    await pcon(ctx, token)
    await pwis(ctx, token)
    await pinte(ctx, token)
    await pcha(ctx, token)
    await phab(ctx, token)


# ------------------- TESTES DE ATRIBUTOS ----------------#

# ------------------- TESTES DE PERÍCIA DE ATRIBUTOS ----------------#

@client.command(aliases=['pstr', 'pfor', 'pforça'])
async def pstre(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'stre', 'p')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['pdes', 'pdestreza'])
async def pdex(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'dex', 'p')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['pconstituição'])
async def pcon(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'con', 'p')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['pint', 'pinteligencia'])
async def pinte(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'int', 'p')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['psab', 'psabedoria'])
async def pwis(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'wis', 'p')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['pcarisma', 'pcar'])
async def pcha(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'cha', 'p')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['ppod', 'phabilidade', 'ppoder'])
async def phab(ctx, tokenOp: discord.Member = None):
    if tokenOp == None:
        token = idPersonagem(ctx.author.id)
    else:
        token = idPersonagem(tokenOp.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], 'hab', 'p')
    if token[1] == 1:
        await ctx.send(token[0])

"""

@client.command()
async def van(ctx, teste):
    if teste.lower().startswith('p') and teste.lower() != 'pod':
        pericia = 'p'
        teste = teste[1:][:3].upper()
    else:
        pericia = 'o'
        teste = teste[:3].upper()

    token = idPersonagem(ctx.author.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], teste, pericia, 'sim')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command()
async def desv(ctx, teste):
    if teste.lower().startswith('p') and teste.lower() != 'pod':
        pericia = 'p'
        teste = teste[1:][:3].upper()
    else:
        pericia = 'o'
        teste = teste[:3].upper()

    token = idPersonagem(ctx.author.id)
    if token[1] == '0':
        await rolagemAtributo(ctx, token[0], teste, pericia, 'no', 'sim')
    if token[1] == 1:
        await ctx.send(token[0])


@client.command(aliases=['s'])
async def sorte(ctx):
    coiso = rolagem(ctx, '1d20')
    dado = int(coiso[1])
    dadoRolagem = coiso[2]
    if dado >= 10:
        await ctx.reply(f'Teste de Sorte\n\nSucesso | {dadoRolagem}', mention_author=True)
    elif dado < 10:
        await ctx.reply(f'Teste de Sorte\n\nFracasso | {dadoRolagem}', mention_author=True)
    else:
        await ctx.reply('uékkkkkk', mention_author=True)


@client.command()
async def calc(ctx, *, conta):
    await ctx.send(f'{conta} = `{eval(conta)}`')


@client.command(aliases=['cMamada'])
async def countMamada(ctx, num):
    arq = open('contador de mamadas.txt', 'a')
    read = open('contador de mamadas.txt', 'r').readlines()
    arq.truncate(0)
    print(read)
    print(num)
    print(int(read[0]) + int(num.replace('+', '').replace('-', '')))
    arq.write(str(int(read[0]) + int(num)))
    await ctx.send(f'Contador de Mamadas: {int(read[0]) + int(num)}')


@client.command()
async def invite(ctx):
    await ctx.send(
        'Convide o Elixir para seu servidor com este link\nhttps://discord.com/api/oauth2/authorize?client_id=873979047640711188&permissions=8&scope=bot')


@client.command()
async def novaMesa(ctx, *, todos):
    guild = ctx.guild
    guildSend = client.get_guild(ctx.guild.id)

    todosA = todos.split(', ')
    print(todosA)
    campanha = todosA[0]
    print(campanha)
    qntPlayer = acharItemNaLista('personage', todosA)
    print(qntPlayer)
    tipoFicha = acharItemNaLista('magia', todosA)
    print(tipoFicha)
    try:
        qntPlayer = int(qntPlayer.split(' ')[0])
    except ValueError:
        qntPlayer = int(qntPlayer.split(' ')[1])
    except AttributeError:
        qntPlayer = acharItemNaLista('play', todosA)
        try:
            qntPlayer = int(qntPlayer.split(' ')[0])
        except ValueError:
            qntPlayer = int(qntPlayer.split(' ')[1])
    print(qntPlayer)
    if tipoFicha == None:
        ficha = """NOME:
IDADE:
JOGADOR: @
GENERO:
ex. magica:
.
atributos;
Força:
Destreza:
Constituição:
Inteligencia:
sabedoria:
carisma:
poder:
.
============
.
pericias:
.
============
.
mandato (tipo do mandato):
.
===========
.
Aparencia;
Cor do olhos:
Cor da pele:
Cor cabelo:
altura:
Roupa completa/vestimentas:
.
.
.
bag/mochila (item -peso);
. 
.
.
armas (arma -dano -peso):
.
.
.
Personalidade:
.
.
.
back hitory:"""
    if 'com magia' in tipoFicha:
        ficha = """NOME:
IDADE:
JOGADOR:
GENERO:
.
.
atributos;
Força:
Destreza:
Constituição:
Inteligencia:
sabedoria:
carisma:
uso magico:
.
mandato:
.
Aparencia;
Cor do olhos:
Cor da pele:
Cor cabelo:
Roupa completa/vestimentas:
Acessórios:
.
.
.
bag/mochila;
. 
.
.

Personalidade:"""
    elif 'sem magia' in tipoFicha:
        ficha = """NOME:
IDADE:
JOGADOR:
GENERO:
.
.
atributos;
Força:
Destreza:
Constituição:
Inteligencia:
sabedoria:
carisma:
uso de armas:
.
.
.
Aparencia;
Cor do olhos:
Cor da pele:
Cor cabelo:
Roupa completa/vestimentas:
Acessórios:
.
.
.
bag/mochila;
. 
.
.

Personalidade:"""
    else:
        await ctx.send(
            'Você não definiu o tipo da ficha, ao final do comando coloque "com magia" para fichas mágicas e "sem magia" para fichas não mágicas. **POR FAVOR CERTIFIQUE QUE VOCÊ BOTO CERTINHO O "com magia" OU "sem magia" DO JEITINHO QUE EU FALEI**')

    try:
        ficha
    except NameError:
        return
    else:
        await guild.create_category(name=campanha, position=7)
        categoriaCampanha = get(ctx.guild.categories, name=campanha)
        count = 0
        while count < qntPlayer:
            await guild.create_text_channel(name=f'personagem-{count + 1}', category=categoriaCampanha)
            channel_id = get(guild.text_channels, name=f'personagem-{count + 1}')
            print(channel_id)
            channel = client.get_guild(ctx.guild.id).get_channel(channel_id.id)
            await channel.send(ficha)
            count += 1
        await ctx.send(
            f'Nova Campanha: **{campanha}** foi criada com sucesso. {qntPlayer} modelos de fichas novas foram enviados ')


@client.command()
async def petição(ctx, *, peticao):
    msg = await ctx.send(f"@everyone {peticao}")
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')


@client.command()
async def RELIQUIAS(ctx):
    await ctx.send('ELE DISSE RELIQUIAS???????????????')

def comando(ctx, helpComando):
    return ctx.send('aaaaa')


@client.command()
async def help(ctx, helpComando=None):
    def secao1():
        embedFicha = discord.Embed(
            title=f'Elixir Comandos\nSeção {1}/{6}:',
            description='',
            color=6950317
        )

        icon = ctx.guild.icon_url
        nome = ctx.guild.name
        embedFicha.set_author(name=nome, icon_url=icon)
        embedFicha.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/812327180423921684/882275900215922729/garrafa-do-amor-C3ADcone-jogo-elixir-mC3A1gico-relaC3A7C3A3o-para-o-rpg-ou-match-variaC3A7C3A3o-gran.png')

        embedFicha.add_field(name='.ficha <personagem>', value='Cria a ficha de um personagem', inline=False)
        embedFicha.add_field(name='.deleteFicha <personagem>',
                             value='Deleta a ficha de um personagem\nAbreivações: dltF', inline=False)
        embedFicha.add_field(name='.ver_Ficha <personagem>',
                             value='Mostra a ficha do personagem\nAbreviações: .verFicha, .verF', inline=False)
        embedFicha.add_field(name='.todosAtributos <personagem> <atributos>',
                             value='Adiciona todos os atributos de uma vez. Os atributos devem ser seprados por enters\nAbreviações: .tdsAtb',
                             inline=False)
        embedFicha.add_field(name='.editarTodosAtributos <personagem> <atributos>',
                             value='Edita todos os atributos de uma vez. Os atributos devem ser seprados por enters\nAbreviações: .editTdsAtb',
                             inline=False)
        embedFicha.add_field(name='.genFicha <personagem>', value='Gera uma ficha aleatória', inline=False)
        embedFicha.add_field(name='.novo_atributo <personagem> <atributo>',
                             value='Adiciona um atributo ao personagem. Exemplo: .novo_atributo Maugirn DEX=20+5\nAbreviações: .addAtb',
                             inline=False)
        embedFicha.add_field(name='.editar_atributo <personagem> <atributo>',
                             value='Subistitui o atributo pelo o novo. Exemplo: .novo_atributo Maugirn DEX=20+5\nAbreviações: .editAtb',
                             inline=False)
        embedFicha.add_field(name='.editarFicha <personagem> <cor> <url da imagem>',
                             value='Subistitui a cor e a imagem padrão da ficha pelas novas', inline=False)

        return embedFicha

    def secao2():
        embedFicha = discord.Embed(
            title=f'Elixir Comandos\nSeção {2}/{6}:',
            description='',
            color=6950317
        )

        icon = ctx.guild.icon_url
        nome = ctx.guild.name
        embedFicha.set_author(name=nome, icon_url=icon)
        embedFicha.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/812327180423921684/882275900215922729/garrafa-do-amor-C3ADcone-jogo-elixir-mC3A1gico-relaC3A7C3A3o-para-o-rpg-ou-match-variaC3A7C3A3o-gran.png')

        embedFicha.add_field(name='.inventario <personagem> <item> <-peso>',
                             value='Adiciona itens ao seu inventario\nAbreviações: .invent, .ivt', inline=False)
        embedFicha.add_field(name='.inventarioRemove <personagem> <posição do item>',
                             value='Remove um item\nAbreviações: .inventR, .ivtR', inline=False)
        embedFicha.add_field(name='.nova_arma <personagem> <arma> <-dado de dano> <-peso>',
                             value='Adiciona uma arma ao seu inventario\nAbreviações: .newA', inline=False)
        embedFicha.add_field(name='.armaRemove <personagem> <arma>', value='Remove uma arma do personagem',
                             inline=False)
        embedFicha.add_field(name='.subtrairItem <personagem> <quantidade> <item>',
                             value='Subtrair uma quantidade de vezes o item\nAbreviações: .sub', inline=False)
        embedFicha.add_field(name='.adicionarItem <personagem> <quantidade> <item>',
                             value='Adiciona uma quantidade de vezes o item\nAbreviações: .add ', inline=False)
        return embedFicha

    def secao3():
        embedFicha = discord.Embed(
            title=f'Elixir Comandos\nSeção {3}/{6}:',
            description='',
            color=6950317
        )

        icon = ctx.guild.icon_url
        nome = ctx.guild.name
        embedFicha.set_author(name=nome, icon_url=icon)
        embedFicha.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/812327180423921684/882275900215922729/garrafa-do-amor-C3ADcone-jogo-elixir-mC3A1gico-relaC3A7C3A3o-para-o-rpg-ou-match-variaC3A7C3A3o-gran.png')

        embedFicha.add_field(name='.select <@player> <personagem>', value='Selciona um personagem para o player',
                             inline=False)
        embedFicha.add_field(name='.desselect <personagem>',
                             value='Desseleciona o personagem para o player ', inline=False)
        embedFicha.add_field(name='.selectAtual <@player>', value='Mostra o personagem selecionado pare o player',
                             inline=False)
        embedFicha.add_field(name='.atack <arma>', value='Da um atack com a arma', inline=False)
        embedFicha.add_field(name='.iniciativa <players> <inimigos-quantidade>',
                             value='Rola uma ordem de iniciativa aleatória. Exemplo: .iniciativa player1,player2,player3 inimigos-4',
                             inline=False)
        embedFicha.add_field(name='.next', value='Mostra o próximo na ordem de iniciativa', inline=False)
        embedFicha.add_field(name='.end', value='Encerra a iniciativa', inline=False)
        return embedFicha

    def secao4():
        embedFicha = discord.Embed(
            title=f'Elixir Comandos\nSeção {4}/{6}:',
            description='',
            color=6950317
        )

        icon = ctx.guild.icon_url
        nome = ctx.guild.name
        embedFicha.set_author(name=nome, icon_url=icon)
        embedFicha.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/812327180423921684/882275900215922729/garrafa-do-amor-C3ADcone-jogo-elixir-mC3A1gico-relaC3A7C3A3o-para-o-rpg-ou-match-variaC3A7C3A3o-gran.png')

        embedFicha.add_field(name='.cura <dado> <@player>',
                             value='Rola um dado de cura e altera no nick\nAbreviações: .c', inline=False)
        embedFicha.add_field(name='.curaCheia <valor> <@player>',
                             value='Adiciona uma valor de cura ao seu nick\nAbreviações: .ch', inline=False)
        embedFicha.add_field(name='.dano <dado> <@player>',
                             value='Rola um dado de dano e altera no nick\nAbreviações: .d', inline=False)
        embedFicha.add_field(name='.danoCheio <valor> <@player>',
                             value='Adiciona uma valor de dano ao seu nick\nAbreviações: .dc', inline=False)
        embedFicha.add_field(name='.magiaLeve',
                             value='Rola o 2d10 de magia, tira a mana de seu nick e mostra o dado de dano que deu\nAbreviações: .ml',
                             inline=False)
        embedFicha.add_field(name='.magiaModerada',
                             value='Rola o 2d30 de magia, tira a mana de seu nick e mostra o dado de dano que deu\nAbreviações: .mm',
                             inline=False)
        embedFicha.add_field(name='.magiaExtrema',
                             value='Rola o 2d50 de magia, tira a mana de seu nick e mostra o dado de dano que deu\nAbreviações: .me',
                             inline=False)
        embedFicha.add_field(name='.full <@player>', value='Coloca a vida e a mana(se tiver) no máximo', inline=False)

        return embedFicha

    def secao5():
        embedFicha = discord.Embed(
            title=f'Elixir Comandos\nSeção {5}/{6}:',
            description='',
            color=6950317
        )

        icon = ctx.guild.icon_url
        nome = ctx.guild.name
        embedFicha.set_author(name=nome, icon_url=icon)
        embedFicha.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/812327180423921684/882275900215922729/garrafa-do-amor-C3ADcone-jogo-elixir-mC3A1gico-relaC3A7C3A3o-para-o-rpg-ou-match-variaC3A7C3A3o-gran.png')

        embedFicha.add_field(name='Abreviações Atributos', value='int, dex, con, hab, cha, stre, wis', inline=False)
        embedFicha.add_field(name='Rolagens Dos Atributos',
                             value='Coloque .<abreviação> para rolar um teste de seu atributo', inline=False)
        embedFicha.add_field(name='Rolagens De Pericias',
                             value='Coloque .p<abeviação> para rolar uma um teste de seu atributo com o bonus de perícia ',
                             inline=False)
        embedFicha.add_field(name='.forçarRolagem <personagem> <atributo>',
                             value='Rola um teste de um atributo de um persongem\nAbreviações: .forR', inline=False)
        embedFicha.add_field(name='.forçarRolagemPericia <personagem> <atributo>',
                             value='Rola um teste de perícia de um persongem\nAbreviações: .forRP', inline=False)
        embedFicha.add_field(name='.roll <dado>', value='Rola um dado\nAbreviações: .r', inline=False)
        embedFicha.add_field(name='.sorte', value='Faz um teste de sorte', inline=False)
        return embedFicha

    def secao6():
        embedFicha = discord.Embed(
            title=f'Elixir Comandos\nSeção {6}/{6}:',
            description='',
            color=6950317
        )

        icon = ctx.guild.icon_url
        nome = ctx.guild.name
        embedFicha.set_author(name=nome, icon_url=icon)
        embedFicha.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/812327180423921684/882275900215922729/garrafa-do-amor-C3ADcone-jogo-elixir-mC3A1gico-relaC3A7C3A3o-para-o-rpg-ou-match-variaC3A7C3A3o-gran.png')

        embedFicha.add_field(name='.analise', value='Faz uma analise apurada da situação', inline=False)
        embedFicha.add_field(name='.eéaqui', value='Acaba com a seção e infarta os players', inline=False)
        embedFicha.add_field(name='.count <numero de vezes> <mensagem>', value='Este comando repete uma mesma messagem',
                             inline=False)
        embedFicha.add_field(name='.xingar <@do xingado>', value='Xinga a pessoa', inline=False)
        embedFicha.add_field(name='.hm', value='HUMMMMMMMMMMMMMMMMM', inline=False)
        embedFicha.add_field(name='.icon', value='Mostra o icone do servidor', inline=False)
        embedFicha.add_field(name='.paror', value='para com tudo', inline=False)
        embedFicha.add_field(name='.reliquias', value='Confirma se ele disse reliquias', inline=False)
        embedFicha.add_field(name='.petição <frase>', value='Cria uma petição', inline=False)
        embedFicha.add_field(name='.calc <conta>', value='Realiza uma conta', inline=False)

        return embedFicha

    pages = 6
    cur_page = 1

    contents = [secao1(), secao2(), secao3(), secao4(), secao5(), secao6()]

    message = await ctx.send(embed=contents[0])
    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)

            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                print(cur_page - 1)
                embedFicha = contents[cur_page - 1]
                await message.edit(embed=embedFicha)
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                embedFicha = contents[cur_page - 1]
                await message.edit(embed=embedFicha)
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)

        except:
            await message.delete()


TOKEN = key.get_token()

client.run(TOKEN)
