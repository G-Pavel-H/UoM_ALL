package board;
import java.util.*;
import cards.*;

public class Display implements Displayable {
    private ArrayList<Card> displayList = new ArrayList<>();

    public void add(Card c){
        this.displayList.add(c);
    }

    public int size(){
        return this.displayList.size();
    }

    public Card getElementAt(int i){
        return this.displayList.get(i);
    }

    public Card removeElement(int i){
        return this.displayList.remove(i);
    }

    
}
