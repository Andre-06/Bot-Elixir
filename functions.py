import data_base
from main import *
import random
from bot_commands import *
from data_base import *


def rolagemTag(dado):

    dado = dado.replace(" ", '')
    finalFinal = []
    resultadoFinal = []
    monteDeDadosSFinal = []
    limite = f"` XXXX ` ⟵  [Limite Alcançado]"

    if '#' in dado:
        rollSeparado = int(dado.split("#")[0])
        dado = dado.split('#')[1]
        if rollSeparado > 100: return limite
    else:
        rollSeparado = 1

    for i in range(0, rollSeparado):

        ###################### PRIMEIRA PARTE SÓ ############

        dadoS = []
        dadoM = []
        soma = []
        min = []

        dados = dado.split('+')
        print(f'dados: {dados}')
        for d in dados:
            print(f'd: {d}')
            if 'd' in d and '-' not in d:
                print('entrou 1: dado puro')
                dadoS.append(d)
            elif '-' in d:
                newDados = d.split('-')
                print(f'newDados: {newDados}')
                if 'd' in newDados[0]:
                    print('entrou 2: primeiro dado do split -')
                    dadoS.append(newDados[0])
                elif newDados[0] != '':
                    print('entrou 3: primeiro numero do split -')
                    soma.append(int(d.split('-')[0]))
                del(newDados[0])
                print(f"newDados new: {newDados}")
                for newD in newDados:
                    print(f'newD: {newD}')
                    if newD == '':
                        print('entrou 4: vazio antes do split -')
                        pass
                    elif 'd' in newD:
                        print('entrou 5: dado puro negativo')
                        dadoM.append(newD)
                    else:
                        print('entrou 6: numero negativo')
                        min.append(int(newD))
            else:
                print('entrou 7: numero positivo')
                soma.append(int(d))

        if len(dadoS) > 10 or len(dadoM) > 10:
            return limite

        #######################   ROLAGEM RANDOMICA   ######################

        monteDeDadosS = []
        monteDeDadosM = []

        if dadoS != []:
            for d in dadoS:
                qntD = d.split('d')[0]
                if qntD == '': qntD = 1
                else: qntD = int(qntD)
                numD = int(d.split('d')[1])

                if qntD > 100 or numD > 500: return limite

                for i in range(0, qntD):
                    ran = random.randint(1, numD)
                    if ran == numD:
                        monteDeDadosS.append(ran + 10000)
                    else:
                        monteDeDadosS.append(ran)
            else:
                monteDeDadosS.sort(reverse=True)

        if dadoM != []:
            for d in dadoM:
                qntD = d.split('d')[0]
                if qntD == '': qntD = 1
                else: qntD = int(qntD)
                numD = int(d.split('d')[1])

                if qntD > 100 or numD > 500: return limite

                for i in range(0, qntD):
                    ran = random.randint(1, numD)
                    if ran == numD:
                        monteDeDadosM.append(ran + 10000)
                    else:
                        monteDeDadosM.append(ran)
            else:
                monteDeDadosM.sort(reverse=True)

        print(f'monteDeDadosS: {monteDeDadosS}')
        print(f'monteDeDadosM: {monteDeDadosM}')
        print(f'sum: {soma}')
        print(f'min: {min}')

        #######################  TOTAIS  ######################

        totalS = 0
        for i in monteDeDadosS:
            if i > 10000:
                totalS = totalS + i - 10000
            else:
                totalS = totalS + i

        totalM = 0
        for i in monteDeDadosM:
            if i > 10000:
                totalM = totalM + i - 10000
            else:
                totalM = totalM + i

        totalSum = sum(soma)

        totalMin = sum(min)

        resultado = totalS - totalM + totalSum - totalMin

        #######################  STR DO SUM E MIN  ######################

        sumStrComp = []
        if soma == []:
            sumStrComp = ''
        else:
            for i in soma:
                sumStrComp.append(str(i))

        minStrComp = []
        if min == []:
            minStrComp = ''
        else:
            for i in min:
                minStrComp.append(str(i))

        #######################  EXTREMO DESASTRE  ######################

        count = 0
        while count < len(monteDeDadosM):
            i = monteDeDadosM[count]
            try:
                if i > 10000:
                    monteDeDadosM[count] = '**' + str(i - 10000) + '**'
                elif i == 17 or i == 1:
                    monteDeDadosM[count] = '**' + str(i) + '**'
            except TypeError:
                pass
            count = count + 1

        count = 0
        while count < len(monteDeDadosS):
            i = monteDeDadosS[count]
            try:
                if i > 10000:
                    monteDeDadosS[count] = '**' + str(i - 10000) + '**'
                elif i == 17 or i == 1:
                    monteDeDadosS[count] = '**' + str(i) + '**'
            except TypeError:
                pass
            count = count + 1

        #######################  FINALIZAÇÕES  ######################

        if totalSum != 0:
            finalSoma = f" + {' + '.join(sumStrComp)}"
        else:
            finalSoma = ''

        if totalMin != 0:
            finalMenos = f" - {' - '.join(minStrComp)}"
        else:
            finalMenos = ''

        if totalM != 0:
            finalDadosNegativos = f" - {monteDeDadosM} {'-'.join(dadoM)}"
        else:
            finalDadosNegativos = ''

        if totalS != 0:
            finalBasico = f"{monteDeDadosS} {'+'.join(dadoS)}"
        else:
            finalBasico = ''

        final = f"` {resultado} ` ⟵  " + finalBasico + finalDadosNegativos + finalSoma + finalMenos
        resultadoFinal.append(resultado)
        monteDeDadosSFinal.append(monteDeDadosS)
        finalFinal.append(final)

    return('\n'.join(finalFinal), sum(resultadoFinal), monteDeDadosSFinal)

