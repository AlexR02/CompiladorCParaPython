import re
import os

class Variavel:
    def __init__(self, identificador, tipo, valor, escopo):
        self.identificador = identificador
        self.valor = valor
        self.escopo = escopo
        self.tipo = tipo
    
    def __str__(self):
        return "Nome de variável{Tipo: " + self.tipo + ", Valor: " + self.valor + "}"

class Funcao:
    def __init__(self, identificador, tipoRetorno, parametros):
        self.identificador = identificador
        self.tipoRetorno = tipoRetorno
        self.parametros = parametros

    def __str__(self):
        return "Função{Tipo: " + self.tipoRetorno + "}"

def analiseSintatica():
    fName = "CodigosTesteC/1.c"#Abre o arquivo para leitura
    output = "1.py"

    #fName = "CodigosTesteC/2.c"
    #output = "2.py"

    #fName = "CodigosTesteC/3.c"
    #output = "3.py"

    #fName = "CodigosTesteC/4.c"
    #output = "4.py"

    #fName = "CodigosTesteC/5.c"
    #output = "5.py"

    #fName = "CodigosTesteC/6.c"
    #output = "6.py"

    #fName = "CodigosTesteC/7.c"
    #output = "7.py"

    #fName = "CodigosTesteC/8.c"
    #output = "8.py"

    #fName = "CodigosTesteC/9.c"
    #output = "9.py"

    #fName = "CodigosTesteC/10.c"
    #output = "10.py"

    f = open(fName, "r")
    outputFile = open(output, "w")
    lines = f.readlines()

    tokens = {}
    qtdLines = 1
    pilhaDelimitadoresC = [] #pilha delimitadores chaves
    pilhaDelimitadoresP = [] #pilha delimitadores parenteses
    tipos = ["int", "float", "void"]


    for line in lines:
        line = re.sub(r"{", " { ", line)
        line = re.sub(r";", " ;", line)
        line = re.sub(r"\((float|int)\)", "", line)
        
        if(re.search(r"[0-9]{1,},[0-9]{1,}", line)):
            print("O valor " + re.search(r"[0-9]{1,},[0-9]{1,}", line).group(0) + " na linha " + str(qtdLines) + " é inválido")
            os.remove(output)
            return

        line = re.sub(r",", " , ", line)
        line = re.sub(r"[ ]{0,}\(", " ( ", line)
        line = re.sub(r"[ ]{0,}\)", " ) ", line)
        line = re.sub(r"\|\|", " || ", line)
        line = re.sub(r"&&", " && ", line)
        line = re.sub(r"=", " = ", line)
        line = re.sub(r"\+", " + ", line)
        line = re.sub(r"-", " - ", line)
        line = re.sub(r"/", " / ", line)
        line = re.sub(r"\*", " * ", line)
        line = re.sub(r"%", " % ", line)
        line = re.sub(r"[^.h]>", " > ", line)
        line = re.sub(r"<[^A-Za-z]", " < ", line)
        line = re.sub(r"!", " ! ", line)
        line = re.sub(r"=[ ]{0,}=", " == ", line)
        line = re.sub(r">[ ]{0,}=", " >= ", line)
        line = re.sub(r"<[ ]{0,}=", " <= ", line)
        line = re.sub(r"![ ]{0,}=", " != ", line)
        line = re.sub(r"[ ]{2,}", " ", line)

        line = re.sub(r" / / .*", "", line)
        #print(line)
        if line.strip() != '':
            line = line.strip()
            tab = len(pilhaDelimitadoresC) * "\t"
            if re.search(r"^#include <.*[.]h>$", line):
                line = line.split()
                tokens[line[0]] = "Palavra reservada"
                biblioteca = re.sub(r"(<|>)","", line[1])
                tokens[biblioteca] = "Biblioteca"
            elif re.search(r"^int main \( .*( |)\)( {|)$", line):
                line = line.split()
                tokens[line[0]] = "Palavra reservada"
                tokens[line[1]] = "Palavra reservada"
                outputFile.write("def main(): \n")
                if len(line) == 3:
                    tokens[line[2]] = "Delimitador de início"
                    pilhaDelimitadoresC.append(qtdLines)
            elif re.search(r"^scanf \( .* \)", line):
                scanAux = (re.sub(r"(scanf \(|\)| |;)", "", line)).split(",")
                if scanAux[0] != '"%i"' and scanAux[0] != '"%f"':
                    print("Erro na linha " + str(qtdLines) + " o caractere " + scanAux[0] + " é inválido")
                    os.remove(output)
                    return
                tipo = "int" if scanAux[0] == '"%i"' else "float"
                var = re.sub(r"^&", "", scanAux[1])
                if re.search(r"^&", scanAux[1]):
                    scanAux[1] = re.sub(r"^&", "", scanAux[1]) + ": Escopo-" + str(pilhaDelimitadoresC[len(pilhaDelimitadoresC)-1])
                    if scanAux[1]  not in tokens:
                        print("Erro na linha " + str(qtdLines) + ", a variável '" + scanAux[1] + "' não foi declarada")
                        os.remove(output)
                        return
                    elif not (((tokens[scanAux[1]]).tipo == "int" and scanAux[0] == '"%i"') or ((tokens[scanAux[1]]).tipo == "float" and scanAux[0] == '"%f"')):
                        print("Erro na linha " + str(qtdLines) + " os tipos do input não são iguais")
                        os.remove(output)
                        return
                
                outputFile.write(tab + var + " = " + tipo + "(input())\n")
                tokens[line] = "Função de input"
            elif re.search(r"^printf \( .* \)", line):
                tokens[(re.sub(r";", "", line))] = "Função para imprimir na tela"
                printAux = (re.sub(r"(scanf \(|\)| |;)", "", line)).split(",")
                outputFile.write(tab + "print(" + printAux[1] + ")\n")
            elif line == "{":
                tokens[line] = "Delimitador de início"
                pilhaDelimitadoresC.append(qtdLines)
            elif line == "}":
                tokens[line] = "Delimitador de fim"
                if len(pilhaDelimitadoresC) > 0:
                    pilhaDelimitadoresC.pop()
                else:
                    print("Delimitador de fim '}' a mais na linha " + str(qtdLines))
                    os.remove(output)
                    return
            elif re.search(r"^(else |)if \( .* \)", line):
                #if re.search(r"{", line):
                tokens[re.search(r"^(else |)if \( .* \)", line).group(0)] = "if condicional"
            elif re.search(r"^else", line):
                tokens[re.search(r"^else", line).group(0)] = "if condicional"
            else:
                aux = line
                tipoAtribuicaoCorrente = ""
                
                line = line.split()
                for j in range(len(line)):
                    i = line[j]
                    #print(i)
                    if i == "return":
                        tokens[i] = "Palavra reservada"
                        retorno = ""
                        for k in range(j + 1, len(line) - 1):
                            retorno = retorno + " " + line[k]
                        outputFile.write(tab + "return " + retorno + "\n")
                    elif i in tipos:
                        tipoAtribuicaoCorrente = i
                        tokens[i] = "Palavra reservada tipo"
                    elif i == "{" or i == "(":
                        tokens[i] = "Delimitador de início"
                        if i == "{":
                            pilhaDelimitadoresC.append(qtdLines)
                        elif i == "(":
                            pilhaDelimitadoresP.append(qtdLines)
                        tipoAtribuicaoCorrente = ""
                    elif i == "}" or i == ")":
                        tipoAtribuicaoCorrente = ""
                        tokens[i] = "Delimitador de fim"
                        if i == '}' and len(pilhaDelimitadoresC) > 0:
                            pilhaDelimitadoresC.pop()
                        elif i == ")" and len(pilhaDelimitadoresP) > 0:
                            tipoAtribuicaoCorrente = ""
                            pilhaDelimitadoresP.pop()
                        else:
                            print("Delimitador de fim " + i + " a mais na linha " + str(qtdLines))
                            os.remove(output)
                            return
                    elif i == "=":
                        tipoAtribuicaoCorrente = ""
                        tokens[i] = "Comando de atribuição"
                    elif i == "+":
                        tokens[i] = "Operador de adição"
                    elif i == "*":
                        tokens[i] = "Operador de multiplicação"
                    elif i == "-":
                        tokens[i] = "Operador de subtração"
                    elif i == "/":
                        tokens[i] = "Operador de divisão"
                    elif i == "%":
                        tokens[i] = "Operador resto da divisão"
                    elif i == ";":
                        tipoAtribuicaoCorrente = ""
                        tokens[i] = "Finalizador de linha"
                        outputFile.write("\n")
                    elif re.search(r"^[a-zA-Z]{1,}[0-9]*$", i):
                        if line[j + 1] == "(":
                            if tipoAtribuicaoCorrente == "" and i not in tokens:
                                print("Erro na linha " + str(qtdLines) + ", a função '" + i + "' não foi declarada corretamente")
                                os.remove(output)
                                return
                            elif tipoAtribuicaoCorrente != "" and i in tokens:
                                print("Erro na linha " + str(qtdLines) + ", a variável '" + i + "' já foi declarada")
                                os.remove(output)
                                return
                            elif i not in tokens:
                                escopo = pilhaDelimitadoresC[len(pilhaDelimitadoresC) - 1] if len(pilhaDelimitadoresC) > 0 else qtdLines
                                identificador = i
                                tipoRetorno = tipoAtribuicaoCorrente
                                parametros = []
                                param = ""
                                for k in range(j+2,len(line)-2):
                                    parametro = line[k]
                                    if parametro not in tipos and parametro != ",":
                                        parametros.append(parametro + ": Escopo-" + str(escopo))
                                        param = param + parametro + ","
                                fun = Funcao(identificador, tipoRetorno, parametros)

                                outputFile.write("def " + fun.identificador + "(" + param[0:len(param)-1] + "): \n")
                                tokens[i] = fun
                        else:
                            escopo = pilhaDelimitadoresC[len(pilhaDelimitadoresC) - 1] if len(pilhaDelimitadoresC) > 0 else 0
                            var = i
                            i = i + ": Escopo-" + str(qtdLines if escopo == 0 else escopo)
                            if tipoAtribuicaoCorrente == "" and i not in tokens:
                                print("Erro na linha " + str(qtdLines) + ", a variável '" + i + "' não foi declarada corretamente")
                                os.remove(output)
                                return
                            elif tipoAtribuicaoCorrente != "" and i in tokens:
                                if escopo >= tokens[i].escopo:
                                    print("Erro na linha " + str(qtdLines) + ", a variável '" + i + "' já foi declarada")
                                    os.remove(output)
                                    return
                            elif i not in tokens:
                                identificador = i
                                tipo = tipoAtribuicaoCorrente
                                valor = ""
                                if line[j + 1] == "=":
                                    if tipo in tipos:
                                        if re.search(r"^[0-9]{1,}([.][0-9]{1,}|)$", line[j + 2]):
                                            valor = line[j + 2]
                                        else:
                                            auxFunc = ""
                                            func = ""
                                            auxList = line.copy()
                                            for l in range(len(line)):
                                                if(line[l] in tokens and type(tokens[line[l]]) == Funcao):
                                                    auxFunc = line[l]
                                                    func = auxFunc
                                                if (line[l] in tokens and type(tokens[line[l]]) == Funcao) == False and auxFunc != "":
                                                    auxFunc = auxFunc + line[l]
                                                    auxList.remove(line[l])
                                                    if line[l] == ")":
                                                        auxList[auxList.index(func)] = auxFunc
                                                        auxFunc = ""
                                            for k in range(j+2, len(auxList)-1):
                                                if ((auxList[k] + ": Escopo-" + str(escopo)) not in tokens) and (auxList[k] not in ["+", "-", "*", "/"]) and (type(auxList[k]) == Funcao and auxList[k] not in tokens):
                                                    print("Erro na linha " + str(qtdLines) + ", sequência de caracteres " + auxList[k] + " na operação não é válida")
                                                    os.remove(output)
                                                    return
                                                elif ((auxList[k] + ": Escopo-" + str(escopo)) in tokens) :
                                                    if (auxList[k-1] != "=" and auxList[k-1] != "(" and (auxList[k-1] not in ["+", "-", "*", "/"])) or ((auxList[k+1] not in ["+", "-", "*", "/"]) and auxList[k+1] != ";" and auxList[k+1] != ")"):
                                                        print("Operação mal formada na linha " + str(qtdLines))
                                                        os.remove(output)
                                                        return
                                                valor = valor + auxList[k] + " "
                                        outputFile.write(tab + var + " = " + valor)
                                var = Variavel(identificador, tipo, valor, escopo)
                                tokens[i] = var
                            elif i in tokens:
                                valor = ""
                                if line[j + 1] == "=":
                                    if re.search(r"^[0-9]{1,}([.][0-9]{1,}|)$", line[j + 2]):
                                        valor = line[j + 2]
                                    else:
                                        auxFunc = ""
                                        func = ""
                                        auxList = line.copy()
                                        for l in range(len(line)):
                                            if(line[l] in tokens and type(tokens[line[l]]) == Funcao):
                                                auxFunc = line[l]
                                                func = auxFunc
                                            if (line[l] in tokens and type(tokens[line[l]]) == Funcao) == False and auxFunc != "":
                                                auxFunc = auxFunc + line[l]
                                                auxList.remove(line[l])
                                                if line[l] == ")":
                                                    auxList[auxList.index(func)] = auxFunc
                                                    auxFunc = ""
                                        for k in range(j+2, len(auxList)-1):
                                            if ((auxList[k] + ": Escopo-" + str(escopo)) not in tokens) and (auxList[k] not in ["+", "-", "*", "/"]) and (type(auxList[k]) == Funcao and auxList[k] not in tokens):
                                                print("Erro na linha " + str(qtdLines) + ", sequência de caracteres " + auxList[k] + " na operação não é válida")
                                                os.remove(output)
                                                return
                                            elif ((auxList[k] + ": Escopo-" + str(escopo)) in tokens) :
                                                if (auxList[k-1] != "=" and auxList[k-1] != ")" and (auxList[k-1] not in ["+", "-", "*", "/"])) or ((auxList[k+1] not in ["+", "-", "*", "/"]) and auxList[k+1] != ";" and auxList[k+1] != "("):
                                                    print("Operação mal formada na linha " + str(qtdLines))
                                                    os.remove(output)
                                                    return
                                            valor = valor + auxList[k] + " "
                                    tokens[i].valor = valor
                                    outputFile.write(tab + var + " = " + valor)
                    elif re.search(r"^[0-9]{1,}([.][0-9]{1,}|)$", i):
                        tokens[i] = "Constante numérica"
                    elif re.search(r"^\".+\"$", i):
                        tokens[i] = "String constante"
                    elif i == ",":
                        tokens[i] = "Separador"
                    elif i in ["==", "!="]:
                        tokens[i] = "Operador de igualdade"
                    elif i in [">", "<",">=", "<="]:
                        tokens[i] = "Operador relacional"
                    elif i in ["!", "&&", "||"]:
                        tokens[i] = "Operador lógico"
                    else:
                        if i == "#include":
                            i = aux
                        print("O token '" + i + "' na linha " + str(qtdLines) + " é inválido")
                        os.remove(output)
                        return
        qtdLines += 1
    if(len(pilhaDelimitadoresC) > 0):
        print("Delimitador de início '{' a mais na linha " + str(pilhaDelimitadoresC[len(pilhaDelimitadoresC)-1]))
        os.remove(output)
        return
    if(len(pilhaDelimitadoresP) > 0):
        print("Delimitador de início '(' a mais na linha " + str(pilhaDelimitadoresP[len(pilhaDelimitadoresP)-1]))
        os.remove(output)
        return
    outputFile.write("main()")
    for key in tokens:
        print(key + " - " + str(tokens[key]))
        if(type(tokens[key]) == Funcao):
            print(tokens[key].parametros)
    print("\n\nSeu código C foi convertido para python com sucesso!!")
    outputFile.close()
    f.close()
    
def main():
    analiseSintatica()

main()