package chess;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class CheckInput {
	
	public static boolean checkCoordinateValidity(String input){
		Pattern p = Pattern.compile("^[1-8]{1}[a-h]{1}?$");
		Matcher m = p.matcher(input);
		boolean b = m.matches();

		if(b){
			return true;
		}
		else{
			return false;
		}
	}
}