def sum(list_):
    total = 0
    for i in list_:
        total = total + i
    else:
        return total

def rolagem(ctx, dado):
    print(ctx)
    if '+' in dado:
        posicao = dado.split('d')
        print(posicao)
        print(posicao[0])
        print(posicao[1])
        separa = posicao[1].split('+')
        soma = int(separa[1])
        x = posicao[0]
        if x == '':
            x = 1
        else:
            x = int(x)
        y = int(separa[0])
        print(type(x))
        print(x)
        if x > 100:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        elif y > 300:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        else:
            count = 0
            maisDeUmDado = 0
            todosOsDados = []
            while x > count:
                deu = random.randint(1, y)
                maisDeUmDado = maisDeUmDado + deu
                todosOsDados.append(deu)
                count = count + 1
                print(todosOsDados)

        resultado = maisDeUmDado + soma
        print(separa)


    elif '-' in dado:
        posicao = dado.split('d')
        separa = posicao[1].split('-')
        soma = int(separa[1])
        x = posicao[0]
        if x == '':
            x = 1
        else:
            x = int(x)
        y = int(separa[0])
        if x > 100:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        elif y > 300:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        else:
            count = 0
            maisDeUmDado = 0
            todosOsDados = []
            while x > count:
                deu = random.randint(1, y)
                maisDeUmDado = maisDeUmDado + deu
                todosOsDados.append(deu)
                count = count + 1
                print(todosOsDados)

        resultado = int(maisDeUmDado) - soma
        print(separa)

    else:
        soma = 0
        posicao = dado.split('d')
        x = posicao[0]
        if x == '':
            x = 1
        else:
            x = int(x)
        y = int(posicao[1])
        if x > 100:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        elif y > 300:
            resultado = 'XXXX'
            todosOsDados = '[Limite Alcançado]'
        else:
            count = 0
            maisDeUmDado = 0
            todosOsDados = []
            while count < x:
                deu = random.randint(1, y)
                maisDeUmDado = maisDeUmDado + deu

                todosOsDados.append(deu)
                count = count + 1
                print(todosOsDados)
            resultado = int(maisDeUmDado)

    if ctx != '1':
        print(posicao)
        if type(todosOsDados) == str:
            final = f"` {resultado} ` ⟵ {todosOsDados} {dado}"
            finalNal = ctx.reply(final, mention_author=True)
            return (finalNal, resultado, final, deu)
        else:
            todosOsDados.sort(reverse=True)
            print(todosOsDados)
            count = 0
            while count < len(todosOsDados):
                if todosOsDados[count] == 1 or todosOsDados[count] == y or todosOsDados[count] == 17:
                    todosOsDados[count] = f'**{todosOsDados[count]}**'
                    print(todosOsDados[count])
                else:
                    count = count + 1
            final = f"` {resultado} ` ⟵ {todosOsDados} {dado}"
            finalNal = ctx.reply(final, mention_author=True)
            return (finalNal, resultado, final, todosOsDados, maisDeUmDado)
    if ctx == '1':
        print(posicao)
        if type(todosOsDados) == str:
            final = f"` {resultado} ` ⟵ {todosOsDados} {dado}"
            return (resultado, final, deu)
        else:
            todosOsDados.sort(reverse=True)
            print(todosOsDados)
            count = 0
            while count < len(todosOsDados):
                if todosOsDados[count] == 1 or todosOsDados[count] == y or todosOsDados[count] == 17:
                    todosOsDados[count] = f'**{todosOsDados[count]}**'
                    print(todosOsDados[count])
                else:
                    count = count + 1
            final = f"` {resultado} ` ⟵ {todosOsDados} {dado}"
            return (resultado, final, todosOsDados, maisDeUmDado)


def acharLinha(arquivo, variavel):
    lerArq = open(arquivo, 'r').readlines()
    count = 0
    while count < len(lerArq):
        if variavel in lerArq[count]:
            return count
            count = count + len(lerArq) + 1
        else:
            count = count + 1
    return IndexError


def item_lista(lista, itemAchar):
    count = 0
    for item in lista:
        if str(itemAchar).lower() in str(item).lower():
            return count
        else:
            count = count + 1
    else:
        return IndexError


