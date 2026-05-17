#pragma once
#include <vector>
#include <forward_list>
#include <iterator>
#include <type_traits>
#include <functional>
#include <cstddef>

// --------------------------------------------------------------------------
// Trait: detect std::forward_list at compile time
// --------------------------------------------------------------------------
template<typename Container>
struct is_forward_list : std::false_type {};

template<typename T, typename A>
struct is_forward_list<std::forward_list<T, A>> : std::true_type {};

// --------------------------------------------------------------------------
// ContainerWrapper<Container>
//
// Wraps std::vector or std::forward_list and exposes a unified interface for:
//   read()     – return const-ref to the element at the current cursor
//   write()    – overwrite the element at the current cursor
//   insert()   – insert a new element at the current cursor position
//   erase()    – remove the element at the current cursor, advance cursor
//   advance()  – move cursor to the next element (wraps around at the end)
//
// The cursor always points to a valid element as long as the container is
// non-empty (size >= 1).
// --------------------------------------------------------------------------
template<typename Container>
class ContainerWrapper {
public:
    static constexpr bool flist = is_forward_list<Container>::value;

    using value_type = typename Container::value_type;
    using iterator   = typename Container::iterator;

    Container c;
    size_t    sz  = 0;

private:
    iterator  cur;
    size_t    idx = 0;
    // prev is only meaningful for forward_list:
    //   it always points to the node *before* cur so that
    //   insert_after(prev) / erase_after(prev) operate at cur.
    iterator  prev;

public:
    // ------------------------------------------------------------------
    // Constructor – pre-initialise with n elements produced by factory()
    // ------------------------------------------------------------------
    explicit ContainerWrapper(size_t n, std::function<value_type()> factory) {
        if constexpr (flist) {
            // Build in sequential (traversal) order by appending at the tail
            auto tail = c.before_begin();
            for (size_t i = 0; i < n; ++i)
                tail = c.insert_after(tail, factory());
            prev = c.before_begin();
            cur  = c.begin();
        } else {
            c.reserve(n + 2); // +2 headroom for benchmark insertions
            for (size_t i = 0; i < n; ++i)
                c.push_back(factory());
            idx = 0;
        }
        sz = n;
    }

    // ------------------------------------------------------------------
    // Move-from-container constructor – wrap an already-initialised container.
    // Useful when the caller controls memory layout (e.g. arbitrary alloc order).
    // ------------------------------------------------------------------
    explicit ContainerWrapper(Container&& existing) : c(std::move(existing)) {
        if constexpr (flist) {
            sz   = static_cast<size_t>(std::distance(c.begin(), c.end()));
            prev = c.before_begin();
            cur  = c.begin();
        } else {
            sz  = c.size();
            idx = 0;
        }
    }

    // ------------------------------------------------------------------
    // read – return const ref to the current element (no cursor movement)
    // ------------------------------------------------------------------
    const value_type& read() const {
        if constexpr (flist) {
            return *cur;
        } else {
            return c[idx];
        }
    }

    // ------------------------------------------------------------------
    // write – overwrite the current element (no cursor movement)
    // ------------------------------------------------------------------
    void write(value_type val) {
        if constexpr (flist) {
            *cur = std::move(val);
        } else {
            c[idx] = std::move(val);
        }
    }

    // ------------------------------------------------------------------
    // insert – insert val so that it becomes the new current element.
    //
    //   vector       : inserts before cur; cur points to the new element.
    //   forward_list : inserts after prev; cur points to the new element.
    //
    // Call advance() afterwards to continue past the inserted element.
    // ------------------------------------------------------------------
    void insert(value_type val) {
        if constexpr (flist) {
            cur = c.insert_after(prev, std::move(val));
        } else {
            c.insert(c.begin() + static_cast<typename Container::difference_type>(idx), std::move(val));
        }
        ++sz;
    }

    // ------------------------------------------------------------------
    // erase – remove the current element and move the cursor to the next
    //         element (wraps to begin() if the removed element was last).
    // ------------------------------------------------------------------
    void erase() {
        if constexpr (flist) {
            cur = c.erase_after(prev);
            if (cur == c.end()) {
                prev = c.before_begin();
                cur  = c.begin();
            }
        } else {
            c.erase(c.begin() + static_cast<typename Container::difference_type>(idx));
            if (idx >= sz - 1)
                idx = 0;
        }
        --sz;
    }

    // ------------------------------------------------------------------
    // advance – move cursor to the next element; wraps to begin() at end.
    // ------------------------------------------------------------------
    void advance() {
        if constexpr (flist) {
            prev = cur;
            ++cur;
            if (cur == c.end()) {
                prev = c.before_begin();
                cur  = c.begin();
            }
        } else {
            idx = (idx + 1) % sz;
        }
    }

    size_t size()  const { return sz; }
    bool   empty() const { return sz == 0; }
};
