package cards;

public class EdibleItem extends Card {
    protected int flavourPoints;

    public EdibleItem(CardType t, String n){
        super(t, n);
    }

    public int getFlavourPoints(){
        return flavourPoints;
    }
}
