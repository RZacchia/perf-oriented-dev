#include <iostream>
#include <cstdlib>
#include <vector>
#include <cstdint>
#include <forward_list>
#include <string>
#include <chrono>
#include <random>
#include <algorithm>
#include "node.hpp"

using namespace std;

struct Metrics
{
    string name;
    float stDev;
    float mean;
};

forward_list<Node> initializeListSequential(int count, int size);

forward_list<Node> initializeListArbitrary(int count, int size);

vector<Node> initializeVector(int count, int size);

vector<chrono::milliseconds> singleRun(int split, int size, int elements, container<Metrics> &metrics)
{
    auto arr = initializeVector(elements, size);
    auto listSeq = initializeListSequential(elements, size);
    auto listArb = initializeListArbitrary(elements, size);
}

int main(int argc, char **argv)
{
    int split, size, elements = 0;

    if (argc == 1)
    {
        split = 90;
        size = 8;
        elements = 100;
        cout << "using default values " << endl;
    }
    else if (argc != 4)
    {
        cerr << "Usage: " << argv[0] << " <split> <size> <elements>" << endl;
        return EXIT_FAILURE;
    }
    else
    {
        split = stoi(argv[1]);
        size = stoi(argv[2]);
        elements = stoi(argv[3]);
    }
    cout << "split: " << split << "%, size: " << size << " bytes, elements: " << elements << endl;

    auto start = chrono::high_resolution_clock::now();
    
    auto arr = initializeVector(elements, size);
    auto listSeq = initializeListSequential(elements, size);
    auto listArb = initializeListArbitrary(elements, size);
    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start).count();
    cout << "Vector initialization took " << duration << " ms" << endl;
    return EXIT_SUCCESS;
}


forward_list<Node> initializeListSequential(int count, int size)
{
    forward_list<Node> list = {};
    for (int i = 0; i < count; ++i)
    {
        list.push_front(Node(size));
    }
    return list;
}

forward_list<Node> initializeListArbitrary(int count, int size)
{
    forward_list<Node> list = initializeListSequential(count, size);
     using Iter = typename forward_list<Node>::iterator;
    vector<Iter> nodes;

    // 1. Collect iterators to every node in the list
    for (auto it = list.begin(); it != list.end(); ++it)
        nodes.push_back(it);

    // 2. Randomly shuffle the iterator order
    random_device rd;
    mt19937 gen(rd());
    shuffle(nodes.begin(), nodes.end(), gen);

    // 3. Build a new list in shuffled order
    forward_list<Node> shuffled;
    auto before = shuffled.before_begin();

    for (auto it : nodes)
        before = shuffled.insert_after(before, std::move(*it));

    // 4. Replace the original list
    list.swap(shuffled);
    return list;
}

vector<Node> initializeVector(int count, int size)
{
    return vector<Node>(count, Node(size));
}