public class Book {
    static String title;
    static Author author;
    static int items;

    public Book(String Title, Author writer, int quant){
        setTitle(Title);
        setAuthor(writer);
        setItems(quant);
    }

    public String getTitle(){
       return Book.title; 
    }

    public Author getAuthor(){
        return Book.author; 
    }
    
    public int getItems(){
        return Book.items; 
    }

    public void setTitle(String Title){
        Book.title = Title; 
    }

    public void setAuthor(Author writer){
        Book.author = writer; 
    }

    public void setItems(int quant){
        Book.items = quant; 
    }
}
