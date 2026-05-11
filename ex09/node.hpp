#pragma once
#include <vector>
#include <random>

class Node
{
public:
    Node(int bytes) : data(bytes) {
        // fil data with random chars
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(0, 255);
        for (auto &byte : data)
            byte = static_cast<char>(dis(gen));
    };
    std::vector<char> data;
};