def qualSinal(atribute):
    if '+' in atribute and '-' in atribute:
        return 'Ih rapaz'
    elif '+' in atribute:
        return '+'
    elif '-' in atribute:
        return '-'
    elif '>' in atribute:
        return '>'
    elif '<' in atribute:
        return '<'
    elif '+' in atribute:
        return '+'
    elif '*' in atribute:
        return '*'
    elif '/' in atribute:
        return '/'
    elif '^' in atribute:
        return '^'
    else:
        return IndexError


def acharAtributo(player, atributo):
    arq = open(f'ficha {player}.txt', 'r')
    ficha = arq.readlines()
    for atributoFicha in ficha:
        if atributo.upper() in atributoFicha.upper():
            return atributoFicha
        else:
            pass


def id_by_name(name_channel, guild):
    for channel in guild:
        print(channel.name)
        if channel.name == name_channel:
            return channel.id
            print(channel.id)


def corConvert(color):
    if color == 'verde':
        cor = 32768
    elif color == 'azul':
        cor = 255
    elif color == 'roxo':
        cor = 6950317
    elif color == 'rosa':
        cor = 16718146
    elif color == 'preto':
        cor = 000000
    elif color == 'branco':
        cor = 16777215
    elif color == 'laranja':
        cor = 16753920
    elif color == 'amarelo':
        cor = 16776960
    elif color == 'vermelho':
        cor = 16711680
    elif color == 'ciano':
        cor = 3801067

    else:
        cor = 'Desculpe, não achei essa cor. Tente colocar o código decimal. \nSite para a conversão de decimal: https://convertingcolors.com/'

    return cor


def acharNoNick(nick, achar):
    print('---INICIO-----------INICIO-------------INICIO--------------------INICIO---------')

    if "|" in nick:
        partesNick = nick.split('|')
        print(partesNick)
    elif 'I' in nick:
        partesNick = nick.split('I')
        print(partesNick)
    elif 'l' in nick:
        partesNick = nick.split('l')
        print(partesNick)
    else:
        return None

    # Maugrin Maugrin , 40/40 , f 20/20
    nome = partesNick[0] + '|'
    hp = partesNick[1] + '|'
    hpAtual = partesNick[1].split('/')[0]
    hpTotal = partesNick[1].split('/')[1]
    flechas = ''
    flechasAtual = ''
    flechasTotal = ''
    manaTotal = ''
    manaAtual = ''
    mana = ''

    count = 0
    while count < len(partesNick):
        print(f"parte do nick analisado: {partesNick[count]}")
        if partesNick[count].replace(' ', '') == '':
            del (partesNick[count])
            print(f'nick tava vazio')
            count = count + 1
        else:
            print(f'nick nn tava vaio')
            count = count + 1

    if len(partesNick) == 3:
        # Maugrin Maugrin , 40/40 , 500/500
        # Maugrin Maugrin , 40/40 , f 20/20

        if 'f' in partesNick[2]:
            # Maugrin Maugrin , 40/40 , f 20/20
            flechas = partesNick[2]
            flechasAtual = partesNick[2].split('/')[0]
            flechasTotal = partesNick[2].split('/')[1]
        else:
            # Maugrin Maugrin , 40/40 , 500/500
            mana = partesNick[2]
            manaAtual = partesNick[2].split('/')[0]
            manaTotal = partesNick[2].split('/')[1]

    elif len(partesNick) == 4:
        # Maugrin Maugrin , 40/40 , 500/500 , f 20/20

        mana = partesNick[2] + '|'
        manaAtual = partesNick[2].split('/')[0]
        manaTotal = partesNick[2].split('/')[1]
        flechas = partesNick[3]
        flechasAtual = partesNick[3].split('/')[0]
        flechasTotal = partesNick[3].split('/')[1]

    nickFinal = f"{nome}{hp}{mana}{flechas}"
    print(f"nome: {nome}")
    print(f"hp: {hp}")
    print(f"hpAtual: {hpAtual}")
    print(f"hpTotal: {hpTotal}")
    print(f"flechas: {flechas}")
    print(f"flechasAtual: {flechasAtual}")
    print(f"flechasTotal: {flechasTotal}")
    print(f"manaTotal: {manaTotal}")
    print(f"manaAtual: {manaAtual}")
    print(f"mana: {mana}")
    print(f"nickFinal: {nickFinal}")

    if achar == 'nome':
        return nome
    elif achar == 'hp':
        return hp
    elif achar == 'hpAtual':
        return hpAtual
    elif achar == 'hpTotal':
        return hpTotal
    elif achar == 'mana':
        return mana
    elif achar == 'manaTotal':
        return manaTotal
    elif achar == 'manaAtual':
        return manaAtual
    elif achar == 'flechas':
        return flechas
    elif achar == 'flechasAtual':
        return flechasAtual
    elif achar == 'flechasTotal':
        return flechasTotal
    elif achar == 'nickFinal':
        return nickFinal
    else:
        return int('aaa')

    print('--FIM------------------------FIM--------------------FIM---------------FIM-----')


