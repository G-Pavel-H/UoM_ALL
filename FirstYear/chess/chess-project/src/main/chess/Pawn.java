package chess;

public class Pawn extends Piece{

	public Pawn(PieceColour pc){
		if (pc.equals(PieceColour.WHITE)){
			this.colour=PieceColour.WHITE;
			setSymbol("♙");
		}
		else if (pc.equals(PieceColour.BLACK)){
			this.colour=PieceColour.BLACK;
			setSymbol("♟");
		}
	}


	@Override
	public boolean isLegitMove(int i0, int j0, int i1, int j1) {
		int difference_i = i1 - i0;
		int difference_j = j1 - j0;

	
		if(Board.getPiece(i0, j0).getColour() == PieceColour.BLACK){
			if(difference_i == 1 && difference_j == 0){
				if(Board.hasPiece(i1, j1)){
					return false;
				}
				else{
					return true;
				}
			}
			else if(Board.hasPiece(i1, j1) && Board.getPiece(i1, j1).getColour() == PieceColour.WHITE){
				if((difference_i == 1 && difference_j == 1) || (difference_i == 1 && difference_j == -1)){
					return true;
				}
				else{
					return false;
				}
			}
			else if (difference_i == 2 && i0 == 1){
				if(difference_j == 0){
					if(Board.hasPiece(i1, j1)){
						return false;
					}
					else{
						return true;
					}
				}
				else{
					return false;
				}
			}
			else {
				return false;
			}
		}

		else{

			if(difference_i == -1 && difference_j == 0){
				if(Board.hasPiece(i1, j1)){
					return false;
				}
				else{
					return true;
				}
			}

			else if(Board.hasPiece(i1, j1) && Board.getPiece(i1, j1).getColour() == PieceColour.BLACK){
				if((difference_i == -1 && difference_j == 1) || (difference_i == -1 && difference_j == -1)){
					return true;
				}
				else{
					return false;
				}
			}

			else if (difference_i == -2 && i0 == 6){
				if(difference_j == 0){
					if(Board.hasPiece(i1, j1)){
						return false;
					}
					else{
						return true;
					}
				}
				else{
					return false;
				}
			}
			else {
				return false;
			}

		}
	}
}
