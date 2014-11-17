#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/search.hh>
#include <algorithm>
#include <iterator>



//Knights Tour Problem
using namespace Gecode;
const int n = 5;
class Basic: public Space {
protected:
	IntVarArray V;
public:
	Basic(void) :
		V(*this, n * n, 0, n) {

		Matrix<IntVarArray> X(V, n, n);

		//constraints
		for (int col = 0; col < X.width(); col++) {
			for (int row = 0; row < X.height(); row++) {
				//std::cout << "cecking row,col: " <<row << " " << col << std::endl;
				std::vector<int> moves = validMoves(row, col, X);
				//dom(*this, X.operator ()(col, row), moves);
				for (int pcol = 0; pcol < X.width(); pcol++) {
					for (int prow = 0; prow < X.height(); prow++) {
						int possibleMove = encode(prow, pcol, X);

						int end = moves+sizeof(moves);
						bool *exits = std::find(std::begin(moves), std::end(moves), possibleMove)!= std::end(moves);
						// find the value 0:
						if (result == end) {
							rel(*this, X.operator ()(col, row), IRT_NQ, possibleMove);
						}
					}
				}
			}
		}

		//Search
		branch(*this, V, INT_VAR_SIZE_MIN(), INT_VAL_MIN());
	}

	Basic(bool share, Basic& s) :
		Space(share, s) {
		V.update(*this, share, s.V);
	}
	virtual Space* copy(bool share) {
		return new Basic(share, *this);
	}

	bool isValid(int row, int col, Matrix<IntVarArray> X) {
		bool ret = row >= 0 && row < X.height() && col >= 0 && col < X.width();
		//		std::cout << "is valid: " << row << " " << col << std::endl;
		//		std::cout << ret << std::endl;
		return ret;
	}

	int encode(int row, int col, Matrix<IntVarArray> X) {
		return row * X.height() + col;
	}

	std::vector<int> validMoves(int row, int col, Matrix<IntVarArray> X) {
		const int iCount = 2;
		const int jCount = 8;
		int tempMoves[iCount][jCount] = {
				//x coordinates
				{ row + 1, row - 1, row + 2, row
						- 2, row + 2, row - 2, row + 1, row - 1 },
						//y coordinates
						{ col - 2, col - 2, col - 1, col - 1, col + 1,
								col + 1, col + 2, col + 2 }
				//
		};
		std::vector<int> v;
		for (int i = 0; i < iCount; i++) {
			for (int j = 0; j< jCount; j++) {
				int r = tempMoves[0][j];
				int c = tempMoves[1][j];
				if (isValid(r, c, X)) {
					//std::cout << "row,col->r,c: " << row << "," << col << "=>" << r << "," << c << std::endl;
					int encoded = encode(r, c, X);
					std::cout << "r,c->encoded: " << r << "," << c << "=>" << encoded << std::endl;
					v.push_back(encoded);
				}
			}
		}
		int* a = &v[0];
		std::cout << "valid moves: ";
		for (int i = 0; i < sizeof(a); i++)
			std::cout << a[i] << " ";
		std::cout << std::endl;
		IntSet validMoves = IntSet(a, sizeof(a));
		std::cout << "validMoves: "<< validMoves <<std::endl;
		//return validMoves;
		return v;
	}

	void print(void) const {
		std::cout << "Printing solutions: " << std::endl;
		std::cout << V << std::endl;
		std::cout << V.size() << std::endl;
	}
};

int main(int argc, char* argv[]) {
	Basic* m = new Basic;
	DFS<Basic> e(m);
	delete m;
	/* one solution*/
	if (Basic* s = e.next()) {
		s->print();
		delete s;
	}

	/* all solutions */
	//while (Basic* s = e.next()) {
	//s->print(); delete s;
	//}
}
