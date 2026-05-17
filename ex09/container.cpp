#include "container.hpp"
#include "node.hpp"
#include <vector>
#include <forward_list>

// Explicit instantiations so the compiler validates both paths.
template class ContainerWrapper<std::vector<Node>>;
template class ContainerWrapper<std::forward_list<Node>>;

