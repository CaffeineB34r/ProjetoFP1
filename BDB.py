def corrigir_palavra(palavra):
    """Retira todas as instancias de maiusculas e minusculas da mesma letra adjacentes e devolve a string corrigida"""
    def diferentes(letra1, letra2):
        return letra1 + letra2 if not (letra1.upper() == letra2.upper() and letra1 != letra2) else ''

    def depurar(start):
        # Utiliza o slice a partir de start comparar adjacentes a cada 2 casas,devolve a string corrigida
        return ''.join((map(diferentes, list(palavra[start::2]), list(palavra[start + 1::2]))))

    if len(palavra) >= 2:
        par, imp = depurar(0), palavra[0] + depurar(1)
        par = par if len(palavra) % 2 == 0 else par + palavra[-1]
        imp = imp if len(palavra) % 2 != 0 else imp + palavra[-1]
        # Tenta corrigir a palavra até que não haja nenhuma alteração feita
        return par if par == imp == palavra else corrigir_palavra(imp) if par == palavra else corrigir_palavra(par)
    return palavra


def eh_anagrama(palavra1, palavra2):
    """Recebe 2 strings, devolve um valor lógico do teste se são anagramas entre si"""
    def sortlist(s): return sorted(list(s.lower()))

    return sortlist(palavra1) == sortlist(palavra2)


def corrigir_doc(frase):
    """Recebe uma string de palavras corruptas, corrige cada uma e retira anagramas,devolve uma string"""

    if not frase or not (isinstance(frase, str) and all(x.isalpha() for x in frase.split())) or '  ' in frase:
        raise ValueError('corrigir_doc: argumento invalido')

    palavras, doc_corrigido = frase.split(' '), ''
    palavras = list(map(corrigir_palavra, palavras))

    while palavras:
        anagrama_teste = palavras.pop(0)
        if palavras:
            for word in palavras:
                if eh_anagrama(anagrama_teste, word) and anagrama_teste.lower() != word.lower():
                    del palavras[palavras.index(word)]
        doc_corrigido += ' ' + anagrama_teste

    return doc_corrigido[1:]


def obter_posicao(movimento, num_atual):
    """Tenta aplicar um movimento ao numero atual, devolve o inteiro correspondente à posiçao resultante"""
    def div_3(num): return num % 3

    cbde = {'C': -3, 'B': 3, 'D': 1 if div_3(num_atual) else 0, 'E': -1 if div_3(num_atual - 1) else 0}
    move_valido = (num_atual + cbde[movimento] in range(1, 10))

    return num_atual + cbde[movimento] if move_valido else num_atual


def obter_digito(movimento, num_atual):
    """Aplica uma sequencia de movimentos num inteiro, devolve o inteiro correspondente à posiçao resultante"""
    for letra in movimento:
        if letra not in 'CBED' or letra == '':
            raise ValueError('obter_pin: argumento invalido')
        num_atual = obter_posicao(letra, num_atual)
    return num_atual


def obter_pin(codigo):
    """Recebe um conjunto de sequencias de movimentos e constroi um tuplo dos resultados destes começando cada em 5"""
    if isinstance(codigo, tuple) and len(codigo) in range(4, 11) and all(codigo):
        num, pin = 5, ()
        for elemento in codigo:
            num = obter_digito(elemento, num)
            pin += (num,)
        if pin:
            return pin
    raise ValueError('obter_pin: argumento invalido')


def eh_entrada(entrada):
    """Testa se o argumento dado cumpre as caracteristicas de uma entrada da bdb
    e devolve o valor logico correspondente"""
    return isinstance(entrada, tuple) and len(entrada) == 3 \
        and (str, str, tuple) == tuple(map(type, entrada)) and len(entrada[1]) == 7 \
        and ' ' not in entrada[0] and '' not in entrada[0].split('-') \
        and entrada[0].islower() and ''.join(entrada[0].split('-')).isalpha() \
        and entrada[1][0] == '[' and entrada[1][-1] == ']' \
        and entrada[1][1:-1].isalpha() and entrada[1][1:-1].islower() \
        and isinstance(entrada[2], tuple) and len(entrada[2]) >= 2 \
        and all(isinstance(n, int) for n in entrada[2]) and sorted(entrada[2])[0] > 0


