package chess;

public class Bishop extends Piece{

	public Bishop(PieceColour pc){
		if (pc.equals(PieceColour.WHITE)){
			colour=PieceColour.WHITE;
			setSymbol("♗");
		}
		else if (pc.equals(PieceColour.BLACK)){
			colour=PieceColour.BLACK;
			setSymbol("♝");
		}
	}

	

	@Override
	public boolean isLegitMove(int i0, int j0, int i1, int j1) {
	
		if(Board.hasPiece(i1, j1)){
			if(Board.getPiece(i1, j1).getColour() == Board.getPiece(i0, j0).getColour()){
				return false;
			}
		}

		if(i0 == i1 || j0 == j1){
			return false;
		}
		
		if(Math.abs(i1 - i0) != Math.abs(j1 - j0)){
			return false;
		}
		
		int rowOffset, colOffset;
		
		if(i0 < i1){
			rowOffset = 1;
		}else{
			rowOffset = -1;
		}
		
		if(j0 < j1){
			colOffset = 1;
		}else{
			colOffset = -1;
		}
		
		int y = j0 + colOffset;
		for(int x = i0 + rowOffset; x != i1; x += rowOffset){
			
			if(Board.hasPiece(x, y)){
				return false;
			}
			
			y += colOffset;
		}
		
		return true;
		
		
	}
}
