package board;
import java.util.*;
import cards.Card;

public class CardPile {
    private Stack<Card> cPile;

    public CardPile(){
        this.cPile = new Stack<Card>();
    }

    public void addCard(Card c){
        this.cPile.push(c);
    }

    public Card drawCard(){
        return this.cPile.pop();
    }

    public void shufflePile(){
        Collections.shuffle(this.cPile);
    }

    public int pileSize(){
       return this.cPile.size();
    }

    public boolean isEmpty(){
        return this.cPile.isEmpty();
    }
}
