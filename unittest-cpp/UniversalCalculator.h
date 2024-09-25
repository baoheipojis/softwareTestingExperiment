#include <stdexcept>
#ifndef CALCULATOR_H
#define CALCULATOR_H

template <typename T>
class Calculator {
public:
    // 加法
    T add(T a, T b) {
        return a + b;
    }

    // 减法
    T subtract(T a, T b) {
        return a - b;
    }

    // 乘法
    T multiply(T a, T b) {
        return a * b;
    }

    // 除法
    T divide(T a, T b) {
        if (b != 0) {
            return a / b;
        } else {
            throw std::invalid_argument("Division by zero is not allowed");
        }
    }
};

#endif // CALCULATOR_H
