package board;
import java.util.*;
import cards.Card;

public class CardList {
    private ArrayList<Card> cList;

    public CardList(){
        this.cList = new ArrayList<Card>();
    }

    public void add(Card c) {
        this.cList.add(0, c);
    }

    public int size(){
        return this.cList.size();
    }

    public Card getElementAt(int n){
        return this.cList.get(n);
    }

    public Card removeCardAt(int n){
        return this.cList.remove(n);
    }

}
