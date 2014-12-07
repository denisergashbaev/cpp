#include <gecode/driver.hh>
#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <iostream>
#include <vector>
using namespace Gecode;

int numSuits;
int numRanks;
std::vector<int> cardIndexes;
int pileSize = 3;


int getSuit(int index){
    return index / numRanks;
}

int getRank(int index){
    return index % numRanks;
}

bool isValidNeighbor(int rank, int otherRank, int numRanks) {
    int minRank = std::min(rank, otherRank);
    int maxRank = std::max(rank, otherRank);
    int diff = maxRank - minRank;
    return diff == 1 || (minRank == 0 && maxRank == numRanks - 1);
}

void printSolitareInput(std::vector <int> cardIndexes){
    int stackCount = cardIndexes.size()/pileSize;
    for (int i=0; i<stackCount; i++) {
        for (int j=0; j < pileSize; j++) {
            //std::cout << "index: " << stackCount * i + j << std::endl;
            int ind = pileSize * i + j;
            int card = cardIndexes[ind];
            std::cout << std::setw(5) << getRank(card) << ":" << getSuit(card);
            std::cout << ",i:" << ind << "c:"<< card;
        }
        std::cout<<std::endl;
    }
}

void printSolitaireSolution(IntVarArray V, std::vector <int> cardIndexes) {
    //std::cout << V << std::endl;
    for (int i = 0; i < V.size(); i++) {
        for (int j = 0; j < V.size(); j++) {
            int value = V[j].val();
            if (i == value) {
                int card = cardIndexes[j];
                //std::cout << j << ":" << card << ">";
                std::cout << getRank(card) << ":" << getSuit(card) << ", ";
                break;
            }
        }
    }
    std::cout<<std::endl;
}

class Solitare : public Space {

protected:
    IntVarArray V;
public:
    Solitare() : V(*this, numSuits * numRanks - 1, 0, numSuits * numRanks - 2) {
        //V: index --> card, value -->position

        //Constraints:
        //1. the positions should be distinct
        distinct(*this, V);

        //2. in each pile, the bottom card can only have a higher position than the card that is on top of it:
        //that is, it may only be placed on the deck if the card before it is already on the deck and thus has uncovered it
        int stackCount = V.size()/pileSize;
        for(int i = 0; i < stackCount; i++) {
            //std::cout << "deck " << i << std::endl;
            for (int j = 0; j < pileSize - 1; j ++) {
                int index0 = pileSize * i + j;
                int index1 = index0 + 1;
                //int card0 = cardIndexes[index0];
                //int card1 = cardIndexes[index1];
                //std::cout << "constraining " << getRank(card0) << ":" << getSuit(card0) << " and " << getRank(card1) << ":" << getSuit(card1) << std::endl;
                rel(*this, V[index0], IRT_GR, V[index1]);
            }
        }

        //3. If two cards have a "rank jump" with a value of more than 1 unit, they can not be consecutive
        for (int i = 0; i < V.size(); i++) {
            int card0 = 0;
            int card1 = cardIndexes[i];
            if (!isValidNeighbor(getRank(card0), getRank(card1), numRanks)){
                //std::cout << "not vn: index0, index1 = " << index0 << " " << index1 << " rank(index0), rank(index1) =" <<getRank(index0) << " " << getRank(index1) << std::endl;
                rel(*this, V[i], IRT_GR, 0);
            }
        }

        for (int i = 0; i < V.size(); i++) {
            int card0 = cardIndexes[i];
            for (int j = i + 1; j < V.size(); j++) {
                int card1 = cardIndexes[j];
                if (!isValidNeighbor(getRank(card0), getRank(card1), numRanks)){
                    //std::cout << "not vn: index0, index1 = " << index0 << " " << index1 << " rank(index0), rank(index1) =" <<getRank(index0) << " " << getRank(index1) << std::endl;
                    //std::cout << "not vn: " << getRank(index0) << ":" << getSuit(index0) << " & " << getRank(index1) << ":" << getSuit(index1) << std::endl;
                    //std::cout << i << "&" << j << "->" << getRank(card0)<<":"<<getRank(card1) << std::endl;
                    rel(*this, abs(V[i] - V[j]) > 1);
                }
            }
        }

        // ====== IMPROVING THE MODEL ======


//one attempt..: adding additional constraints for some of the cards
//        for (int i = 0; i < V.size(); i++) {
//            int level = i % pileSize;
//            if (level == 0) {
//                rel(*this, V[i], IRT_GR, 1);
//            } else if (level == 1) {
//                rel(*this, V[i], IRT_GR, 0);
//                rel(*this, V[i], IRT_LE, numSuits * numRanks - 2 - 1);
//            } else if (level == 2) {
//                rel(*this, V[i], IRT_LE, numSuits * numRanks - 2 - 2);
//            }
//        }



//experimenting with dom constraints instead of rel
//                for (int i = 0; i < V.size(); i++) {
//                    int level = i % pileSize;
//                    if (level == 0) {
//                        dom(*this, V[i], IntSet(1, numSuits * numRanks - 2));
//                    } else if (level == 1) {
//                        dom(*this, V[i], IntSet(0, numSuits * numRanks - 2 - 1));
//                    } else if (level == 2) {
//                        dom(*this, V[i], IntSet(0, numSuits * numRanks - 2 - 2));
//                    }
//                }

//another attempt...: reversing the constraints on the pile
//        for(int i = 0; i < stackCount; i++) {
//            //std::cout << "deck " << i << std::endl;
//            for (int j = pileSize - 1; j > 1; j--) {
//                int index0 = pileSize * i + j;
//                int index1 = index0 - 1;
//                rel(*this, V[index0], IRT_LE, V[index1]);
//            }
//        }


//started with this branching strategy
        //branch(*this, V, INT_VAR_NONE(), INT_VAL_MIN());

//many other experiments with branching strategies...
        Rnd r(1U);
        //These two do not improve the performance of the 4_7_* instances
        //branch(*this, V, INT_VAR_SIZE_MIN(), INT_VAL_MIN());
        //branch(*this, V,  INT_VAR_MERIT_MIN(&mer), INT_VAL(&v));
        //branch(*this, V,  tiebreak(INT_VAR_DEGREE_MAX(), INT_VAR_MERIT_MIN(&mer)), INT_VAL_MIN());
        //branch(*this, V,  INT_VAR_DEGREE_MAX(), INT_VAL_MIN());

        //and random branching strategy, now the 4_7_* instances work too
        //branch(*this, V, tiebreak(INT_VAR_SIZE_MIN(), INT_VAR_RND(r)), INT_VAL_RND(r));


//This branching strategy seems most sensible:
        //prefer the cards which are on top of the pile INT_VAR_MERIT_MAX, resolve the tie breaks by preferring a variable with most constraints -- INT_VAR_DEGREE_MAX

        branch(*this, V, tiebreak(INT_VAR_MERIT_MAX(&mer), INT_VAR_DEGREE_MAX()), INT_VALUES_MIN());

    }