def validar_cifra(cifra, checksum):
    """Testa se a cifra do argumento é coerente com o checksum e devolve o valor logico correspondente"""
    cifra = sorted(filter(lambda a: a != '-', sorted(list(cifra))), key=lambda a: cifra.count(a), reverse=True)
    cifra = list(dict.fromkeys(cifra))
    return cifra[:5] == list(checksum)[1:-1]


def filtrar_bdb(lista):
    """Recebe uma lista de entradas e devolve uma lista daquelas que não têm cifra valida"""
    if isinstance(lista, list) and lista and all(map(eh_entrada, lista)):
        invalidos = [x for x in lista if not (validar_cifra(x[0], x[1]))]
        return invalidos
    raise ValueError('filtrar_bdb: argumento invalido')


def obter_num_seguranca(chave):
    """Recebe um tuplo de inteiros e devolve a menor diferença entre eles"""
    lista1, lista2 = list(sorted(chave)), [0] + list(sorted(chave))
    subtracao = sorted(list(map(lambda x, y: x - y, lista1, lista2))[1:])
    return subtracao[0]


def decifrar_texto(cifra, seguranca):
    """Recebe uma string e um inteiro e
    devolve uma string com a rotaçao de cada caracter com base no numero de segurança"""
    def corta(lista, start):
        lista[start::2] = [' ' if e == '-' else ord(e) + (-1) ** start + seguranca for e in lista[start::2]]

    cifra, seguranca = list(cifra), seguranca % 26
    corta(cifra, 0), corta(cifra, 1)
    cifra = [' ' if e == ' ' else e - 26 if e > 122 else e + 26 if e < 97 else e for e in cifra]
    cifra = [' ' if e == ' ' else chr(e) for e in cifra]
    return ''.join(cifra)


def decifrar_bdb(entradas):
    """Recebe uma lista de entradas e devolve uma lista com cada uma dessas decifradas"""
    if isinstance(entradas, list) and entradas and all(map(eh_entrada, entradas)):
        decifrados = list(map(lambda entrada: decifrar_texto(entrada[0], obter_num_seguranca(entrada[2])), entradas))
        return decifrados
    raise ValueError('decifrar_bdb: argumento invalido')


def eh_utilizador(utilizador):
    """Testa se é um utilizador valido e devolve o valor lógico correspondente"""
    def teste_dicionarios(dicionario, chaves, tipos):
        return sorted(dicionario.keys()) == sorted(chaves) and all(dicionario.values()) \
            and tuple(map(type, [dicionario.get(x) for x in sorted(dicionario.keys())])) == tipos

    return isinstance(utilizador, dict) \
        and teste_dicionarios(utilizador, ['name', 'pass', 'rule'], (str, str, dict)) \
        and teste_dicionarios(utilizador['rule'], ['vals', 'char'], (str, tuple)) \
        and len(utilizador['rule']['vals']) == 2 and len(utilizador['rule']['char']) == 1 \
        and tuple(map(type, utilizador['rule']['vals'])) == (int, int) \
        and 0 < utilizador['rule']['vals'][0] <= utilizador['rule']['vals'][1]


def eh_senha_valida(password, rule):
    """Recebe uma password e uma regra e testa se a password cumpre a regra e devolve o valor  lógico correspondente"""
    regra_indiv = len([x for x in password if x == rule['char']]) in range(rule['vals'][0], rule['vals'][1] + 1)
    regra_vogal = len([x for x in password if x in 'aeiou']) >= 3
    regra_geral = any([password[x] == password[x - 1] for x in range(1, len(password))])
    return regra_indiv and regra_vogal and regra_geral


def filtrar_senhas(entradas):
    """Recebe uma lista de entradas e devolve aquelas em que a pass não cumpre as regras"""
    if isinstance(entradas, list) and all((lambda x: isinstance(x, dict), entradas)):
        nomes = sorted([x['name'] for x in entradas if eh_utilizador(x) and not eh_senha_valida(x['pass'], x['rule'])])
        if nomes:
            return nomes
    raise ValueError('filtrar_senhas: argumento invalido')
