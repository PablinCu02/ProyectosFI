import re
import time


#Función para crear un patrón de expresión regular a partir
#de un diccionario y una nueva entrada
def DIREC(dic, nuevo, exp):
    exp = nuevo
    for valor in dic:
        exp = exp + '|' + valor
    exp = r'\b' + '(' + exp + ')' + r'\b'
    return (re.compile(exp), exp)

#Función principal que procesa las líneas de código de ensamblador
def Pasadas(lectura):
    errores = []
    patron_num = re.compile(r'\d+')
    patron_org = re.compile(r'\s*(ORG)\s+(\d+)\n') 
    patron_directivas = re.compile(r'^(\s*([a-z]+):)')
    ORG = int(patron_num.search(lectura[0]).group()) if patron_org.match(lectura[0]) else 0
    contador_lineas = ORG
    CONTADOR = []
    BufEs = []
    diccionario = {}
    COBJETO = []
    patron_directiva = re.compile(r'([a-z]+)') 
    EXP = '(DADO)$'
    patron_dic = re.compile(EXP)
    patron_separadores = re.compile(r'[ ,]')
    patron_comentarios = re.compile(r';.*')        
    patron_espacios = re.compile(r'[\t\n]')
    
    for linea in lectura:
        linea = linea.replace("\n", "")
        linea = patron_espacios.sub("", linea)
        linea = patron_comentarios.sub("", linea)
        if patron_separadores.sub("", linea) == "":
            continue
        if patron_directivas.match(linea):
            if patron_directiva.search(linea).group() not in diccionario:
                IO = DIREC(diccionario, patron_directiva.search(linea).group(), EXP)
                EXP = IO[1]
                patron_dic = IO[0]
                diccionario.update({patron_directiva.search(linea).group(): (True, str(contador_lineas))})
            else:
                if diccionario[patron_directiva.search(linea).group()][0] is False:
                    diccionario[patron_directiva.search(linea).group()] = (True, str(contador_lineas))
            linea = patron_directivas.sub("", linea, 1)
        if patron_directiva.search(linea) and patron_directiva.search(linea).group() not in diccionario:
            IO = DIREC(diccionario, patron_directiva.search(linea).group(), EXP)
            EXP = IO[1]
            patron_dic = IO[0]
            diccionario.update({patron_directiva.search(linea).group(): (False, str(contador_lineas))})
        linea = patron_directiva.sub(str(contador_lineas) + " ", linea)        
        YU = SRCH(MiTabla, patron_separadores.sub("", linea))
        if YU:
            contador_lineas += int(YU[2])
            continue
        T = TRAD(linea, vector(), contador_lineas)
        if T:
            K = SRCH(MiTabla, patron_separadores.sub("", T[0]))
            contador_lineas = contador_lineas + int(K[2]) if K else contador_lineas + 1
        else:
            contador_lineas += 1  
    
    contador_lineas = ORG
    i = 0
    etiquetas_definidas = []
    for linea in lectura:
        linea = linea.replace("\n", "")
        linea = patron_espacios.sub("", linea)
        linea = patron_comentarios.sub("", linea)
        if patron_separadores.sub("", linea) == "":
            COBJETO.append("\t")
            CONTADOR.append("\t")
            continue
        if patron_directivas.match(linea):
            if patron_directiva.search(linea).group() in etiquetas_definidas:
                COBJETO.append("ETIQUETA PREVIAMENTE DEFINIDA")
                errores.append("ETIQUETA PREVIAMENTE DEFINIDA: " + linea)
                CONTADOR.append(format(contador_lineas, '04X'))
                contador_lineas += 1
                continue
            else:
                etiquetas_definidas.append(patron_directiva.search(linea).group())
            linea = patron_directivas.sub("", linea)
        if patron_directiva.search(linea):
            if not diccionario[patron_directiva.search(linea).group()][0]:
                errores.append("ETIQUETA INDEFINIDA: " + linea)
                COBJETO.append("ETIQUETA INDEFINIDA")
                CONTADOR.append(format(contador_lineas, '04X'))
                contador_lineas += 1
                continue
            else:
                linea = patron_dic.sub(diccionario.get(patron_dic.search(linea).group())[1] + " ", linea)
        KU = SRCH(MiTabla, patron_separadores.sub("", linea))
        if KU:
            COBJETO.append(KU[1])
            CONTADOR.append(format(contador_lineas, '04X'))
            contador_lineas += int(KU[2])
            i += 1
            continue
        BufEs = TRAD(linea, vector(), contador_lineas)
        TR = SRCH(MiTabla, patron_separadores.sub("", BufEs[0])) if BufEs else None
        if TR:
            num_bytes = int(TR[2]) * 2
            HEXA = TR[1].replace("r", BufEs[1][0])
            HEXA = HEXA.replace("t", BufEs[1][1])
            if len(BufEs[1][2]) == 16:
                num_bytes -= 4
                HEXA = format(int(HEXA.replace("n", ""), 2), '0' + str(num_bytes) + 'X')
                EnHexa = format(int(BufEs[1][2], 2), '04X')
                HEXA = HEXA + EnHexa[2:] + EnHexa[:2]
                COBJETO.append(str(HEXA))
                CONTADOR.append(format(contador_lineas, '04X'))
                contador_lineas += int(TR[2])
                i += 1
                continue
            HEXA = HEXA.replace("n", BufEs[1][2])
            HEXA = HEXA.replace("d", BufEs[1][3])
            COBJETO.append(format(int(HEXA, 2), '0' + str(num_bytes) + 'X'))
            CONTADOR.append(format(contador_lineas, '04X'))
            contador_lineas += int(TR[2])
            i += 1
        else:
            errores.append("ERROR DE SINTAXIS " + linea)
            COBJETO.append("ERROR DE SINTAXIS")
            CONTADOR.append(format(contador_lineas, '04X'))
            contador_lineas += 1
            i += 1    
    return (CONTADOR, COBJETO, errores, ORG, diccionario)

