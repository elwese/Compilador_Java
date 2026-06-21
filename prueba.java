public class prueba {
    // Prueba de Cesar Delgado
    public static void pruebaCesarDelgado() {
        int edad = 20;
        float nota = 8.5f;

        char inicial = 'C';
        String nombre = "Cesar";

        if (edad >= 18) {
            edad++;
        }

        if (nota != 10.0f) {
            nota -= 0.5f;
        }

        System.out.println("Prueba Cesar Delgado:");
        System.out.println("edad = " + edad + " nota = " + nota);
        System.out.println("inicial = " + inicial + " nombre = " + nombre);
    }

    // Prueba añadida por Jonathan Pacalla
    public static void pruebaJonathanPacalla() {
        int a = 5;
        int b = 2;

        int c = a & b;     
        int d = a | b;      
        int e = a ^ b;      
        int f = a << b;     
        int g = a >> b;     
        int h = (a > b) ? a : b; 

        System.out.println("Prueba Jonathan Pacalla:");
        System.out.println("a=" + a + " b=" + b);
        System.out.println("c (a&b)=" + c + " d (a|b)=" + d + " e (a^b)=" + e);
        System.out.println("f (a<<b)=" + f + " g (a>>b)=" + g + " h=" + h);
    }

    // main para ejecutar ambas pruebas
    public static void main(String[] args) {
        pruebaCesarDelgado();
        pruebaJonathanPacalla();
    }
}
