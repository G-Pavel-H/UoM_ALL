package chess;

public class Queen extends Piece{
	

	public Queen(PieceColour pc){
		if (pc.equals(PieceColour.WHITE)){
			this.colour=PieceColour.WHITE;
			setSymbol("♕");
		}
		else if (pc.equals(PieceColour.BLACK)){
			this.colour=PieceColour.BLACK;
			setSymbol("♛");
		}
	}

	

	@Override
	public boolean isLegitMove(int i0, int j0, int i1, int j1) {
		int difference_i = i1 - i0;
		int difference_j = j1 - j0;

		if(Board.hasPiece(i1, j1)){
			if(Board.getPiece(i1, j1).getColour() == Board.getPiece(i0, j0).getColour()){
				return false;
			}
		}
		if(i1 > i0 && j1 > j0){
			if(difference_i == difference_j){
					difference_i--;
					difference_j--;
				while(difference_i > 0){
					int square_check_i = i0 + difference_i;
					int square_check_j = j0 + difference_j;
					if(Board.hasPiece(square_check_i, square_check_j)){
						return false;
					}
					difference_i--;
					difference_j--;
					}
					return true;
			}
			else{
				return false;
			}
		}
		else if(i1 > i0 && difference_j == 0){
				difference_i--;
				
				while(difference_i > 0){
					int square_check_i = i0 + difference_i;
					if(Board.hasPiece(square_check_i, j0)){
						return false;
					}
					difference_i--;
					}
					return true;
		}
		else if (i1 > i0 && j1 < j0){
			difference_j = Math.abs(difference_j);
			if(difference_i == difference_j){
				difference_i--;
				difference_j--;
				while(difference_i > 0){
					int square_check_i = i0 + difference_i;
					int square_check_j = j0 - difference_j;
					if(Board.hasPiece(square_check_i, square_check_j)){
						return false;
					}
					difference_i--;
					difference_j--;
					}
					return true;
			}
			else{
				return false;
			}
		}
		else if(difference_i == 0 && j1 < j0){
			difference_j = Math.abs(difference_j);
			difference_j--;
			while(difference_j > 0){
				int square_check_j = j0 - difference_j;
				if(Board.hasPiece(i0, square_check_j)){
					return false;
				}
				difference_j--;
				}
				return true;
		}
		else if(i1 < i0 && j1 < j0){
			difference_j = Math.abs(difference_j);
			difference_i = Math.abs(difference_i);
			if(difference_i == difference_j){
				difference_i--;
				difference_j--;
				while(difference_i > 0){
					int square_check_i = i0 - difference_i;
					int square_check_j = j0 - difference_j;
					if(Board.hasPiece(square_check_i, square_check_j)){
						return false;
					}
					difference_i--;
					difference_j--;
					}
					return true;
			}
			else{
				return false;
			}
		}
		else if(i1 < i0 && difference_j == 0){
			difference_i = Math.abs(difference_i);
			difference_i--;
			while(difference_i > 0){
				int square_check_i = i0 - difference_i;
				if(Board.hasPiece(square_check_i, j0)){
					return false;
				}
				difference_i--;
				}
				return true;
		}
		else if (i1 < i0 && j1 > j0){
			difference_i = Math.abs(difference_i);
			if(difference_i == difference_j){
				difference_i--;
				difference_j--;
				while(difference_i > 0){
					int square_check_i = i0 - difference_i;
					int square_check_j = j0 + difference_j;
					if(Board.hasPiece(square_check_i, square_check_j)){
						return false;
					}
					difference_i--;
					difference_j--;
					}
					return true;
			}
			else{
				return false;
			}
		}
		else if(difference_i == 0 && j1 > j0){
			difference_j--;
			while(difference_j > 0){
				int square_check_j = j0 + difference_j;
				if(Board.hasPiece(i0, square_check_j)){
					return false;
				}
				difference_j--;
				}
				return true;
		}
		else{
			return false;
		}
	}
}
