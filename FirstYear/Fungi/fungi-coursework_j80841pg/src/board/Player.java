package board;
import java.util.*;
import cards.*;

public class Player {
    private Hand h;
    private Display d;
    private int score;

    private int handlimit;
    private int sticks;

    public Player(){
        this.h = new Hand();
        this.d = new Display();
        this.score = 0;
        this.handlimit = 8;
        this.sticks = 0;
        Pan pan = new Pan();
        d.add(pan);
        
    }

    public int getScore(){
        return this.score;
    }

    public int getHandLimit(){
        return this.handlimit;
    }

    public int getStickNumber(){
        return this.sticks;
    }

    public void addSticks(int n){
        this.sticks = this.sticks + n;
        Card c = new Stick();
        for (int i = 0; i < n; i++){
            addCardtoDisplay(c);
        }
    }

    public void removeSticks(int n ){
        this.sticks = this.sticks - n;
        int count = 0;
        for (int i = 0; i < getDisplay().size(); i++){

                if(getDisplay().getElementAt(i).getType().equals(CardType.STICK)){
                    getDisplay().removeElement(i);
                    i--;
                    count++;
                }
            if(count == n){
                break;
            }
        }
    }

    public Hand getHand(){
        return h;
    }

    public Display getDisplay(){
        return d;
    }

    public void addCardtoHand(Card c){
        if(c.getType().equals(CardType.BASKET)){
            addCardtoDisplay(c);
        }
        else if(c.getType().equals(CardType.STICK)){
            addCardtoDisplay(c);

            
        }
        else{
            h.add(c);
         }

    }

    public void addCardtoDisplay(Card c){
        if(c.getType().equals(CardType.BASKET)){
            this.handlimit = getHandLimit() + 2;
        }
        this.d.add(c);
    }

    //Taking Card from the Forest
    public boolean takeCardFromTheForest(int n){
        int index = 8 - n;
        //In front of feet no sticks needed
        if(index == 6 || index == 7){
            if(Board.getForest().getElementAt(index).getType().equals(CardType.BASKET)){
                addCardtoDisplay(Board.getForest().getElementAt(index));
                Board.getForest().removeCardAt(index);
                return true;
            }
            if(getHand().size() + 1 > getHandLimit()){
                return false;
            }
            addCardtoHand(Board.getForest().getElementAt(index));
            Board.getForest().removeCardAt(index);
            return true;
        }
        else{
            if(sticks < n - 2){
                return false;
            }
            
            if(Board.getForest().getElementAt(index).getType().equals(CardType.BASKET)){
                System.out.println("Card number: " + n);
                System.out.println("Sticks number before: " + getStickNumber());
                System.out.println("Display size before removing sticks: " + getDisplay().size());
                removeSticks(n-2);
                System.out.println("Sticks number after: " + getStickNumber());
                System.out.println("Display size after removing sticks: " + getDisplay().size());
                for(int i = 0; i < getDisplay().size(); i++){
                    System.out.println("Display: " + getDisplay().getElementAt(i));
                
                }
                
                addCardtoDisplay(Board.getForest().getElementAt(index));   
                System.out.println("Display size after adding basket: " + getDisplay().size());   
                System.out.println(".....");    
                Board.getForest().removeCardAt(index);
                return true;
            }
            if(getHand().size() + 1 > getHandLimit()){
                return false;
            }
            removeSticks(n-2);
            addCardtoHand(Board.getForest().getElementAt(index));
            Board.getForest().removeCardAt(index);
            return true;

        }
    }

    //Take all from decay
    public boolean takeFromDecay(){
        ArrayList<Card> decP = Board.getDecayPile();
        int basket_count = 0;
        for(int i=0; i< decP.size(); i++){
            if(decP.get(i).getType().equals(CardType.BASKET)){
                this.handlimit = getHandLimit() + 2;
                basket_count++;
            }
        }

        if(getHandLimit()-getHand().size() < decP.size()-basket_count){
             return false;
        }
        else{
            for(int i=0; i< decP.size(); i++){
                if(decP.get(i).getType().equals(CardType.BASKET)){
                    this.handlimit = this.handlimit - 2;
                    addCardtoDisplay(decP.get(i));
                }
                else{
                    addCardtoHand(decP.get(i));
                }
            }
            Board.clearDecayPile();
            return true;
        }
    }
    