def rolagemAtributo(ctx, token, atributo, pericia, vantagemCod='', desvantagemCod=''):
    # tenta abrir a ficha, se não exiter o persongme, masnda a mesmagem de erro
    try:
        personagens_db()
    except mysql.connector.errors.OperationalError:
        return ctx.send('A conecção com o servidor PC batata de Maugrin foi perdida')
    if token not in personagens_db():
        return ctx.send('O personagem selecionado não existe')

    # trasforma o docs em lista e coloca o atributo no upper só pra confirmar
    atributo = atributo[:3].upper()

    # ve se é um teste de percia ou nn
    if pericia == 'p':
        vantagem = 6
        ctxDePericia = 'Perícia '
    else:
        vantagem = 0
        ctxDePericia = ''

    # acha a linha que esta o atributo e ve se é soma ou subtração pra depois fazer
    # e tamebm defini o modificador
    # define o atributo
    valorAtributo = atributo_db(atributo, token=token, get_atb=True)
    print('VALOR TRIBUTO AAAAA ' + str(valorAtributo))
    modificador = atributo_db(atributo, token=token, get_mod=True)
    print(modificador)
    sinal = qual_sinal_db(valorAtributo)
    print(f'sinal: {sinal}')
    print(atributo)
    # só pra enviar certinho na msg
    if atributo == 'STR':
        habilidade = 'força'
    elif atributo == 'DEX':
        habilidade = 'destreza'
    elif atributo == 'CON':
        habilidade = 'constituição'
    elif atributo == 'WIS':
        habilidade = 'sabedoria'
    elif atributo == 'CHA':
        habilidade = 'carisma'
    elif atributo == 'HAB' or atributo == 'POD':
        habilidade = 'poder'
    elif atributo == 'INT':
        habilidade = 'inteligencia'

    d100 = False

    # ve se é os neon
    validaçãoD100 = ['ptolomeu', 'maugrin']
    # validaçãoD60 = ['mario', 'alissa']
    validaçãoD60 = [' ']
    if token.lower() in validaçãoD100:
        dadoJogado = '1d100'
        d100 = True
        tabelaSistema = 'tabela sistema d100.txt'
        arq = open(tabelaSistema, 'r')
        tabela = arq.readlines()
        tabelaAtributo = tabela[int(valorAtributo) - 1].split('\t')
        if pericia == 'p':
            modificador = int(modificador) + 6
    elif token.lower() in validaçãoD60:
        dadoJogado = '1d60'
        tabelaSistema = 'tabela sistema d60.txt'
        arq = open(tabelaSistema, 'r')
        tabela = arq.readlines()
        tabelaAtributo = tabela[int(valorAtributo) - 1].split('\t')
        if pericia == 'p':
            modificador = int(modificador) + 4
    else:
        dadoJogado = '1d20'
        tabelaSistema = 'tabela sistema d20.txt'
        arq = open(tabelaSistema, 'r')
        tabela = arq.readlines()
        tabelaAtributo = tabela[int(valorAtributo) - 1].split('\t')
        if pericia == 'p':
            modificador = int(modificador) + 2

    # abre a tabela do sistema e ve a linha correspondente do seu atributo

    # rola o dado com o valor do modificador
    rolarDado = rolagem(ctx, f'{dadoJogado}{sinal}{modificador}')
    dado = rolarDado[1]
    dadoNatural = rolarDado[3]

    # define o normal bom e extremo baseado na linha
    normal = tabelaAtributo[0]
    bom = tabelaAtributo[1]
    extremo = tabelaAtributo[2]
    muitoBom = 1000000
    otimo = 100000000
    comVantagem = int(normal) - vantagem

    if d100 == True:
        print('entramos')
        muitoBom = tabelaAtributo[2]
        otimo = tabelaAtributo[3]
        extremo = tabelaAtributo[4]
        if dadoNatural == ['**1**'] or dadoNatural == ['**17**']:
            resultado = '**Desastre**'
            estagio = -1
        elif dado >= int(normal) and dado < int(bom):
            resultado = '`Sucesso Normal`'
            estagio = 1
        elif dado >= int(bom) and dado < int(muitoBom):
            resultado = '`**Sucesso Bom**`'
            estagio = 2
        elif dado >= int(muitoBom) and dado < int(otimo):
            resultado = '__Sucesso Muito Bom__'
            estagio = 3
        elif dado >= int(otimo) and dado < int(extremo):
            resultado = '**[Sucesso Ótimo]**'
            estagio = 4
        elif dado >= int(extremo):
            resultado = '--->>**EXTREMO**<<---'
            estagio = 5
        elif dado < int(normal):
            resultado = 'Fracasso'
            estagio = 0
        else:
            resultado = 'uékkkkkk analise'
    else:
        # ve o q tirou no dado
        if dadoNatural == ['**1**'] or dadoNatural == ['**17**']:
            resultado = '**Desastre**'
            estagio = -1
        elif dado >= int(normal) and dado < int(bom):
            resultado = '`Sucesso Normal`'
            estagio = 1
        elif dado >= int(bom) and dado < int(extremo):
            resultado = '`**Sucesso Bom**`'
            estagio = 2
        elif dado >= int(extremo):
            resultado = '**EXTREMO**'
            estagio = 3
        elif dado < int(normal):
            resultado = 'Fracasso'
            estagio = 0
        else:
            resultado = 'uékkkkkk analise'

    print(f'normal: {normal}\nbom: {bom}\nextremo: {extremo}\nmuito bom: {muitoBom}\notimo: {otimo}')

    final = ctx.reply(
        f'{token.title()}: {ctxDePericia}{habilidade.title()} = {valorAtributo}{sinal}{modificador} \n{resultado} | {rolarDado[2]} ',
        mention_author=False)

    # ve se o dado ta com vantagem e faz todo o processo de novo
    if 's' in vantagemCod:
        rolarDado1 = rolagem(ctx, f'{dadoJogado}{sinal}{modificador}')
        dado = rolarDado1[1]
        dadoNatural = rolarDado1[3]

        if d100 == True:
            if dadoNatural == ['**1**'] or dadoNatural == ['**17**']:
                resultado1 = '**Desastre**'
                estagio1 = -1
            elif dado > int(normal) and dado < int(bom):
                resultado1 = '`Sucesso Normal`'
                estagio1 = 1
            elif dado >= int(bom) and dado < int(extremo):
                resultado1 = '`**Sucesso Bom**`'
                estagio1 = 2
            elif dado >= int(muitoBom) and dado < int(otimo):
                resultado1 = '__Sucesso Muito Bom__'
                estagio1 = 3
            elif dado >= int(otimo) and dado < int(extremo):
                resultado1 = '**[Sucesso Ótimo]**'
                estagio1 = 4
            elif dado >= int(extremo):
                resultado1 = '-->>>>>**EXTREMO**<<<<<--'
                estagio1 = 5
            elif dado < int(normal):
                resultado1 = 'Fracasso'
                estagio1 = 0
            else:
                resultado = 'uékkkkkk analise'
        else:
            # ve o q tirou no dado
            if dadoNatural == ['**1**'] or dadoNatural == ['**17**']:
                resultado1 = '**Desastre**'
                estagio1 = -1
            elif dado >= int(normal) and dado < int(bom):
                resultado1 = '`Sucesso Normal`'
                estagio1 = 1
            elif dado >= int(bom) and dado < int(extremo):
                resultado1 = '`**Sucesso Bom**`'
                estagio1 = 2
            elif dado >= int(extremo):
                resultado1 = '**EXTREMO**'
                estagio1 = 3
            elif dado < int(normal):
                resultado1 = 'Fracasso'
                estagio1 = 0
            else:
                resultado1 = 'uékkkkkk analise'

        if estagio > estagio1:
            ultimaLinha1 = f'~~{resultado1} | {rolarDado1[2]}~~'
            ultimaLinha = f'{resultado} | {rolarDado[2]}'

        elif estagio < estagio1:
            ultimaLinha1 = f'{resultado1} | {rolarDado1[2]}'
            ultimaLinha = f'~~{resultado} | {rolarDado[2]}~~'

        elif estagio == estagio1:

            if rolarDado[1] > rolarDado1[1]:
                ultimaLinha1 = f'~~{resultado1} | {rolarDado1[2]}~~'
                ultimaLinha = f'{resultado} | {rolarDado[2]}'

            elif rolarDado[1] < rolarDado1[1]:
                ultimaLinha1 = f'{resultado1} | {rolarDado1[2]}'
                ultimaLinha = f'~~{resultado} | {rolarDado[2]}~~'

            elif rolarDado[1] == rolarDado1[1]:
                ultimaLinha1 = f'{resultado1} | {rolarDado1[2]}\n*Ai é foda bixokkkkkkkkk*'
                ultimaLinha = f'{resultado} | {rolarDado[2]}'
        ultimaLinha = ultimaLinha.replace("\n", "")
        final = ctx.reply(
            f'{token.title()}: {ctxDePericia}{habilidade.title()} = {valorAtributo}{sinal}{modificador} \n{ultimaLinha}\n{ultimaLinha1} ',
            mention_author=False)

    # ve se o dado ta com desvantagem e faz todo o processo de novo
    elif 's' in desvantagemCod:
        rolarDado1 = rolagem(ctx, f'{dadoJogado}{sinal}{modificador}')
        dado = rolarDado1[1]
        dadoNatural = rolarDado1[3]
        if dadoNatural == ['**1**'] or dadoNatural == ['**17**']:
            resultado1 = '**Desastre**'
            estagio1 = 0
        elif dado >= comVantagem and dado < int(bom):
            resultado1 = '`Sucesso Normal`'
            estagio1 = 1
        elif dado >= int(bom) and dado < int(extremo):
            resultado1 = '`**Sucesso Bom**`'
            estagio1 = 2
        elif dado >= int(extremo):
            resultado1 = '**EXTREMO**'
            estagio1 = 3
        elif dado < int(normal):
            resultado1 = 'Fracasso'
            estagio1 = -1
        else:
            resultado1 = 'uékkkkkk analise'

        if estagio < estagio1:
            ultimaLinha1 = f'~~{resultado1} | {rolarDado1[2]}~~'
            ultimaLinha = f'{resultado} | {rolarDado[2]}'

        elif estagio > estagio1:
            ultimaLinha1 = f'{resultado1} | {rolarDado1[2]}'
            ultimaLinha = f'~~{resultado} | {rolarDado[2]}~~'

        elif estagio == estagio1:

            if rolarDado[1] < rolarDado1[1]:
                ultimaLinha1 = f'~~{resultado1} | {rolarDado1[2]}~~'
                ultimaLinha = f'{resultado} | {rolarDado[2]}'

            elif rolarDado[1] > rolarDado1[1]:
                ultimaLinha1 = f'{resultado1} | {rolarDado1[2]}'
                ultimaLinha = f'~~{resultado} | {rolarDado[2]}~~'

            elif rolarDado[1] == rolarDado1[1]:
                ultimaLinha1 = f'{resultado1} | {rolarDado1[2]}\n*Putz, complexokkkkkkkkk*'
                ultimaLinha = f'{resultado} | {rolarDado[2]}'
        ultimaLinha = ultimaLinha.replace("\n", "")
        final = ctx.reply(
            f'{token.title()}: {ctxDePericia}{habilidade.title()} = {valorAtributo}{sinal}{modificador} \n{ultimaLinha}\n{ultimaLinha1} ',
            mention_author=False)

    return final


