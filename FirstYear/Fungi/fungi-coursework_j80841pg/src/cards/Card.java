package cards;
public class Card {

    protected CardType type;
    protected String cardName;

    public Card(CardType t, String n){
        this.type = t;
        this.cardName = n;
    }

    public CardType getType(){
        return type;
    }

    public String getName(){
        return cardName;
    }
}
