public class PruebaCesarDelgado {
    public static void main(String[] args) {
        int x = 10;
        double calculo = 2.5;
        boolean bandera = true;
        String mensaje = "Resultado final: ";
        //hola
        if (x > 5 && x > 10 ) {
            x = x + 5;
        } else {
            mensaje = "Error en bandera";
        }
        
        while (x < 20) {
            x = x + 1;
        }
        
        for (int i = 0; i < 3; i = i + 1) {
            calculo = calculo * 2.0;
        }
    }
}