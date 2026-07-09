
    public static void main(String[] args) {
        // Palabras reservadas de Jonathan Pacalla
        if (true) {
            int a = 5;
            float b = 2.5f;
            double c = 3.14;
            long d = 100L;
            short e = 10;
            byte f = 1;
            char g = 'A';
            boolean h = true;
            boolean i = false;
            
            // Operadores bitwise de Jonathan Pacalla
            int bitwise_and = a & 3;     // BIT_AND
            int bitwise_or = a | 2;      // BIT_OR
            int bitwise_xor = a ^ 1;     // BIT_XOR
            int bitwise_not = ~a;        // BIT_NOT
            int left_shift = a << 1;     // LSHIFT
            int right_shift = a >> 1;    // RSHIFT
            
            // Operador ternario de Jonathan Pacalla
            int max = (a > 3) ? a : 3;   // QUESTION
            
            System.out.println("Prueba Jonathan Pacalla:");
            System.out.println("Palabras reservadas: if, int, float, double, long, short, byte, char, boolean, true, false");
            System.out.println("Operadores bitwise:");
            System.out.println("a & 3 = " + bitwise_and);
            System.out.println("a | 2 = " + bitwise_or);
            System.out.println("a ^ 1 = " + bitwise_xor);
            System.out.println("~a = " + bitwise_not);
            System.out.println("a << 1 = " + left_shift);
            System.out.println("a >> 1 = " + right_shift);
            System.out.println("Operador ternario: max = " + max);
        }
    }