def idPersonagem(nick):
    arq = open('id e personagens.txt', 'r')
    docs = arq.readlines()
    print(nick)
    count = 0
    linhaNick = 0
    nickExiste = False
    while count < len(docs):
        if str(nick) in str(docs[count]):
            print(f'entramos {docs[count]}')
            linhaNick = count
            count = count + len(docs) + 8
            nickExiste = True
        else:
            print(docs[count])
            count = count + 1

    if nickExiste == True:
        docs = docs[linhaNick].split('=')[0]
        return (docs[:len(docs) - 1].title(), '0')
    if nickExiste == False:
        return (
        'Nenhum personagem selecionado para esse player. Selecione um personagem com o `.select <@player> <personagem>`',
        1)


def idPeloPersonagem(personagem):
    arq = open('id e personagens.txt', 'r')
    docs = arq.readlines()

    count = 0
    linhaNick = 0
    while count < len(docs):
        if str(personagem) in str(docs[count]):
            print(f'entramos {docs[count]}')
            linhaNick = count
            count = count + len(docs) + 8
        else:
            print(docs[count])
            count = count + 1

    return (docs[linhaNick].split('=')[1])


def acharItemNaLista(item, lista):
    for i in lista:
        if item in i:
            return i
            break


def val_a_in_b(a, b):
    if a in b:
        c = a
        return c


