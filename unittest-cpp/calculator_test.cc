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
// 1.4.3：定义测试夹具 CalculatorCombinedTest

TEST_F(CalculatorTest, AddsTwoNumbers) {
    EXPECT_EQ(5, calc.add(2, 3));
}

// 1.4.1：使用 EXPECT_EQ 和 EXPECT_NEAR 完成 SubtractsTwoNumbers, MultipliesTwoNumbers, DividesTwoNumbers 测试用例

// 1.4.1：使用 EXPECT_THROW 完成 DivisionByZeroThrows 测试用例

// 1.4.2：使用 TEST_P 和 INSTANTIATE_TEST_SUITE_P 定义一个参数化测试 CanAddNumbers

// 1.4.3：使用 TEST_P 和 INSTANTIATE_TEST_SUITE_P 定义一个组合参数化测试 AddCombination
