package board;
import java.util.*;
import cards.*;


public class Board {
    private static CardPile forestCardsPile;
    private static CardList forest;
    private static ArrayList<Card> decayPile;

    public static void initialisePiles(){
        forest = new CardList();
        forestCardsPile = new CardPile();
        decayPile = new ArrayList<Card>();
    }

    public static void setUpCards(){
        BirchBolete birchd = new BirchBolete(CardType.DAYMUSHROOM);
        BirchBolete birchn = new BirchBolete(CardType.NIGHTMUSHROOM);

        HoneyFungus honeyfungusd = new HoneyFungus(CardType.DAYMUSHROOM);
        HoneyFungus honeyfungusn = new HoneyFungus(CardType.NIGHTMUSHROOM);
        
        TreeEar treeeard = new TreeEar(CardType.DAYMUSHROOM);
        TreeEar treeearn = new TreeEar(CardType.NIGHTMUSHROOM);

        LawyersWig lawyerswigd = new LawyersWig(CardType.DAYMUSHROOM);
        LawyersWig lawyerswign = new LawyersWig(CardType.NIGHTMUSHROOM);

        Shiitake shiitaked = new Shiitake(CardType.DAYMUSHROOM);
        Shiitake shiitaken = new Shiitake(CardType.NIGHTMUSHROOM);

        HenOfWoods henofwoodsd = new HenOfWoods(CardType.DAYMUSHROOM);
        HenOfWoods henofwoodsn = new HenOfWoods(CardType.NIGHTMUSHROOM);
        
        Porcini porcinid = new Porcini(CardType.DAYMUSHROOM);
        Porcini porcinin = new Porcini(CardType.NIGHTMUSHROOM);

        Chanterelle chanterelled = new Chanterelle(CardType.DAYMUSHROOM);
        Chanterelle chanterellen = new Chanterelle(CardType.NIGHTMUSHROOM);

        Morel moreld = new Morel(CardType.DAYMUSHROOM);

        Butter butter = new Butter();
        Cider cider = new Cider();

        Pan pan = new Pan();
        Basket basket = new Basket();
        //System.out.println(forestCardsPile.pileSize());
        // Adding the cards into the pile
        // Adding the daymushrooms
        for(int i = 0; i < 4; i++){
            getForestCardsPile().addCard(birchd);
            getForestCardsPile().addCard(porcinid);
            getForestCardsPile().addCard(chanterelled);
        }
        
        for(int i = 0; i < 10; i++){
            getForestCardsPile().addCard(honeyfungusd);           
        }

        for(int i = 0; i < 8; i++){
            getForestCardsPile().addCard(treeeard);
        }

        for(int i = 0; i < 6; i++){
            getForestCardsPile().addCard(lawyerswigd);
        }

        for(int i = 0; i < 5; i++){
            getForestCardsPile().addCard(shiitaked);
            getForestCardsPile().addCard(henofwoodsd);
        }
        
        for(int i = 0; i < 3; i++){
            getForestCardsPile().addCard(moreld);
        }

        //Adding the nightmushrooms
        getForestCardsPile().addCard(honeyfungusn);
        getForestCardsPile().addCard(treeearn);
        getForestCardsPile().addCard(lawyerswign);
        getForestCardsPile().addCard(shiitaken);
        getForestCardsPile().addCard(henofwoodsn);
        getForestCardsPile().addCard(birchn);
        getForestCardsPile().addCard(porcinin);
        getForestCardsPile().addCard(chanterellen);
        
        //Adding the other cards
        for(int i = 0; i < 3; i++){
            getForestCardsPile().addCard(butter);
            getForestCardsPile().addCard(cider);
        }
        for(int i = 0; i < 11; i++){
            getForestCardsPile().addCard(pan);     
        }
        for(int i = 0; i< 5; i++){
            getForestCardsPile().addCard(basket);
        }
        //System.out.println(getForestCardsPile().pileSize());
        
    }

    public static CardPile getForestCardsPile(){
        return forestCardsPile;
    }

    public static CardList getForest(){
        return forest;
    } 

    public static ArrayList<Card> getDecayPile(){
        return decayPile;
    }
    public static void updateDecayPile(){
        if (getDecayPile().size() != 4){
            getDecayPile().add(forest.getElementAt(forest.size()-1));
            getForest().removeCardAt(forest.size()-1);
        }
        else{
            getDecayPile().clear();
            getDecayPile().add(forest.getElementAt(forest.size()-1));
            getForest().removeCardAt(forest.size()-1);
        }
    }
    public static void clearDecayPile(){
        getDecayPile().clear();
    }
}
