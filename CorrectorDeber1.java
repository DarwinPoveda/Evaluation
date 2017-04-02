import org.junit.Test;
import static org.junit.Assert.assertEquals;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;
import Deber1.Program;


public class CorrectorDeber1 {

	@Test (timeout=500)
	public void test() {
		Program p = new Program();
		assertEquals(0, p.Puzzle(0));
		assertEquals(2, p.Puzzle(1));
		assertEquals(4, p.Puzzle(2));
	}

	public static void main(String[] args) {
		//Pasamos las pruebas
		Result result = JUnitCore.runClasses(CorrectorDeber1.class);
		String fails = "", cadena;

		//Si han fallado todos los tests es que su constructor va mal
		if(result.getFailureCount() == result.getRunCount()){
			if(result.getFailures().get(0).getMessage() == null){
				fails = "<p>No se han podido realizar pruebas a su entrega: Compruebe que el constructor de su clase funciona de forma correcta. </p>";
			}
		}
		//Recuperamos los mensajes de las pruebas que han fallado
		else {
			for (Failure failure : result.getFailures()) {
				cadena = failure.getMessage();
				//Si se produjo un timeout necesitamos saber en qu� m�todo para cambiar el mensaje
				if(cadena!=null && cadena.contains("timed out")){
					String metodo = failure.getTestHeader().split("_")[0];
					cadena = "<p>Error detectado al probar el m�todo "+metodo+": Ha excedido el tiempo de prueba. Compruebe que no tiene bucles infinitos en su c�digo.</p> ";
				}
				fails += cadena;
			}
		}		
		
		//System.out.println(result.wasSuccessful());
		//Para depurar en Eclipse
		System.out.println(result.getRunCount());
		System.out.println(result.getFailureCount());
		System.out.println(fails);
	}

}
