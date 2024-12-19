#include "Calculator.h"
#include <gtest/gtest.h>

using ::testing::Test;
using ::testing::TestWithParam;
using ::testing::Values;
using ::testing::Combine;

class CalculatorTest : public Test{ // 参数化测试中需修改为 TestWithParam<>
protected:
    Calculator calc;
};

// 1.4.2：定义测试夹具 CalculatorParamTest
// 它继承自Google的一个模板类，中间的std::tuple<int, int, int>表示这个测试夹具的参数类型为3个整数
class CalculatorParamTest : public TestWithParam<std::tuple<int, int, int>> {
protected:
    Calculator calc;
};

// 1.4.3：定义测试夹具 CalculatorCombinedTest
class CalculatorCombinedTest : public TestWithParam<std::tuple<int, int, int>> {
protected:
    Calculator calc;
};

TEST_F(CalculatorTest, AddsTwoNumbers) {
    EXPECT_EQ(5, calc.add(2, 3));
}

// 1.4.1：使用 EXPECT_EQ 和 EXPECT_NEAR 完成 SubtractsTwoNumbers, MultipliesTwoNumbers, DividesTwoNumbers 测试用例

TEST_F(CalculatorTest, SubtractsTwoNumbers) {
    EXPECT_EQ(1, calc.subtract(3, 2));
}

TEST_F(CalculatorTest, MultipliesTwoNumbers) {
    EXPECT_EQ(6, calc.multiply(2, 3));
}

TEST_F(CalculatorTest, DividesTwoNumbers) {
//    因为浮点数的精度问题，所以使用 EXPECT_NEAR
    EXPECT_NEAR(2.0, calc.divide(6, 3), 1e-5);
}

// 1.4.1：使用 EXPECT_THROW 完成 DivisionByZeroThrows 测试用例
TEST_F(CalculatorTest, DivisionByZeroThrows) {
    EXPECT_THROW(calc.divide(1, 0), std::invalid_argument);
}

// 1.4.2：使用 TEST_P 和 INSTANTIATE_TEST_SUITE_P 定义一个参数化测试 CanAddNumbers

TEST_P(CalculatorParamTest, CanAddNumbers) {
    int a, b, expected;
    std::tie(a, b, expected) = GetParam();
    EXPECT_EQ(expected, calc.add(a, b));
}

INSTANTIATE_TEST_SUITE_P(AdditionTests, CalculatorParamTest, Values(
    std::make_tuple(1, 1, 2),
    std::make_tuple(2, 3, 5),
    std::make_tuple(10, 20, 30)
));

// 1.4.3：使用 TEST_P 和 INSTANTIATE_TEST_SUITE_P 定义一个组合参数化测试 AddCombination

TEST_P(CalculatorCombinedTest, AddCombination) {
    int a, b, c, expected;
    std::tie(a, b, c) = GetParam();
    EXPECT_EQ(a+b+c, calc.add(calc.add(a, b), c));
}

INSTANTIATE_TEST_SUITE_P(AdditionCombinationTests, CalculatorCombinedTest, Combine(
    Values(1, 2, 3),
    Values(4, 5, 6),
    Values(7, 8, 9)
));