    //Cookikng mushrooms
    public boolean cookMushrooms(ArrayList<Card> cookingCards){
        boolean PanInHand = false;
        boolean PanInDisp = false;

        ArrayList<Card> allmush = new ArrayList<>();
        ArrayList<Card> daymush = new ArrayList<>();
        ArrayList<Card> nightmush = new ArrayList<>();
        ArrayList<Card> butters = new ArrayList<>();
        ArrayList<Card> ciders = new ArrayList<>();

        int numOfMush = 0;
        
       //checking for pan in passed arraylist
        for(int i = 0; i < cookingCards.size(); i++){
            if(cookingCards.get(i).getType().equals(CardType.PAN)){
                PanInHand = true;
                break;
            }
        }
        for(int i = 0; i < getDisplay().size(); i++){
            if(getDisplay().getElementAt(i).getType().equals(CardType.PAN)){
                PanInDisp = true;
                break;
            }
        }

        if(!PanInDisp && !PanInHand){
            return false;
        }

        for(int i = 0; i < cookingCards.size(); i++){

            if(cookingCards.get(i).getType().equals(CardType.DAYMUSHROOM)){
                daymush.add(cookingCards.get(i));
                allmush.add(cookingCards.get(i));
            }
            else if(cookingCards.get(i).getType().equals(CardType.NIGHTMUSHROOM)){
                nightmush.add(cookingCards.get(i));
                allmush.add(cookingCards.get(i));
            }
            else if(cookingCards.get(i).getType().equals(CardType.BUTTER)){
                butters.add(cookingCards.get(i));
            }
            else if(cookingCards.get(i).getType().equals(CardType.CIDER)){
                ciders.add(cookingCards.get(i));
            }
            else if(cookingCards.get(i).getType().equals(CardType.BASKET)){
                return false;
            }

        }

        numOfMush = daymush.size() + 2*nightmush.size();


        //Checking mushrooms amount
        if(numOfMush < 3){
            return false;
        }

        //Making sure all the names of mushrooms are the same
        for(int i = 0; i < allmush.size(); i++ ){
                for(int j = 0; j < allmush.size(); j++){
                    if(!(allmush.get(i).getName().equals(allmush.get(j).getName()))){
                        return false;
                    }
                }
        }

        //Checking how manay butters and ciders can fit
        int possible_but_cid = 4*butters.size() + 5*ciders.size();

        if(possible_but_cid > numOfMush){
            return false;
        }


        // Create 9 instances of all types of cards to get its flavour points
        BirchBolete birchd = new BirchBolete(CardType.DAYMUSHROOM);
        HoneyFungus honeyfungusd = new HoneyFungus(CardType.DAYMUSHROOM);
        TreeEar treeeard = new TreeEar(CardType.DAYMUSHROOM);
        LawyersWig lawyerswigd = new LawyersWig(CardType.DAYMUSHROOM);
        Shiitake shiitaked = new Shiitake(CardType.DAYMUSHROOM);
        HenOfWoods henofwoodsd = new HenOfWoods(CardType.DAYMUSHROOM);
        Porcini porcinid = new Porcini(CardType.DAYMUSHROOM);
        Chanterelle chanterelled = new Chanterelle(CardType.DAYMUSHROOM);
        Morel moreld = new Morel(CardType.DAYMUSHROOM);

        ArrayList<Mushroom> allMushCards = new ArrayList<>();

        allMushCards.add(birchd);
        allMushCards.add(honeyfungusd);
        allMushCards.add(treeeard);
        allMushCards.add(lawyerswigd);
        allMushCards.add(shiitaked);
        allMushCards.add(henofwoodsd);
        allMushCards.add(porcinid);
        allMushCards.add(chanterelled);
        allMushCards.add(moreld);

        int current_card_flavour = 0; 
        
        for (int i=0; i < allMushCards.size(); i++){

            if(allmush.get(0).getName().equals(allMushCards.get(i).getName())){
                // System.out.println(allMushCards.get(i).getName() + "pts " + allMushCards.get(i).getFlavourPoints());
                current_card_flavour = allMushCards.get(i).getFlavourPoints();
                break;
            }
        }

        // System.out.println("numberof mushs " + numOfMush);
        // System.out.println("the number of butter " + butters.size());
        // System.out.println("the number of cider " + ciders.size());

        // System.out.println("the score before " + this.score);
        
        this.score += (butters.size()*3) + (ciders.size()*5) + (numOfMush*current_card_flavour);
        // System.out.println("the score after " + this.score);

        //Updating Hand and Display
        int count_removed = 0;

        if(PanInHand){
            for(int i = 0; i < getHand().size(); i++){
                if(getHand().getElementAt(i).getType().equals(CardType.PAN)){
                    getHand().removeElement(i);
                    break;
                }
            }
        }
        else{
            for(int i = 0; i < getDisplay().size(); i++){
                if(getDisplay().getElementAt(i).getType().equals(CardType.PAN)){
                    getDisplay().removeElement(i);
                    break;
                }
            }
        }

        for(int i = 0; i < getHand().size(); i++){
            if(count_removed < numOfMush){
                for (int j = 0; j < allmush.size(); i++){
                    if(getHand().getElementAt(i).getName().equals(allmush.get(j).getName())){
                        if(getHand().getElementAt(i).getType().equals(CardType.NIGHTMUSHROOM)){
                            getHand().getElementAt(i);
                            count_removed += 2;
                        }
                        else{
                            getHand().getElementAt(i);
                            count_removed += 1;
                        }
                    }
                }
            }
            else{
                break;
            }
        }

        return true;

    }