async def fichaCompletaCodigo(ctx, fichaInteira, nova=False, editar=False):
    ficha = fichaInteira.split('▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n')
    dadosPessoais = ficha[1].split('\n')
    atributos = ficha[2].split('\n')[1:]
    pericias = ficha[3].split('\n')[1:]

    bag = ficha[6].split('\n')[2:]
    bag2 = []
    for i in bag:
        i2 = i.split('►')
        bag2.append(''.join(i2))
    else:
        bag = bag2

    arma = ficha[7].split('\n')[2:]
    arma2 = []
    for i in arma:
        i2 = i.split('►')
        arma2.append(''.join(i2))
    else:
        arma = arma2

    nome = dadosPessoais[0].replace(" ", '').replace('NOME:', '')

    print('-------- DADOS PESSOAIS -----------')
    print(dadosPessoais)
    print('NOME: ' + nome)
    print('-------- ATRIBUTOS -----------')
    print(atributos)
    print('-------- PERICIAS -----------')
    print(pericias)
    print('-------- BAG -----------')
    print(bag)
    print('-------- ARMA -----------')
    print(arma)

    cAtributos = {'Força': 'str', 'Destreza': 'dex', 'Constituição':'con', 'Inteligência' : 'inte',
                  'Sabedoria' : 'wis', 'Carisma' : 'cha', 'Poder' : 'pod'}

    atbL = []
    valL = []
    modL = []

    for item in atributos:
        item = item.replace(' ', '').split(':')
        if item == ['']: pass
        else:
            atb = cAtributos[item[0]]
            val = item[1].split('(')[0]
            mod = item[1].split('(')[1].replace(")", '')

            atbL.append(atb)
            valL.append(val)
            modL.append(mod)

    character_exist = False

    db = data_base.cursor.execute("""select a.idatributos, a.personagematributos
                                from atributos as a""", True)
    print(f"db: {db}")

    for tpl in db:
        print(f"Tupla: {tpl}")
        print(f"Nome: {tpl[1].lower()}")
        print(f"Igual: {nome.lower()}")
        if nome.lower() == tpl[1].lower():
            print(f'Foi\nidtable: {tpl[0]}')
            character_exist = True
            idtable = tpl[0]

            break
    if character_exist == True:
        for i in range(0, 7):
            data_base.script_sql(f"""UPDATE atributos SET {atbL[i]} = '{valL[i]} WHERE idatributos = '{idtable}' """)
            data_base.script_sql(f"""UPDATE atributos SET mod{atbL[i]} = '{modL[i]} WHERE idatributos = '{idtable}' """)
    else:
        data_base.script_sql(f"""UPDATE atributos
                    SET (personagematributos, {atbL[0]}, {atbL[1]}, {atbL[2]}, {atbL[3]},
                    {atbL[4]}, {atbL[5]}, {atbL[6]}, mod{atbL[0]}, mod{atbL[1]}, mod{atbL[2]}, mod{atbL[3]},
                    mod{atbL[4]}, mod{atbL[5]}, mod{atbL[6]}) VALUES ('{nome}', '{valL[0]}', '{valL[1]}',
                    '{valL[2]}', '{valL[3]}', '{valL[4]}', '{valL[5]}', '{valL[6]}', '{modL[0]}', '{modL[1]}', '{modL[2]}',
                    '{modL[3]}', '{modL[4]}', '{modL[5]}', '{modL[6]}')""")

    count = 0
    print(ficha)
    posicaoNome = item_lista(ficha, 'NOME')

    posicaoForça = item_lista(ficha, 'Força')
    posicaoDestreza = item_lista(ficha, 'Destreza')
    posicaoConstituição = item_lista(ficha, 'Constituição')
    posicaoCarisma = item_lista(ficha, 'Carisma')
    posicaoSabedoria = item_lista(ficha, 'Sabedoria')
    posicaoInteligencia = item_lista(ficha, 'Inteligência')

    posicaoArroba = item_lista(ficha, 'JOGADOR')

    if posicaoNome == IndexError: await ctx.send('Não consegui reconhecer seu nome')
    if posicaoForça == IndexError: await ctx.send('Não consegui reconhecer sua força ')
    if posicaoDestreza == IndexError: await ctx.send('Não consegui reconhecer sua destreza ')
    if posicaoConstituição == IndexError: await ctx.send('Não consegui reconhecer sua constituição')
    if posicaoCarisma == IndexError: await ctx.send('Não consegui reconhecer seu carisma')
    if posicaoSabedoria == IndexError: await ctx.send('Não consegui reconhecer sua sabedoria')
    if posicaoInteligencia == IndexError: await ctx.send('Não consegui reconhecer sua inteligencia')
    if posicaoArroba == IndexError: await ctx.send('Não consegui reconhecer seu @')

    token = ficha[posicaoNome].split('NOME')[1]
    arroba = ficha[posicaoArroba].split('JOGADOR:')[1]
    print(f'token antes {token}')
    if token.startswith(':  '):
        token = token[3:]
        print(f'token com dois espços na frente, agora ta assim{token}')
    elif token.startswith(': '):
        token = token[2:]
        print(f'token tava com 1 espaço só, agora ta asism{token}')
    elif token.startswith(':'):
        token = token[1:]
        print(f'sem espaço nenhum, tava certo{token}')
    else:
        await ctx.send("Não consegui reconhecer seu nome")

    token = token.split(' ')[0]
    Força = ficha[posicaoForça]
    Destreza = ficha[posicaoDestreza]
    Constituição = ficha[posicaoConstituição]
    Carisma = ficha[posicaoCarisma]
    Sabedoria = ficha[posicaoSabedoria]
    Inteligencia = ficha[posicaoInteligencia]

    try:
        modificadorHabilidade = ficha[item_lista(ficha, 'uso magico:')].split(':')[1].replace(' ', '')
    except TypeError:
        try:
            modificadorHabilidade = ficha[item_lista(ficha, 'uso de armas:')].split(':')[1].replace(' ', '')
        except TypeError:
            try:
                modificadorHabilidade = ficha[item_lista(ficha, 'poder')].split(':')[1].replace(' ', '')
            except TypeError:
                await ctx.send('Não consegui reconhecer seu poder')

    try:
        modificadorForça = Força.split('(')[0].split(':')[1].replace(' ', '')
        períciasForça = Força.split('(')[1].replace(')', '')
    except IndexError:
        modificadorForça = Força.split(':')[1].replace(' ', '')
        períciasForça = ''

    try:
        modificadorDestreza = Destreza.split('(')[0].split(':')[1].replace(' ', '')
        períciasDestreza = Destreza.split('(')[1].replace(')', '')
    except IndexError:
        modificadorDestreza = Destreza.split(':')[1].replace(' ', '')
        períciasDestreza = ''

    try:
        modificadorConstituição = Constituição.split(':')[1].replace(' ', '')
        períciasConstituição = Constituição.split('(')[1].replace(')', '')
    except IndexError:
        modificadorConstituição = Constituição.split(':')[1].replace(' ', '')
        períciasConstituição = ''

    try:
        modificadorCarisma = Carisma.split('(')[0].split(':')[1].replace(' ', '')
        períciasCarisma = Carisma.split('(')[1].replace(')', '')
    except IndexError:
        modificadorCarisma = Carisma.split(':')[1].replace(' ', '')
        períciasCarisma = ''

    try:
        modificadorSabedoria = Sabedoria.split('(')[0].split(':')[1].replace(' ', '')
        períciasSabedoria = Sabedoria.split('(')[1].replace(')', '')
    except IndexError:
        modificadorSabedoria = Sabedoria.split(':')[1].replace(' ', '')
        períciasSabedoria = ''

    try:
        modificadorInteligencia = Inteligencia.split('(')[0].split(':')[1].replace(' ', '')
        períciasInteligencia = Inteligencia.split('(')[1].replace(')', '')
    except IndexError:
        modificadorInteligencia = Inteligencia.split(':')[1].replace(' ', '')
        períciasInteligencia = ''

    força = f'STR={modificadorForça}'
    destreza = f'DEX={modificadorDestreza}'
    inteligencia = f'INT={modificadorInteligencia}'
    sabedoria = f'WIS={modificadorSabedoria}'
    carisma = f'CHA={modificadorCarisma}'
    constituicao = f'CON={modificadorConstituição}'
    habilidade = f'HAB={modificadorHabilidade}'

    print(modificadorDestreza)
    print(modificadorInteligencia)
    print(modificadorSabedoria)
    print(modificadorCarisma)
    print(modificadorConstituição)

    atributos = [força, destreza, inteligencia, sabedoria, carisma, constituicao, habilidade]

    print(token)
    print(type(token))
    open(f'ficha {token}.txt', 'a')
    if nova == True and editar == False:
        count = 0
        while count < 7:
            await novo_atributo(ctx, token, atributos[count])
            count = count + 1
        await xp(ctx, token, modificadorXp, '!')
        await select(ctx, arroba, token)
        await ctx.send('Nova ficha adicionada com sucesso\nUse o `.verF <personagem>` para ver sua ficha')
    elif nova == False and editar == True:
        count = 0
        while count < 7:
            await editar_atributo(ctx, token, atributos[count])
            count = count + 1
        await xp(ctx, token, modificadorXp)
        await ctx.send('Ficha editada com sucesso\nUse o `.verF <personagem>` para ver sua ficha')


