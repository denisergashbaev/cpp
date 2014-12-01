#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/search.hh>
#include <algorithm>
#include <iterator>
#include <iomanip>

//Group Sports Scheduling Problem
using namespace Gecode;
const int groupCount = 4;
const int groupSize = 4;
const int weekCount = 5;
class GroupSportsScheduling: public Space {
protected:
    IntVarArray V;
public:
    GroupSportsScheduling(void) :
        V(*this,  groupCount * groupSize * weekCount, 0, groupCount * groupSize - 1) {

        //build a matrix: columns are the weeks and rows are the groups (with their players)
        Matrix<IntVarArray> X(V, weekCount, groupCount * groupSize);

        //enforce the 'distinct constraint' on each of the columns (that is, the players within one week may not be repeated -- play in different groups)
        for(int i = 0; i<X.width();i++) {
            distinct(*this, X.col(i));
        }

        //lexicographical order for the columns
        for (int col0=1; col0<X.width(); col0++) {
            rel(*this, X.col(col0-1), IRT_LE, X.col(col0));
        }

        //lexicographical order for the rows
        for (int row0=1; row0 < X.height(); row0++) {
            rel(*this, X.row(row0-1), IRT_LE, X.row(row0));
        }



        //make sure that if a player_1 has played agains player_2 in week_n, than player_1 may not play against player_2 in week_n+1
        //first col
        for (int col0=0; col0<X.width();col0++) {
            //next col
            for (int col1=col0+1; col1 < X.width();col1++) {
                //std::cout << ">>> col0, col1: " << col0 << "," << col1 << std::endl;
                int rowStep = 1; //because we take group windows of size 2
                for (int col0_row0=0, step0 = 0; col0_row0 +  rowStep < X.height(); col0_row0 += step0) {
                    if (col0_row0 % groupSize  == groupSize - 2) {
                        step0 = 2;
                    } else {
                        step0 = 1;
                    }
                    for (int col0_row1=col0_row0+1; col0_row1 %groupSize !=0;col0_row1++) {
                        //                    std::cout << std::endl;
                        //                    std::cout << ">>> col0, row0: " << col0 << ", " << row0 << std::endl;
                        for (int col1_row0=0, step2 = 0; col1_row0 +  rowStep < X.height(); col1_row0 += step2) {
                            if (col1_row0 % groupSize  == groupSize - 2) {
                                step2 = 2;
                            } else {
                                step2 = 1;
                            }
                            //                        std::cout << ">>>col1, row1: " << col1 << ", " << row1 << std::endl;
                            for (int col1_row1 = col1_row0 + 1; col1_row1 % groupSize != 0; col1_row1++) {
                                rel(*this,
                                    (X(col0, col0_row0) != X(col1, col1_row0) && X(col0, col0_row0) != X(col1, col1_row1))
                                    ||
                                    (X(col0, col0_row1) != X(col1, col1_row0) && X(col0, col0_row1) != X(col1, col1_row1))
                                    );
                            }
                        }

                    }

                }
            }
        }
        branch(*this, V, INT_VAR_SIZE_MIN(), INT_VAL_MIN());
    }

    GroupSportsScheduling(bool share, GroupSportsScheduling& s) :
        Space(share, s) {
        V.update(*this, share, s.V);
    }

    void print(void) const {
        //std::cout << "Vector form: " << V << std::endl;
        Matrix<IntVarArray> X(V, weekCount, groupCount * groupSize);
        std::cout << "Matrix form: " << std::endl;
        for (int row = 0; row < X.height(); row++) {
            if (row % groupCount == 0) {
                std::cout << std::endl;
            }
            for (int col = 0; col < X.width(); col++) {
                std::cout << std::setw(5) << X(col, row);
            }
            std::cout << std::endl;

        }
    }

    virtual Space* copy(bool share) {
        return new GroupSportsScheduling(share, *this);
    }
};



int main(int argc, char* argv[]) {
    GroupSportsScheduling* m = new GroupSportsScheduling;
    DFS<GroupSportsScheduling> e(m);
    delete m;
    /* one solution*/
    if (GroupSportsScheduling * s = e.next()) {
        s->print();
        delete s;
    }
}
