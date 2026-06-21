public class PruebaCesarDelgado {
    public static void main(String[] args) {
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
}
