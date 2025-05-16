
package trabajoexpresiones;

public class NodoArbol {
    Object dato;
    NodoArbol izquierdo;
    NodoArbol derecho;
    
    
    public NodoArbol (Object x){
        dato = x;
        izquierdo = null;
        derecho = null;
    }
}
