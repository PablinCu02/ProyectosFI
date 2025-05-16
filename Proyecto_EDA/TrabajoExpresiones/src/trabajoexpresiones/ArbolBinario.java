
package trabajoexpresiones;

public class ArbolBinario {
    NodoArbol raiz;
    
    public ArbolBinario(){
        raiz = null;
    }
    
    public ArbolBinario (String cadena){
        raiz = creaArbolBE(cadena);
    }
    
    public void reiniciaArbol(){
        raiz = null;
    }
    
    public void creaNodo (Object dato){
        raiz = new NodoArbol (dato);
    }
    
    public NodoArbol creaSubArbol (NodoArbol dato2, NodoArbol dato1, NodoArbol operador){
        operador.izquierdo = dato1;
        operador.derecho = dato2;
        return operador;
    }
    
    public boolean arbolVacio(){
        return raiz == null;
    }
    
    private String preorden (NodoArbol subArbol, String c){
        String cadena;
        cadena = "";
        
        if(subArbol !=null){
            cadena = c + subArbol.dato.toString()+"\n"+preorden(subArbol.izquierdo, c) 
                    + preorden(subArbol.derecho,c);
        }
        return cadena;
    }
    
    private String inorden (NodoArbol subArbol, String c){
        String cadena; 
        cadena = "";
        if (subArbol != null){
            cadena = c + inorden (subArbol.izquierdo, c) + subArbol.dato.toString() +
                    "\n" + inorden (subArbol.derecho, c);
        }
        return cadena;
    }
    
    private String posorden (NodoArbol subArbol, String c){
        String cadena;
        cadena = "";
        if (subArbol != null){
            cadena = c + posorden (subArbol.izquierdo, c) + posorden (subArbol.derecho, c) 
                    + subArbol.dato.toString() + "\n";
        }
        return cadena;
    }
    
    public String toString (int a){
        String cadena = "";
        switch (a){
            case 0 -> cadena = preorden(raiz, cadena);
            case 1 -> cadena = inorden (raiz, cadena);
            case 2 -> cadena = posorden (raiz, cadena);
        }
        return cadena;
    }
    
    private int prioridad(char c){
        int p = 100;
        
        p = switch (c) {
            case '^' -> 30;
            case '*', '/' -> 20;
            case '+', '-' -> 10;
            default -> 0;
        }; //Aqui se asume que lo que debe estar en la pila es un valor 0
        return p;
    }
    
    private boolean esOperador (char c){
        boolean resultado;
        resultado = switch (c){
            case '(', ')', '^', '*', '/', '+', '-' -> true;
            default -> false;
        };
        return resultado;
    }
    
    private NodoArbol creaArbolBE (String cadena){
        PilaArbolExp PilaOperadores;
        PilaArbolExp PilaExpresiones;
        NodoArbol token;
        NodoArbol op1;
        NodoArbol op2;
        NodoArbol op;
        
        PilaOperadores = new PilaArbolExp ();
        PilaExpresiones = new PilaArbolExp ();
        
        char caracterEvaluado;
        
        for(int i = 0; i <cadena.length(); i++){
            caracterEvaluado = cadena.charAt(i);
            token = new NodoArbol (caracterEvaluado);
            if(!esOperador (caracterEvaluado)){
                PilaExpresiones.insertar(token);
            }
            else
                switch (caracterEvaluado){
                    case '(' -> PilaOperadores.insertar(token);
                    case ')' -> {
                        while(!PilaOperadores.pilaVacia() && !PilaOperadores.topePila().dato.equals('(')){
                            op2 = PilaExpresiones.quitar();
                            op1 = PilaExpresiones.quitar();
                            op = PilaOperadores.quitar();
                            op = creaSubArbol (op2, op1, op);
                            PilaExpresiones.insertar(op);
                        }
                        PilaOperadores.quitar();
                    }
                    default -> {
                        while(!PilaOperadores.pilaVacia() && prioridad(caracterEvaluado) <=
                                prioridad(PilaOperadores.topePila().dato.toString().charAt(0))){
                            op2 = PilaExpresiones.quitar();
                            op1 = PilaExpresiones.quitar();
                            op = PilaOperadores.quitar();
                            op = creaSubArbol (op2, op1, op);
                            PilaExpresiones.insertar(op);
                        }
                        PilaOperadores.insertar(token);
                    }
                }
                
        }
        while (!PilaOperadores.pilaVacia()){
            op2 = PilaExpresiones.quitar();
            op1 = PilaExpresiones.quitar();
            op = PilaOperadores.quitar();
            op = creaSubArbol (op2, op1, op);
            PilaExpresiones.insertar(op); 
        }
        op = PilaExpresiones.quitar();
        return op;
    }
    
    public double EvaluaExpresion(){
        return evalua(raiz);
    }
    
    private double evalua (NodoArbol subArbol){
        double acum = 0;
        if (!esOperador (subArbol.dato.toString().charAt(0))){
            return Double.parseDouble(subArbol.dato.toString());
        }
        else{
            switch (subArbol.dato.toString().charAt(0)){
                case '^' -> acum = acum + Math.pow(evalua(subArbol.izquierdo), evalua(subArbol.derecho));
                case '*' -> acum = acum + evalua(subArbol.izquierdo) * evalua(subArbol.derecho);
                case '/' -> acum = acum + evalua(subArbol.izquierdo) / evalua(subArbol.derecho);
                case '+' -> acum = acum + evalua(subArbol.izquierdo) + evalua(subArbol.derecho);
                case '-' -> acum = acum + evalua(subArbol.izquierdo) - evalua(subArbol.derecho); 
            }
            return acum;
        }
    }
    
}

