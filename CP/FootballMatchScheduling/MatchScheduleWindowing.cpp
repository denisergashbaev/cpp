#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/search.hh>

//Football match scheduling problem. Find optimal schedule.
//Additional constraint: 4 teams cannot play immediately with each other without a break inbetween
using namespace Gecode;
const int n = 10;
class Basic: public Space {
protected:
	IntVarArray V;
public:
	Basic(void):
			V(*this, n * (n - 1), 0, n - 1) {

		Matrix<IntVarArray> X(V, n - 1, n);

		//constraints

		//row should contain distinct values
		for (int i = 0; i < X.height(); i++) {
			distinct(*this, X.row(i));
		}
		//this constraint is not needed, it's implicit
//		for (int j = 0; j < X.width(); j++) {
//			distinct(*this, X.col(j));
//		}
		//row must not contain the team itself -> !i
		for (int j = 0; j < X.width(); j++) {
			for (int i = 0; i < X.height(); i++) {
				rel(*this, X(j, i) != i);
			}
		}

		//if team 0 plays with team 3, then team 3 must play with team 0
		for (int j = 0; j < X.width(); j++) {
			for (int i = 0; i < X.height(); i++) {
				element(*this, X.col(j), X(j, i), i);
			}
		}

		//additional windowing constraint
		const int numTeams = 4;
		IntSet teams = IntSet(0, numTeams-1);
		std::cout << teams << std::endl;
		for (int col = 0; col + numTeams < X.width(); col++) {
			for (int row = 0; row < numTeams - 1; row++) {
				//4-1 for one team is implicitly there
				count(*this, X.slice(col, col+numTeams, row, row+1), teams, IRT_LE, numTeams-1);
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
	void print(void) const {
		std::cout << "Printing solutions: " << std::endl;
		std::cout << V << std::endl;
		std::cout << V.size() << std::endl;
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < n - 1; j++) {
				int index = (i * (n - 1) + j);
				//std::cout << index << " " << std::endl;
				std::cout << V[index] << " ";
			}
			std::cout << std::endl;
		}
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
