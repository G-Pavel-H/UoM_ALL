//import org.junit.jupiter.api.Test;
//import static org.junit.jupiter.api.Assertions.assertEquals;

public class Author{
  static String name;
  static int yearOfBirth;

  public Author(String fname, int birth){
    setAuthorName(fname);
    setYearOfBirth(birth);
  }

  public String getAuthorName(){
    return Author.name;
  }

  public void setAuthorName(String fname){
    Author.name = fname;
  }

  public int getYearOfBirth(){
    return Author.yearOfBirth;
  }

  public void setYearOfBirth(int birth){
    Author.yearOfBirth = birth;
  }

}