package cards;

public class Mushroom extends EdibleItem {
    protected int sticksPerMushroom;

    public Mushroom(CardType t, String n){
        super(t, n);
    }

    public int getSticksPerMushroom(){
        return sticksPerMushroom;
    }
}
