public class Library {
    Book[] bookList;
    static int currentNumberOfUniqueBooks;
    static int i = 0;
    Library(int capacity){
        bookList = new Book[capacity];
    }

    public void addBook(Book book){
        bookList[i] = new Book(book.getTitle(), book.getAuthor(), book.getItems());
        i++;
        currentNumberOfUniqueBooks = bookList.length;
        System.out.println(currentNumberOfUniqueBooks);
    }

    public void whichBooks(){
        for (int i=0; i < bookList.length; i++){
            System.out.println(bookList[i]);
        }
    }

    public void whichAuthors(){
        for (int i=0; i < bookList.length; i++){
            Book book_author = bookList[i];
            Author current_author = book_author.getAuthor();
            String current_name = current_author.getAuthorName();
            System.out.println(current_name);
        }
    }

    public void borrowBook(Book book1){
        int available = book1.getItems();
        
        if (available >= 1){
            System.out.println("Book has successfully been booked!");
            available -= 1;
            book1.setItems(available);
            if (available == 0){
                currentNumberOfUniqueBooks -= 1;
            }
        }
        else{
            System.out.println("Book is not available at the moment");
        }
    }

    public void returnBook(Book book2){
        int current_quant = book2.getItems();
        current_quant += 1;
        book2.setItems(current_quant);
        System.out.println("Book was successfully retirned, Thanks You!");
    }

    public static void main(String[] args){
        System.out.println("Starting my new library\n");
        //1. Create library
        Library l= new Library(100);
        //2. Populate library
        //Add 'Oscar Wilde' as a new author
        Author a1 = new Author("Oscar Wilde", 1889);
        //Add three items of 'The Importance of Being Earnest' to the library
        Book b1 = new Book("The Importance of Being Earnest", a1, 3);
        l.addBook(b1);
        System.out.println(l.bookList);
        //Add two items of 'The Picture of Dorian Gray' to the library
        Book b2 = new Book("The Picture of Dorian Gray", a1, 2);
        l.addBook(b2);
        //Add 'Charles Dickens' as a new author
        Author a2 = new Author("Charles Dickens", 1812);
        //Add three items of 'The Picture of Oliver Twist' to the library
        Book b3 = new Book("Oliver Twist", a2, 3);
        l.addBook(b3);
        //3. Explore library
        l.whichBooks();
        l.whichAuthors();
        //4. Interact with the library
        //Borrow Oliver Twist
        l.borrowBook(b3);
        //Return Oliver Twist
        l.returnBook(b3);
        //Borrow more than available
        l.borrowBook(b2);
        l.borrowBook(b2);
        l.borrowBook(b2);
        
    }
}

