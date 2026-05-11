#include <iostream>
#include <cstdlib>
#include <vector>
#include <cstdint>
#include <forward_list>
#include <string>

using namespace std;
// std dev and/or time as end parameter
// insert/deletion and read/write as percentage of access

class Node
{
public:
    Node(int bytes) : data(bytes) {};
    vector<char> data;
};

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
    forward_list<Node> list = {};
    for (int i = 0; i < count; ++i)
    {
        list.push_front(Node(size));
    }
    return list;
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
        cerr << "meh" << endl;
    }

    std::forward_list<Node> b = {};
    std::vector<Node> a = {};

    // Insert nodes into the list
    b.push_front(Node(1));
    b.push_front(Node(2));
    b.push_front(Node(3));

    // Insert a node at an arbitrary position (e.g., after the 2nd element)
    int position = 1; // 0-based index of the element to insert after
    auto it = b.before_begin();
    for (int i = 0; i <= position; ++i)
    {
        ++it;
    }
    b.insert_after(it, Node(42));
    return EXIT_SUCCESS;
}