#Funcion para retornar un vector inicializado
def vector():
    return ["1", "1", "1", "1"]

#Funcion para buscar una clave en una tabla hash
def SRCH(tabla, clave):
    indice = HASH(clave, len(tabla))      
    if tabla[indice]:                  
        for elemento in tabla[indice]:     
            if elemento[0] == clave:     
                return elemento       
    return None                

# Función para obtener el complemento A2 
def compA2(binario, t):
    for i in range(t, -1, -1):
        if binario[i] == "1":
            for k in range(i):
                binario[k] = "1" if binario[k] == "0" else "0" 
            break
    return ''.join(binario)

# Función para crear la tabla hash
def tabla(tam):                 
    return [list() for _ in range(tam)]

# Función para generar el archivo LST con el resultado del ensamblado
def ARLST(CONTADOR, COBJETO, LEER, dic, NOMBRE, ORG):
    try:
        with open(NOMBRE + ".LST", 'w') as archivo:
            print("ORG 0000 " + str(ORG), file=archivo)
            for i in range(len(LEER)):        
                print(f"{CONTADOR[i]}  {COBJETO[i]}  {LEER[i]}", end="", file=archivo)           
            for clave in dic:
                print("|" + clave + " , " + format(int(dic[clave][1]), '04X') + "|", file=archivo)
        print("Tu archivo LST se ha generado")
    except Exception as e:
        print(e)
        print("No se pudo generar LST")


# Función de hash para generar índices de clave en la tabla
def HASH(clave, tam):       
    valor_hash = 0                     
    for i, caracter in enumerate(clave):        
        valor_hash += ord(caracter) * (i + 1)        
    p = 17	                    
    a, b = 23, 56                 
    return ((a * valor_hash + b) % p) % tam   

