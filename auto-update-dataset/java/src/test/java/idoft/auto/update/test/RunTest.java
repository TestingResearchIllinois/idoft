package idoft.auto.update.test;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import idoft.auto.update.Main;

public class RunTest {
	@Test
	public void runTest() {
		Main m=new Main();
		int n= m.getStatuses();
		Assertions.assertEquals(0, n);
	}
}
