
public class PruebaJoseSalazar {
    
    public static void main(String[] args) {
        int[] arreglo = {10, 20, 30, 40};
        int x = 15;
        int y = 7;
        int z = 3;

        x *= 2;  
        y /= 2;  
        z %= 2;  

        boolean condicionA = (x > 20) && (y < 10);
        boolean condicionB = !(z > 1) || (arreglo[0] < 5);

        if (condicionA) {
            System.out.println("La condicion A es verdadera.");
        } else if (condicionB) {
            System.out.println("La condicion B es verdadera.");
        }
        
        System.out.println("Fin de la prueba de Jose Salazar");
    }
}
