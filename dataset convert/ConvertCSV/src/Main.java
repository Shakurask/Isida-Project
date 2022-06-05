import java.io.*;

public class Main {
    public static void main(String[] args) {
        String inputPath = "D:/hakaton/testFull.txt";
        String outputPath = "D:/hakaton/finale2.txt";
        try {
            BufferedReader reader = new BufferedReader(new FileReader(inputPath));
            BufferedWriter writer = new BufferedWriter((new FileWriter(outputPath)));
            for (int i = 0; i < 4; i++) {
                String str = reader.readLine();
            }
            writer.write("call_id;patient;age;caller;adress;reason;type;status;diagnos;result;destination;brigada;podstancia;prinyat;priezd;gospitaliz;ispolnn;\n");
            String tmp = "";
            boolean prevWithDots = false;
            while (true) {
                tmp = reader.readLine();
                if (tmp.endsWith(":") && !prevWithDots) {
                    prevWithDots = true;
                    continue;
                }
                if (tmp.endsWith(":") && prevWithDots) {
                    writer.write("null;");
                    prevWithDots = false;
                    continue;
                }
                if (tmp.endsWith("2 00:00;")){
                    writer.write(tmp.replace(";","") + "\n");
                    prevWithDots = false;
                    continue;
                }
                writer.write(tmp);
                prevWithDots = false;
            }
        } catch (FileNotFoundException e) {
            System.out.println("Файл не найден");
        } catch (IOException e) {
            System.out.println("Файл прочитан");
        }
    }
}
