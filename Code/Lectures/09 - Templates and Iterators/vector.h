#pragma once
// Define and implement a simple the Vector class
template <typename T>
class Vector
{
private:
    T *data = nullptr;   // Pointer to allocated array
    size_t capacity =10; // Total capacity of the vector
    size_t size =0;     // Current number of elements

    void deepCopy(const Vector& other) //deep copy of the vector
    {
        capacity = other.capacity;
        size = other.size;
        if (data) delete[] data; // free the memory of the current objecy
        data = new T[capacity]{}; //init with 0
        for (size_t i = 0; i < size; ++i)
        {
            data[i] = other.data[i];
        }
    }

public:
    Vector(size_t initial_capacity = 10) : capacity(initial_capacity), size(0) 
    { 
        data = new T[capacity]{};
    }
    ~Vector() { if(data) delete[] data;}
    Vector(const Vector &other) { deepCopy(other);} // Copy constructor
    Vector &operator=(const Vector &other) // Copy assignment operator
    {
        if (this != &other) deepCopy(other);
        return *this;
    }
    void push_back(T value) // Add an element to the vector
    {
        if (size >= capacity) resize();
        data[size++] = value;
    } 
    void resize() // Resize the vector
    {
        capacity *= 2;
        T *new_data = new T[capacity]{};
        for (size_t i = 0; i < size; ++i) new_data[i] = data[i];
        delete[] data;
        data = new_data;
    }

    T &operator[](size_t index)// Access an element by index
    {
        while (index >= capacity) resize();
        size = index + 1;
        return data[index];
    }
 
    // Iterator class - nested class enclosing by Vector class
    // Nested class has access to the private member of the enclosing class
    // prevent collisions and allow each container to have its own iterator.
    class iterator
    {
    private:
        T *ptr;
        Vector<T> v;
    public:
        iterator(T *p, const Vector<T> &Vec) : ptr(p), v(Vec) {} // constructor
        T &operator*() const { return *ptr;} // Dereference operator
        T *operator->() const { return ptr;} // Member access operator
        iterator &operator++()  //Pre-inclement operator
        {
            ++ptr;
             return *this;
        } 
        iterator operator++(int)// Post-increment operator
        {
            iterator temp = *this;
            ++ptr;
            return temp;
        }
      bool operator==(const iterator &other) const { return ptr == other.ptr;} // Equality comparison
      bool operator!=(const iterator &other) const{ return ptr != other.ptr;}// Inequality comparison
    };

    class riterator
    {
    private:
        T *ptr;
        Vector<T> v;
    public:
        riterator(T *p, const Vector<T> &vec) : ptr(p), v(vec) {} // constructor
        T &operator*() const { return *ptr;} // Dereference operator
        T *operator->() const { return ptr;} // Member access operator
        riterator &operator++()  //Pre-inclement operator
        {
            --ptr;
             return *this;
        } 
        riterator operator++(int)// Post-increment operator
        {
            riterator temp = *this; 
            --ptr;
            return temp;
        }
        bool operator==(const riterator &other) const { return ptr == other.ptr;} // Equality comparison
        bool operator!=(const riterator &other) const{ return ptr != other.ptr;}// Inequality comparison
    };

    // Return an iterator to the beginning, forward iterator
    iterator begin() const
    {
        iterator it = iterator(data, *this); // pass the data pointer to the iterator.
        return it;
    }
    // Return an iterator to the end
    iterator end() const
    {
        iterator it = iterator(data + size, *this);
        return it;
    }
  
    // Return a reverse iterator, backward itertor
    riterator rbegin() const
    {
        riterator r_it = riterator(data+size-1, *this); // last element.
        return r_it;
    }
    // Return an reverse iterator to the end
    riterator rend() const
    {
        riterator r_it = riterator(data-1, *this);
        return r_it;
    }
};