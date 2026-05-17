#include <iostream>
#include <cstdlib>
#include <vector>
#include <cstdint>
#include <forward_list>
#include <string>
#include <chrono>
#include <random>
#include <algorithm>
#include <cmath>
#include <queue>
#include "node.hpp"
#include "container.hpp"

using namespace std;

// Global volatile sink: writing here creates an observable side effect so
// the optimizer cannot discard benchmarked memory accesses as dead code.
static volatile uint64_t g_benchmark_sink = 0;

enum class ContainerType{
    Vector,
    ForwardList
};


struct Metrics
{
    string name;
    float stDev;
    float median;
};

forward_list<Node> initializeListSequential(int count, int size);

forward_list<Node> initializeListArbitrary(int count, int size);

vector<Node> initializeVector(int count, int size);

template<typename Container>
uint64_t checksumContainer(const Container& c)
{
    uint64_t acc = 1469598103934665603ULL;
    for (const auto& node : c)
    {
        acc ^= static_cast<uint64_t>(node.data.size());
        acc *= 1099511628211ULL;
        if (!node.data.empty())
        {
            acc ^= static_cast<unsigned char>(node.data[0]);
            acc *= 1099511628211ULL;
        }
    }
    return acc;
}

template<typename Container>
Metrics singleRun(const string& name, int split, int size, ContainerWrapper<Container>& container)
{
    // modeChangeIndex: every N-th operation is an ins/del; 0 means never (100% read/write)
    const int modeChangeIndex = (split >= 100)
        ? 0
        : static_cast<int>(100.0f / (100.0f - static_cast<float>(split)));

    int  counter  = 1;
    bool isWrite  = false;
    bool isInsert = false;

    const chrono::seconds duration(10);

    // Welford online algorithm for stDev (ms), plus running median via two heaps.
    // https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance
    long long n        = 0;
    double    mean_ms  = 0.0;
    double    M2_ms    = 0.0;
    uint64_t  read_acc = 0;
    priority_queue<double> lower; // max-heap
    priority_queue<double, vector<double>, greater<double>> upper; // min-heap

    auto start = chrono::high_resolution_clock::now();
    while (chrono::high_resolution_clock::now() - start < duration) {

        auto op_start = chrono::high_resolution_clock::now();

        if (modeChangeIndex > 0 && counter % modeChangeIndex == 0) {
            if(isInsert){
                container.insert(Node(size));
                container.advance();
            } else {
                container.erase();
            }
            isInsert = !isInsert;
        } else {
            if (isWrite) container.write(Node(size));
            else {
                const auto& node = container.read();
                read_acc ^= static_cast<uint64_t>(node.data.size());
                if (!node.data.empty())
                    read_acc ^= static_cast<unsigned char>(node.data[0]);
            }
            container.advance();
            isWrite = !isWrite;
        }

        double ms = chrono::duration<double, milli>(
            chrono::high_resolution_clock::now() - op_start).count();

        if (lower.empty() || ms <= lower.top()) {
            lower.push(ms);
        } else {
            upper.push(ms);
        }

        if (lower.size() > upper.size() + 1) {
            upper.push(lower.top());
            lower.pop();
        } else if (upper.size() > lower.size()) {
            lower.push(upper.top());
            upper.pop();
        }

        ++n;
        double delta = ms - mean_ms;
        mean_ms     += delta / static_cast<double>(n);
        M2_ms       += delta * (ms - mean_ms); // uses updated mean (Welford)

        ++counter;
    }

    // Consume container state after timed section to prevent dead-code removal
    // while keeping the benchmark loop itself unchanged.
    uint64_t post = checksumContainer(container.c)
        ^ static_cast<uint64_t>(counter)
        ^ static_cast<uint64_t>(n)
        ^ read_acc;
    g_benchmark_sink ^= post;

    double variance = (n > 1) ? M2_ms / static_cast<double>(n - 1) : 0.0;
    double median = 0.0;
    if (!lower.empty() && lower.size() == upper.size()) {
        median = (lower.top() + upper.top()) * 0.5;
    } else if (!lower.empty()) {
        median = lower.top();
    }

    return Metrics{ name, static_cast<float>(sqrt(variance)), static_cast<float>(median) };
}

int main(int argc, char **argv)
{
    int split, size, elements = 0;

    if (argc == 1)
    {
        split = 95;
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

    split = clamp(split, 0, 100);

    cout << "split: " << split << "%, size: " << size << " bytes, elements: " << elements << endl;

    auto printMetrics = [](const Metrics& m) {
        cout << m.name
             << "  median=" << m.median << " ms"
             << "  stDev=" << m.stDev << " ms\n";
    };

    {
        ContainerWrapper<vector<Node>> w(initializeVector(elements, size));
        printMetrics(singleRun("vector", split, size, w));
    }
    {
        ContainerWrapper<forward_list<Node>> w(initializeListSequential(elements, size));
        printMetrics(singleRun("forward_list_sequential", split, size, w));
    }
    {
        ContainerWrapper<forward_list<Node>> w(initializeListArbitrary(elements, size));
        printMetrics(singleRun("forward_list_arbitrary", split, size, w));
    }

    cout << "sink=" << g_benchmark_sink << '\n';

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