    // Selling Mushrooms
    public boolean sellMushrooms(String name,int numToSell){

        String cardName = name.replaceAll(" ", "").replaceAll("\'","").toLowerCase();

        int num_mush_available = 0;


        int amountOfDay_available = 0;
        int amountOfNight_available = 0;

        int amountOfDay_needed = 0;
        int amountOfNight_needed = 0;

        for(int i = 0; i < getHand().size(); i++){
            if(getHand().getElementAt(i).getName().equals(cardName)){
                if(getHand().getElementAt(i).getType().equals(CardType.DAYMUSHROOM)){
                    amountOfDay_available = amountOfDay_available + 1;
                }
                else if(getHand().getElementAt(i).getType().equals(CardType.NIGHTMUSHROOM)){
                    amountOfNight_available = amountOfNight_available + 1;
                }
            }
        }

        num_mush_available = amountOfDay_available + 2*amountOfNight_available;

        if(num_mush_available < numToSell || numToSell < 2 || num_mush_available < 2){
            // System.out.println("mush name " + cardName);
            // System.out.println("Hand size: "+getHand().size());
            // for(int i = 0; i< getHand().size(); i++){
            //     System.out.println(getHand().getElementAt(i).getName());
            // }
            // System.out.println("cards in name by hand " + cards_inhand_byname);
            // System.out.println("Day avbl " + amountOfDay_available);
            // System.out.println("Night avble " + amountOfNight_available);
            // System.out.println("Mush avble " + num_mush_available);
            // System.out.println("Need to sell " + numToSell);
            return false;
        }

        
        
        //Instances to get stick number
        BirchBolete birchd = new BirchBolete(CardType.DAYMUSHROOM);
        HoneyFungus honeyfungusd = new HoneyFungus(CardType.DAYMUSHROOM);   
        TreeEar treeeard = new TreeEar(CardType.DAYMUSHROOM);
        LawyersWig lawyerswigd = new LawyersWig(CardType.DAYMUSHROOM);
        Shiitake shiitaked = new Shiitake(CardType.DAYMUSHROOM);
        HenOfWoods henofwoodsd = new HenOfWoods(CardType.DAYMUSHROOM);       
        Porcini porcinid = new Porcini(CardType.DAYMUSHROOM);
        Chanterelle chanterelled = new Chanterelle(CardType.DAYMUSHROOM);
        Morel moreld = new Morel(CardType.DAYMUSHROOM);        

        ArrayList<Mushroom> allMushCards = new ArrayList<>();

        allMushCards.add(birchd);
        allMushCards.add(honeyfungusd);
        allMushCards.add(treeeard);
        allMushCards.add(lawyerswigd);
        allMushCards.add(shiitaked);
        allMushCards.add(henofwoodsd);
        allMushCards.add(porcinid);
        allMushCards.add(chanterelled);
        allMushCards.add(moreld);
        
        int current_card_sticks = 0; 

        for (int i =0; i < allMushCards.size(); i++){
            if(allMushCards.get(i).getName().equals(cardName)){
                current_card_sticks = allMushCards.get(i).getSticksPerMushroom();
                break;
            }
        }

        //adding sticks
        addSticks(current_card_sticks*numToSell);

        //Removing cards from hand
        outer: for(int i = 0; i <= amountOfDay_available; i++){
            for(int j = 0; j <= amountOfNight_available; j++){
                if(2*j + i == numToSell){
                    amountOfDay_needed = i;
                    amountOfNight_needed = j;
                    break outer;
                }
            }
        }
        //System.out.println("Needed days" + amountOfDay_needed);
        //System.out.println("Needed nights" + amountOfNight_needed);
        
        //System.out.println(getHand().size()+" Before");

        while (amountOfDay_needed > 0){
            for(int i = 0; i < getHand().size(); i++){
                if(getHand().getElementAt(i).getName().equals(cardName) && getHand().getElementAt(i).getType().equals(CardType.DAYMUSHROOM)){
                    getHand().removeElement(i);
                    break;
                }
            }
            amountOfDay_needed--;
        }

        while (amountOfNight_needed > 0){
            for(int i = 0; i < getHand().size(); i++){
                if(getHand().getElementAt(i).getName().equals(cardName) && getHand().getElementAt(i).getType().equals(CardType.NIGHTMUSHROOM)){
                    getHand().removeElement(i);
                    break;
                }
            }
            amountOfNight_needed--;
        }

       // System.out.println(getHand().size()+" After");

        

        return true;


    }
    
    //Pan down
    public boolean putPanDown(){
        
        //Looking for pan in hand and adding to display if found one
        for (int i = 0; i < getHand().size(); i++){
            if(getHand().getElementAt(i).getType().equals(CardType.PAN)){
                addCardtoDisplay(getHand().getElementAt(i));
                getHand().removeElement(i);
                return true;
            }
        }
        //If reached to this point return false as pan was not found
        return false;

    }
}

