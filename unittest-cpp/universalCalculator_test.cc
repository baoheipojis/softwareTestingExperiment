// universalCalculator_test.cc

#include "UniversalCalculator.h"
#include <gtest/gtest.h>

using ::testing::Test;
using ::testing::TestWithParam;
using ::testing::Values;
using ::testing::Combine;

template <typename T>
class CalculatorTest : public ::testing::Test {
protected:
    Calculator<T> calc;
};


using MyTypes = ::testing::Types<int, float, double>;
TYPED_TEST_SUITE(CalculatorTest, MyTypes);

TYPED_TEST(CalculatorTest, AddTest) {
    Calculator<TypeParam> calc;
    TypeParam a = 1;
    TypeParam b = 2;
    EXPECT_EQ(a + b, calc.add(a, b));
}