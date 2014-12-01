#include <gecode/driver.hh>
#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <iostream>
#include <vector>
using namespace Gecode;

int numSuits;
int numRanks;
std::vector<int> inputDeck;
int stackSize = 3;


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
    int stackCount = cardIndexes.size()/stackSize;
    for (int i=0; i<stackCount; i++) {
        for (int j=0; j < stackSize; j++) {
            //std::cout << "index: " << stackCount * i + j << std::endl;
            int card = cardIndexes[stackSize * i + j];
            std::cout << std::setw(5) << getRank(card) << ":" << getSuit(card);
        }
        std::cout<<std::endl;
    }
}

void printSolitaireSolution(IntVarArray V, std::vector <int> cardIndexes) {
    for (int i = 0; i < V.size(); i++) {
        for (int j = 0; j < V.size(); j++) {
            int value = V[j].val();
            if (i == value) {
                std::cout << std::setw(5) << getRank(cardIndexes[j]) << ":" << getSuit(cardIndexes[j]);
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
        //std::cout << V << std::endl;

        //Constraints:
        //1. the positions should be distinct
        distinct(*this, V);

        //2. in each deck, the bottom card can only have a higher position than the card that is on top of it:
        //that is, it may only be placed on the deck if the card before it is already on the deck and thus has uncovered it
        int stackCount = V.size()/stackSize;
        for(int i = 0; i < stackCount; i++) {
            //std::cout << "deck " << i << std::endl;
            for (int j = 0; j < stackSize - 1; j++) {
                int index0 = stackSize * i + j;
                int index1 = index0 + 1;
                int card0 = inputDeck[index0];
                int card1 = inputDeck[index1];
                //std::cout << "constraining " << getRank(card0) << ":" << getSuit(card0) << " and " << getRank(card1) << ":" << getSuit(card1) << std::endl;
                rel(*this, V[index0] > V[index1]);
            }
        }

        //3. If two cards have a "rank jump" with a value of more than 1 unit, they can not be consequtive
        for (int i = 0; i < V.size(); i++) {
            if (i == 0) {
                int index0 = 0;
                int index1 = inputDeck[i];
                if (!isValidNeighbor(getRank(index0), getRank(index1), numRanks)){
                    rel(*this, abs(0 - V[index1]) > 1);
                }
            }
            for (int j = i + 1; j < V.size(); j++) {
                int index0 = inputDeck[i];
                int index1 = inputDeck[j];
                if (!isValidNeighbor(getRank(index0), getRank(index1), numRanks)){
                    rel(*this, abs(V[i] - V[j]) > 1);
                }
            }
        }
        //Search
        branch(*this, V, INT_VAR_NONE(), INT_VAL_MIN());
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

        std::cout << std::endl << "Solution: " << std::endl;
        printSolitaireSolution(V, inputDeck);
    }
};



int main(int argc, char** argv){
    if(argc !=2){
        std::cout<< "The only parameter should be the file name: "<<std::endl;
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
        inputDeck.push_back(temp);
    }
    std::cout << std::endl << "Input: " << std::endl;
    printSolitareInput(inputDeck);

    Solitare* s = new Solitare;
    DFS<Solitare> e(s);
    delete s;
    std::cout << "Printing solution (if available): " << std::endl;
    if(Solitare* t = e.next()){
        t->print();
        delete t;
    }
    return 0;
}
