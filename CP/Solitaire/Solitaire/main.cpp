#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/search.hh>
#include <algorithm>
#include <iterator>

//Knights Tour Problem
using namespace Gecode;
const int n = 10;
class Basic: public Space {
protected:
    IntVarArray V;
public:
    Basic(void) :
        V(*this, n * n, 0, n*n-1) {

        Matrix<IntVarArray> X(V, n, n);

        //constraints
        circuit(*this, V);
        for (int col = 0; col < X.width(); col++) {
            for (int row = 0; row < X.height(); row++) {
                //std::cout << "checking row,col: " <<row << " " << col << std::endl;
                std::vector<int> moves = validMoves(row, col, X);
                int a[moves.size()];

                //std::cout << "valid moves (vector): ";
                for (std::vector<int>::size_type i = 0; i != moves.size();
                     i++) {
                    //std::cout << moves[i] << " ";
                    a[i] = moves[i];
                }

                IntSet validMovesSet = IntSet(a, moves.size());
                std::cout << "valid moves (intset): " << validMovesSet
                          << std::endl;

                dom(*this, X(col, row), validMovesSet);
            }
        }

        std::cout << V << std::endl;
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
            { row + 1, row - 1, row + 2, row - 2, row + 2, row - 2, row + 1,
              row - 1 },
            //y coordinates
            { col - 2, col - 2, col - 1, col - 1, col + 1, col + 1, col + 2,
              col + 2 }
            //
        };
        std::vector<int> v;
        for (int j = 0; j < jCount; j++) {
            int r = tempMoves[0][j];
            int c = tempMoves[1][j];
            if (isValid(r, c, X)) {
                //std::cout << "row,col->r,c: " << row << "," << col << "=>" << r << "," << c << std::endl;
                int encoded = encode(r, c, X);
                //std::cout << "r,c->encoded: " << r << "," << c << "=>"
                //<< encoded << std::endl;
                v.push_back(encoded);
            }
        }
        return v;
    }

    void print(void) const {
        int a[V.size()];
        for (int i = 0, counter = 0; i < V.size(); i++) {
            int pos = V[i].val();
            a[pos] = counter++;
        }
        std::cout << "Printing solutions: " << std::endl;
        std::cout << V << std::endl;
        std::cout << "size: " << V.size() << std::endl;

        for (int i = 0; i < V.size(); i++) {
            if (i % n == 0) {
                std::cout<< std::endl;
            }
            std::cout << a[i] << " ";
        }
        std::cout<< std::endl;
    }
};

int main(int argc, char* argv[]) {
    Basic* m = new Basic;
    DFS<Basic> e(m);
    delete m;
    /* one solution*/
    if (Basic * s = e.next()) {
        s->print();
        delete s;
    }
}