    //infer the 'merit' of a card based on where it is located on the pile
    static double mer(const Space& home, IntVar x, int i) {
      double val = i % pileSize; //is the size of the stack: 0 - behind others, 2 - on top
      return val;
    }

    static int v(const Space& home, IntVar x, int i) {
      int bestval = x.min();
      return bestval;
    }

    Solitare(bool share, Solitare& s) : Space(share, s) {
        V.update(*this, share, s.V);
    }
    virtual Space* copy(bool share) {
        return new Solitare(share,*this);
    }
    void print(void) const {
        //std::cout << "V: " << V << std::endl;
        //std::cout << "V.size=" << V.size() << std::endl;

        std::cout << std::endl << "Solution:\n " << std::endl;
        printSolitaireSolution(V, cardIndexes);
    }
};



int main(int argc, char** argv){
    if(argc !=2){
        std::cout<< "Please provide an absolute path to the input file"<<std::endl;
        exit(1);
    }

    std::ifstream fin;
    fin.open(argv[1]);
    int temp;
    fin >> numSuits >> numRanks;
    std::cout << "Number of suits: "<< numSuits <<std::endl;
    std::cout << "Number of ranks: "<< numRanks <<std::endl;

    for (int i = 0; i<numSuits*numRanks-1; i++ ){
        fin >> temp;
        //std::cout << temp << " "<< std::endl;
        cardIndexes.push_back(temp);
    }
    std::cout << std::endl << "Input: " << std::endl;
    printSolitareInput(cardIndexes);

    Solitare* s = new Solitare;
    DFS<Solitare> e(s);
    delete s;
    std::cout << "Printing solution (if available):\n" << std::endl;
    if(Solitare* t = e.next()){
        t->print();
        delete t;
    }
    return 0;
}
