package idoft.auto.update;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;
import org.openqa.selenium.By;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import io.github.bonigarcia.wdm.WebDriverManager;

public class Main {
	private static int count = 0;
	private static ArrayList<String> columnValues = new ArrayList<String>();
	private static ArrayList<Integer> ignore = new ArrayList<Integer>();
	private void readData() {
		Scanner scanner, scanner1;
		int i=0;	
		try {
			File f = new File("/home/runner/work/idoft/idoft/pr-data.csv");
			scanner = new Scanner(f);
			scanner1 = new Scanner(new File("ignore.csv"));
			while (scanner.hasNextLine()) {
				String values = scanner.nextLine();
				columnValues.add(values);
				count++;
			}
			while (scanner1.hasNextLine()) {
				if (i == 0) {
					String values = scanner1.nextLine();
					i++;
				} else {
					String values = scanner1.nextLine();
					System.out.println(Integer.parseInt(values));
					ignore.add(Integer.parseInt(values));
				}
			}
			f = null;
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}
	private boolean isIgnoreLine(int i) {
		if (ignore.contains(i))
			return true;
		return false;
	}
	private String status(String url) {
		WebDriverManager.chromedriver().setup();
		ChromeOptions ChromeOptions = new ChromeOptions();
		ChromeOptions.addArguments("--headless", "window-size=1024,768", "--no-sandbox");
		WebDriver driver = new ChromeDriver(ChromeOptions);
		try {
			driver.get(url);
			String status = driver.findElement(By.className("State")).getText();
			String sstatus;
			if (status.equals("Open"))
				sstatus = "Opened";
			else if (status.equals("Merged"))
				sstatus = "Accepted";
			else
				sstatus = "Rejected";

			return sstatus;
		} catch (NoSuchElementException e) {
			return "Opened";
		} finally {
			driver.close();
		}

	}

	public int getStatuses() {
		try {
			readData();
			FileWriter fw;
			String[] status = new String[count];
			status[0] = columnValues.get(0);
			for (int i = 1; i < count; i++) {
				String[] tmp = columnValues.get(i).split(",", -1);
				if (columnValues.get(i).contains("Opened") && !isIgnoreLine(i)) {
					String url = tmp[6];
					tmp[5] = status(url);
					status[i] = String.join(",", tmp);
					System.out.println(status[i]);
				} else if (tmp.length < 6)
					status[i] = columnValues.get(i);
				else
					status[i] = columnValues.get(i);
				System.out.println(i);
				if (i % 200 == 0)
					Thread.sleep(20000);
			}
			fw = new FileWriter("/home/runner/work/idoft/idoft/pr-data.csv");
			int i = 0;
			while (i < count) {
				fw.write(status[i] + "\n");
				i++;
			}
			fw.flush();
			fw.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return -1;
		} catch (InterruptedException e) {
			e.printStackTrace();
			return -1;
		}
		System.out.println("Process finished!");
		return 0;
	}

}