# Función para generar el archivo HEX con el código ensamblado
def ARHEX(he, OR, NOMBRE):
    indice = 0
    checksum = 0
    linea_hex = ""
    hex_lines = []
    direcciones_iniciales = [format(OR, '04X')]
    tamaños = []
    checksums = []
    for i in range(len(he) // 2):
        if (indice / 32) == 1:
            checksum += 16 + int(format(OR - 16, '04X')[:2], 16) + int(format(OR - 16, '04X')[-2:], 16)
            checksums.append(format(int(compA2(list(format(checksum, '016b')), 15), 2), '04X')[-2:])
            tamaños.append(format(indice // 2, '02X'))
            direcciones_iniciales.append(format(OR, '04X'))
            hex_lines.append(linea_hex)
            indice = 0
            checksum = 0
            linea_hex = ""
        OR += 1
        checksum += int(he[2 * i:2 * i + 2], 16)    
        indice += 2
        linea_hex += he[2 * i:2 * i + 2]
    checksum += (indice // 2) + int(format(OR - (indice // 2), '04X')[:2], 16) + int(format(OR - (indice // 2), '04X')[-2:], 16)
    hex_lines.append(linea_hex)
    tamaños.append(format(indice // 2, '02X'))
    checksums.append(format(int(compA2(list(format(checksum, '016b')), 15), 2), '04X')[-2:])
    try:    
        with open(NOMBRE + ".HEX", 'w') as archivo:
            for i in range(len(hex_lines)):
                print(":" + tamaños[i] + direcciones_iniciales[i] + "00" + hex_lines[i] + checksums[i], file=archivo)
            print(":00000001FF", file=archivo)
        print("Tu archivo HEX se ha generado")
    except Exception as e:
        print("No se pudo generar HEX")
    return 

# Función para añadir elementos a la tabla hash
def FORMATO(tabla, cadena):
    tabla[HASH(cadena[0], len(tabla))].append((cadena[0], cadena[1], cadena[2]))


RegistrosJIJIJ = {"B":"000","C":"001","D":"010","E":"011","H":"100","L":"101","A":"111","BC":"00","DE":"01","HL":"10","IX":"10","IY":"10","SP":"11","AF":"11"}
cond = {"NZ":"000","Z":"001", "NC":"010","C":"011", "PO":"100", "PE":"101","P": "110", "M":"111"}

# Función para traducir las instrucciones de ensamblador a código máquina
def TRAD(cadena, codigos, CLJR):
    patron_registro = re.compile(r'[A-E]|H|L')
    patron_numero_final = re.compile(r'(\d+)$')
    patron_numero = re.compile(r'-*\d+')
    patron_ixyr = re.compile(r'(\(I(X|Y)\+\d+\))')
    patron_instrucciones = re.compile(r'ADD|LD|INC|ADC|SUB|AND|OR|CP|DEC|')
    patron_condicionales = re.compile(r'NZ|Z|NC|C|PO|PE|P|M')
    patron_sustitucion_jp = re.compile(r'JP|CALL')
    patron_ld_datos = re.compile(r'\s*((LD)\s+(HL|(\(\d+\))),\s+(HL|(\(\d+\)))|((LD)\s+(A|(\(\d+\))),\s+((A|(\(\d+\))))))\s*')
    
    if patron_ld_datos.match(cadena):
        numero_encontrado = int(patron_numero.search(cadena).group())
        if numero_encontrado <= 65536:
            codigos[2] = format(numero_encontrado, "016b")
            return patron_numero.sub("nn", cadena), codigos
        else:
            return None

    patron_ld_add = re.compile(r'\s*((((LD)\s+(([A-E]|H|L)|(\d+)|(\(I(X|Y)\+\d+\))),\s+(([A-E]|H|L)|(-*\d+)|(\(I(X|Y)\+\d+\))))|(LD)\s+((\(I(X|Y)\+\d+\)),\s+(([A-E]|H|L)|(\d+))))|(((ADD|ADC|SUB|AND|OR|CP)\s+(([A-E]|H|L)|(\d+)|(\(I(X|Y)\+\d+\))))|((INC|DEC)\s+((([A-E]|H|L)|(\(I(X|Y)\+\d+\))))))\s*$|(\s*IN\s+(T|([A-E]|H|L)),\s+(\(\d+\)|\(K\))\s*|\s*(OUT)\s+\(K\),\s+([A-E]|H|L)))')

    if patron_ld_add.match(cadena):
        mnemonicos = patron_instrucciones.findall(cadena)
        cadena = patron_instrucciones.sub("WV", cadena)
        codigos[0] = RegistrosJIJIJ.get(patron_registro.search(cadena).group()) if patron_registro.search(cadena) else "None"
        cadena_temp = patron_registro.sub("r", cadena, 1)
        codigos[1] = RegistrosJIJIJ.get(patron_registro.search(cadena_temp).group()) if patron_registro.search(cadena_temp) else "None"
        cadena_temp2 = patron_registro.sub("t", cadena_temp, 1)

        if patron_ixyr.search(cadena_temp):
            valor_numero = int(patron_numero.search(patron_ixyr.search(cadena_temp).group()).group())
            if valor_numero <= 255:
                cadena_temp2 = patron_ixyr.sub(patron_numero.sub("d", patron_ixyr.search(cadena_temp).group()), cadena_temp2)
                codigos[3] = format(valor_numero, "08b")
            else:
                return None
            
        if patron_numero.search(cadena_temp2):
            numero = int(patron_numero.search(cadena_temp2).group())
            if -128 <= numero <= 255:
                codigos[2] = negativoBin(list(format(abs(numero), "08b")), 7) if numero < 0 else format(abs(numero), "08b")
                cadena_temp2 = patron_numero.sub("n", cadena_temp2)
            else:
                return None

        for mnemonico in mnemonicos:
            cadena_temp2 = cadena_temp2.replace("WV", mnemonico, 1)

        return cadena_temp2, codigos

    patron_jp_call = re.compile(r'\s*(JP|CALL)\s+((\d+)|(NZ|Z|NC|C|PO|PE|P|M))(|,)\s+((\d+)|)\s*')
    
    if patron_jp_call.match(cadena):
        instruccion_guardada = ""
        if patron_sustitucion_jp.search(cadena):
            instruccion_guardada = patron_sustitucion_jp.search(cadena).group()
            cadena = patron_sustitucion_jp.sub('WV', cadena)
        
        codigos[0] = cond.get(patron_condicionales.search(cadena).group()) if patron_condicionales.search(cadena) else "NADA"
        cadena = patron_condicionales.sub("cc", cadena)
        numero_encontrado = int(patron_numero.search(cadena).group())
        
        if numero_encontrado <= 65536:
            cadena = cadena.replace('WV', instruccion_guardada)
            codigos[2] = format(numero_encontrado, "016b")
            return patron_numero.sub("nn", cadena), codigos

        else:
            return None
    
    JRRE = re.compile(r'\s*((JR|DJNZ)\s+(((\d+)\s*)|((C|NC|Z|NZ),\s+(\d+)\s*)))')
    if JRRE.match(cadena) != None:
        Numeronn = int(patron_numero.search(cadena).group())
        if ((Numeronn-(CLJR+2) )> -126 and (Numeronn-(CLJR+2)<129)):#Caso ya que solo se puede mover 255 lugares creo jijiji
            Numeronn = Numeronn - (CLJR+2) 
            if Numeronn<0:
                bin12 = format(abs(Numeronn),"08b")
                codigos[2] = negativoBin(list(bin12),7)
            else:
                codigos[2] = format(Numeronn,"08b") #Solo nos importa la diferencia 
            return (patron_numero.sub("e",cadena),codigos)
        else:
            return None

# Función para obtener el complemento a 2 de un número binario negativo
def negativoBin(binario, t):
    for i in range(t, -1, -1):
        if binario[i] == "1":
            for k in range(i):
                binario[k] = "1" if binario[k] == "0" else "0"
            break
    return ''.join(binario)


#MAIN
if __name__ == '__main__':
    MiTabla = tabla(100) 
    generar_hex = True
    generar_lst = True  
    nombre_archivo = input("Nombre del archivo para ensamblar: ")
    direccion_archivo = f"{nombre_archivo}.ASM"
    
    LEER = []
    inicio = time.time()
    try:
        with open("MNEMONICOS.txt") as archivo:  
            for linea in archivo:
                linea = linea.split(",")
                linea[2] = linea[2].replace("\n", "")
                FORMATO(MiTabla, linea)
    except FileNotFoundError:
        print("No se encuentra el archivo de mnemonicos en el directorio")
        exit()
    
    try: 
        with open(direccion_archivo) as archivo:
            LEER = archivo.readlines()
    except FileNotFoundError:
        print(direccion_archivo + " no localizado")
        exit()

    Limpiando = re.compile(r'\.ASM(.*)')
    NOMBRE = Limpiando.sub("", direccion_archivo)
    
    resultado_pasadas = Pasadas(LEER)
    patron_espacios = re.compile('[\t\n]')
    
    if not resultado_pasadas[2]:
        print("No se encontraron errores, todo bien :D")
    else:
        print("Hay errores en:")
        for error in resultado_pasadas[2]:
            print(error)
    
    if generar_hex:  
        if not resultado_pasadas[2]:
            ARHEX(patron_espacios.sub("", ''.join(resultado_pasadas[1])), resultado_pasadas[3], NOMBRE)
        else: 
            print("Hay error en el codigo objeto")
            print("No se pudo generar el archivo HEX")    
    if generar_lst:
        ARLST(resultado_pasadas[0], resultado_pasadas[1], LEER, resultado_pasadas[4], NOMBRE, resultado_pasadas[3])

