import static org.junit.Assert.*;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.util.*;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

import Practica1.Deportista;

public class Corrector {

	float delta = (float) 0.001;

	Deportista d1;
	
 	@Before
	public void setUp() throws Exception {
 		d1 = new Deportista(100, false, 34, 175);
 	}
	
	@Test (timeout=500)
	public void test_dormir1() {
		try{
			d1.dormir();
			if( Math.abs(d1.getPeso()-99.768) > delta )
				fail("<p>La clase Deportista no funciona bien cuando se duerme sin comer ni hacer ejercicio. </p>");
		}catch(Exception e){
			fail("<p>dormir no funciona bien. </p>");
		}
	}

	@Test (timeout=500)
	public void test_practicarCiclismo() {
		try{
			d1.practicarCiclismo(60);
			d1.dormir();
			if( Math.abs(d1.getPeso()-99.680) > delta )
				fail("<p>La clase Deportista no funciona bien cuando se coge la bici y duerme. </p>");
		}catch(Exception e){
			fail("<p>practicarCiclismo no funciona bien. </p>");
		}
	}
	
	@Test (timeout=500)
	public void test_practicarCarrera() {
		try{
			d1.practicarCarrera(60);
			d1.dormir();
			if( Math.abs(d1.getPeso()-99.608) > delta )
				fail("<p>La clase Deportista no funciona bien cuando corre y duerme. </p>");
		}catch(Exception e){
			fail("<p>practicarCarrera no funciona bien. </p>");
		}
	}
	
	@Test (timeout=500)
	public void test_comer1() {
		try{
			d1.comer(1500);
			d1.dormir();
			if(Math.abs(d1.getPeso()-99.935) > delta)
				fail("<p>La clase Deportista no funciona bien cuando come poco y duerme. </p>");
		}catch(Exception e){
			fail("<p>comer no funciona bien. </p>");
		}
	}

	@Test (timeout=500)
	public void test_comer2() {
		try{
			d1.comer(15000);
			d1.dormir();
			if(Math.abs(d1.getPeso()-101.435) > delta)
				fail("<p>La clase Deportista no funciona bien cuando come mucho y duerme. </p>");
		}catch(Exception e){
			fail("<p>comer no funciona bien. </p>");
		}
	}

	@Test (timeout=500)
	public void test_comer3() {
		try{
			d1.comer(1000);
			d1.comer(1000);
			d1.comer(1000);
			d1.dormir();
			if(Math.abs(d1.getPeso()-100.101) > delta)
				fail("<p>La clase Deportista no funciona bien cuando come varias veces y duerme. </p>");
		}catch(Exception e){
			fail("<p>comer no funciona bien. </p>");
		}
	}

	@Test (timeout=500)
	public void test_comer4() {
		try{
			int almuerzo [] = {325, 200};
			d1.comer(almuerzo);
			d1.dormir();
			if(Math.abs(d1.getPeso()-99.826) > delta)
				fail("<p>La clase Deportista no funciona bien cuando come una comida de varios platos y duerme. </p>");
		}catch(Exception e){
			fail("<p>comer no funciona bien. </p>");
		}
	}

	@Test (timeout=500)
	public void test_comer5() {
		try{
			int almuerzo [] = {325, 200};
			d1.comer(almuerzo);
			d1.comer(almuerzo);
			d1.dormir();
			if(Math.abs(d1.getPeso()-99.885) > delta)
				fail("<p>La clase Deportista no funciona bien cuando come varias comidas de varios platos y duerme. </p>");
		}catch(Exception e){
			fail("<p>comer no funciona bien. </p>");
		}
	}

	@Test (timeout=500)
	public void test_comer6() {
		try{
			int almuerzo [] = {325, 200};
			d1.comer(almuerzo);
			d1.comer(3000);
			d1.comer(almuerzo);
			d1.dormir();
			if(Math.abs(d1.getPeso()-100.218) > delta)
				fail("<p>La clase Deportista no funciona bien cuando come varias comidas de varios platos y comidas individuales. </p>");
		}catch(Exception e){
			fail("<p>comer no funciona bien. </p>");
		}
	}

	@Test (timeout=500)
	public void test_todo() {
		try{
			d1.comer(100);
			int almuerzo [] = {325, 200};
			d1.comer(almuerzo);
			int comida [] = {139, 552, 190};
			d1.comer(comida);
			d1.comer(36);
			int cena [] = {350, 200, 400};
			d1.comer(cena);
			d1.practicarCiclismo(60);
			d1.practicarCarrera(60);
			d1.dormir();
			if(Math.abs(d1.getPeso()-99.797) > delta)
				fail("<p>La clase Deportista no funciona bien cuando combina comidas y ejercicios. </p>");
		}catch(Exception e){
			fail("<p>comer no funciona bien. </p>");
		}
	}

	public static void main(String args[]) throws FileNotFoundException {

		//No dejamos que el alumno escriba en la salida 
		
		
		//Pasamos las pruebas
		Result result = JUnitCore.runClasses(Corrector.class);
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
				//System.out.println(fails);
			}
		}
		
		//System.setOut(o);
		//Para depurar en Eclipse
		System.out.println(result.getRunCount());
		System.out.println(result.getFailureCount());
		System.out.println(fails);
                //System.out.println(result.wasSuccessful());
		
		//PrintWriter out = new PrintWriter("/home/user/PROG/corrector/Corrector/p3/src/ejecucion.txt");
		
		//Para desplegar en l048
		//PrintWriter out = new PrintWriter(args[0]);
		//out.println(result.getRunCount());
		//out.println(result.getFailureCount());
		//out.println(fails);
		//out.flush();
		//out.close();
		
		//System.exit(-1);
	}
}