def atributosModi(atb, token):
    cAtributos = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA', 'HAB', 'POD']
    nomeAtributo = atb
    valorAtributo = atributo_db(atb, token=token, get_atb=True)
    modificadorAtributo = atributo_db(atb, token=token, get_mod=True)
    validaçãoD100 = ['ptolomeu', 'maugrin']
    # validaçãoD60 = ['alissa', 'mario']
    validaçãoD60 = [' ']
    d100 = False

    if token.lower() in validaçãoD100:
        arq = open('tabela sistema d100.txt', 'r')
        tabela = arq.readlines()
        tabelaAtributo = tabela[int(valorAtributo) - 1].split('\t')
        d100 = True
    elif token.lower() in validaçãoD60:
        arq = open('tabela sistema d60.txt', 'r')
        tabela = arq.readlines()
        tabelaAtributo = tabela[int(valorAtributo) - 1].split('\t')
    else:
        arq = open('tabela sistema d20.txt', 'r')
        tabela = arq.readlines()
        tabelaAtributo = tabela[int(valorAtributo) - 1].split('\t')

    normal = str(tabelaAtributo[0])
    bom = tabelaAtributo[1]
    extremo = tabelaAtributo[2]
    muitoBom = ''
    otimo = ''
    if d100 == True:
        muitoBom = tabelaAtributo[2]
        otimo = tabelaAtributo[3]
        extremo = tabelaAtributo[4]

    cEmoji = [':punch:', ':scales:', ':shield:', ':brain:', ':zany_face:', ':bow_and_arrow:', ':medal:']
    emoji = ''
    nomeAtributo = atb
    if 'STR' in nomeAtributo:
        emoji = cEmoji[0]
    elif 'DEX' in nomeAtributo:
        emoji = cEmoji[5]
    elif 'CON' in nomeAtributo:
        emoji = cEmoji[2]
    elif 'WIS' in nomeAtributo:
        emoji = cEmoji[1]
    elif 'CHA' in nomeAtributo:
        emoji = cEmoji[4]
    elif 'HAB' in nomeAtributo or 'POD' in nomeAtributo:
        nomeAtributo = 'PODER'
        emoji = cEmoji[6]
    elif 'INT' in nomeAtributo:
        emoji = cEmoji[3]

    sinal = qual_sinal_db(valorAtributo)

    return (nomeAtributo, valorAtributo, modificadorAtributo, sinal, normal, bom, extremo, emoji, muitoBom, otimo)
