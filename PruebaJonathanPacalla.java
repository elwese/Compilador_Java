public class PruebaJonathanPacalla {
    public static void main(String[] args) {
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
}
