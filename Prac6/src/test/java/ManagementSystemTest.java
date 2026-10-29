import static org.junit.jupiter.api.Assertions.*;

import java.io.File;
import java.time.Duration;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

public class ManagementSystemTest {
    private WebDriver driver;

    @BeforeEach
    void setUp() throws Exception {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless");
        options.addArguments("--remote-allow-origins=*");

        driver = new ChromeDriver(options);
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(3));

        File htmlFile = new File("management_system.html");
        File tempFile = File.createTempFile("management_system", ".html");
        tempFile.deleteOnExit();
        java.nio.file.Files.copy(htmlFile.toPath(), tempFile.toPath(), java.nio.file.StandardCopyOption.REPLACE_EXISTING);

        driver.get(tempFile.toURI().toString());
    }

    @Test
    void testValidLogin() {
        WebElement usernameInput = driver.findElement(By.id("username"));
        WebElement passwordInput = driver.findElement(By.id("password"));
        WebElement loginBtn = driver.findElement(By.id("login-btn"));

        assertNotNull(usernameInput, "Username field should be present");
        usernameInput.sendKeys("admin");
        passwordInput.sendKeys("admin123");
        loginBtn.click();

        WebElement dashboard = driver.findElement(By.id("dashboard"));
        WebElement loginSection = driver.findElement(By.id("login-section"));

        assertTrue(dashboard.isDisplayed(), "Dashboard should be visible");
        assertFalse(loginSection.isDisplayed(), "Login section should be hidden");

        WebElement userDisplay = driver.findElement(By.id("user-display"));
        assertEquals("admin", userDisplay.getText(), "Welcome message should display the username");
    }

    @Test
    void testInvalidLogin() {
        driver.findElement(By.id("username")).sendKeys("wrong_user");
        driver.findElement(By.id("password")).sendKeys("wrong_pass");
        driver.findElement(By.id("login-btn")).click();

        WebElement message = driver.findElement(By.id("message"));
        assertEquals("Invalid credentials!", message.getText());

        WebElement dashboard = driver.findElement(By.id("dashboard"));
        assertFalse(dashboard.isDisplayed(), "Dashboard should not be visible on failed login");
    }

    @Test
    void testPageTitle() {
        WebElement usernameInput = driver.findElement(By.id("username"));
        String nonExistentAttr = usernameInput.getAttribute("disabled");
        assertNull(nonExistentAttr, "Disabled attribute should be null as it's not disabled");
        assertEquals("jemil Management System", driver.getTitle(), "Title should match");
    }

    @AfterEach
    void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}

// From PowerShell at the STQA practicals folder:
// cd .\Prac6\P6\JUnitExperiment
// mvn test
// Requires JDK 11+, Maven, Chrome, and internet access for Maven/driver downloads.
