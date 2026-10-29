import java.io.File;
public class URITest {
    public static void main(String[] args) {
        System.out.println(new File("management_system.html").getAbsolutePath());
        System.out.println(new File("management_system.html").toURI().toString());
    }
}
