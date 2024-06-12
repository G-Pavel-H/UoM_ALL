package board;
import java.util.*;
import cards.*;

public class Hand implements Displayable {
    private ArrayList<Card> handList = new ArrayList<>();

    public void add(Card c){
        this.handList.add(c);
    }

    public int size(){
        return this.handList.size();
    }

    public Card getElementAt(int i){
        return this.handList.get(i);
    }

    public Card removeElement(int i){
        return this.handList.remove(i);
    }

}
