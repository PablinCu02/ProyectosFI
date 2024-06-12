   ORG 300

   LD B, (380);Numero a calcular el factorial
   LD A, B; Se pasa el contenido del registro B (el factorial) al acumulador
   CP 0; Se compara con 0
   JP Z, fact; Si es cero se manda a la etiqueta 'fact' para verificar si el otro valor es válido ('C')
   JP calcfact; Si no se cumple lo anterior, es un numero a calcular valido y comenzamos con los calculos
facto:
   LD B, 1; 
   JP fin; Finaliza el programa
fact:
   LD A,C; Si ingresa a esta etiqueta se pasa el contenido del registro C al acumulador
   CP 0; y se compara con cero
   JP Z, facto; Si es cero se manda a la etiqueta 'facto'
   DEC A; en caso contrario se decrementa en uno lo que tiene el acumulador
   CP 0; y se compara con cero
   JP Z, facto; en caso de que sea cero se manda a la etiqueta 'facto'
   JP calcfact; en caso contrario es un factorial valido y se manda a la etiqueta 'calcfact'



calcfact:
   PUSH B; Se agrega el factorial a calcular a la pila
   DEC B; Se decrementa en uno
   PUSH B; Se agrega a la pila el nuevo valor
   DEC B; Se decrementa una vez mas este ultimo valor 
   PUSH B; Se agrega a la pila

   POP E; Se saca el ultimo valor ingresado en pila al registro HL
   POP F; Se saca el penultimo valor agregado a pila al registro DE, este sera el contador que nos indicará cuantas veces hace falta realizar la multiplicacion

   POP B; Se agrega el numero inicial al registro BC
   PUSH E; Se ingresa HL a la pila
   LD E, 0; Se inicializa en cero el registro HL, en el se irá almacenando el resultado de la multiplicacion

 
verificar:
   ADD E, B; Se suma el contenido que esta en el registro HL mas lo que tiene el registro BC
   DEC F; Se decrementa el contador contenido en DE, se hizo la primera multiplicacion
   LD A, D; 
   CP 0; ¿Hemos terminado el cálculo?
   JP NZ, verificar; No, verificamos D
   JP Z, verificarcontenido; No, verificamos E
   ; En caso de que no se cumplan las dos anteriores, salta al sig calculo "multiplicacion"

verificarcontenido:
   LD A, E; ¿Hemos terminado el cálculo?
   CP 0;
   JP NZ, verificar;

multiplicacion:
   POP F; Se saca el ultimo valor de la pila, este representa los ciclos que faltan para completar el factorial
   DEC F; 
   PUSH F; 
   INC F; Se vuelve a incrementar en uno el registro DE
   PUSH E; E contiene el factorial hasta el momento
   POP B; 
   LD E ,0; 
   ;HL almacena temporalmente el resultado, se encarga de las operaciones
   LD A, D;
   CP 0; manda a la etiqueta 'fin' y termina el programa, ahora si el contador no es cero se manda a la etiqueta 'vertifde'
   JP NZ, vertifde;
   LD A, E;
   CP 0;
   JP NZ, vertifde;
   JP Z, fin; 
   
vertifde:
   ;Etiqueta parecida a "verificar" pero ésta nos da el salto hacia el final
   ADD E, B; 
   DEC F; Se decrementa el contador contenido en DE 
   LD A, D; 
   CP 0; 
   JP NZ, vertifde;
   LD A, E;
   CP 0;
   JP Z, multiplicacion;
   JP NZ, vertifde;

fin:
   PUSH B; BC contiene el factorial calculado en hexadecimal 
   LD (390), BC ; se almacenará en la localidad (1090h)
   HALT; Termina