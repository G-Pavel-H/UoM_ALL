package chess;

public class Knight extends Piece{


 	public Knight(PieceColour pc){
		if (pc.equals(PieceColour.WHITE)){
			this.colour=PieceColour.WHITE;
			setSymbol("♘");
		}
		else if (pc.equals(PieceColour.BLACK)){
			this.colour=PieceColour.BLACK;
			setSymbol("♞");
		}
	}


	@Override
	public boolean isLegitMove(int i0, int j0, int i1, int j1) {
		int difference_i = i1 - i0;
		int difference_j = j1 - j0;
		difference_i = Math.abs(difference_i);
		difference_j = Math.abs(difference_j);
		
		if((difference_i == 2 && difference_j == 1) || (difference_i == 1 && difference_j == 2)){
			if(Board.hasPiece(i1, j1)){
				if(Board.getPiece(i1, j1).getColour()!= Board.getPiece(i0, j0).getColour()){
					return true;
				}
				else{
					return false;
				}
			}
			else{
				return true;
			}
		}
		else{
			return false;
		}
	
	}
}
