# 软件测试实验指导书

## 1 C++ 单元测试
### 1.1 实验目的

利用 C++ 单元测试框架 googletest 的特性，提高单元测试编写和执行效率。

### 1.2 环境配置

本实验的所有操作均可以在 vim，或记事本内完成。当然，由于现代代码编辑器提供了代码补全，调试支持，插件等一系列强大功能，我们在此推荐使用 [VSCode](https://code.visualstudio.com/) 以支持你在本实验的代码编写。为此，推荐在 VSCode 主侧栏的扩展商店中安装如下插件：

- C/C++ Extension Pack
- Extension Pack for Java
- Python Extension Pack

然后，为了正确编译并使用 gtest 测试 C++ 代码，你将需要：
- 支持 C++14 及以上的 C++ 编译器
- 构建工具 CMake 和 Make

具体过程可参考 [GoogleTest官方文档](https://google.github.io/googletest/quickstart-cmake.html)。以下是各平台的推荐配置。

对于 **Windows** 平台：
- 推荐编译器为微软开发的 MSVC，通过下载 [Visual Studio 生成工具](https://aka.ms/vs/17/release/vs_BuildTools.exe)，并在其中勾选使用C++的桌面开发，安装。
- 构建工具可在 [CMake](https://cmake.org/download/) 和 [Make](https://gnuwin32.sourceforge.net/packages/make.htm) 官网安装。
  更推荐的方法是使用包管理器（比如[WinGet](https://github.com/microsoft/winget-cli), [Scoop](https://scoop.sh/) 和 [Chocolatey](https://chocolatey.org/install) ）一键安装。以 Scoop 为例，在 Powershell 中安装 Scoop：
    ````` powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
    `````
    然后通过Scoop安装所需构建工具：
    ````` powershell
    scoop install cmake make
    `````

对于 **Linux** 平台，编译器使用 gcc/clang 均可。通过包管理器安装。以 Debian/Ubuntu 为例：
````` shell
sudo apt install gcc g++ cmake make
`````

对于 **Mac** 平台，我们同样推荐使用包管理器 [Homebrew](https://brew.sh/) 配置环境。在 Mac 终端内输入
````` shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
`````
以安装 Homebrew。随后安装所需软件：
````` shell
brew install gcc g++ cmake make
`````

为验证构建工具已正确安装，在终端输入
````` shell
cmake --version
make --version
`````
若正确显示版本信息，表示工具已经安装并准备好使用。

此时即可在项目中配置 gtest。新建一个 ``my_project`` 文件夹并进入:
````` shell
mkdir my_project && cd my_project
`````
在其中新建一个 ``hello_test.cc``，内容为：
`````C++
#include <gtest/gtest.h>

TEST(HelloTest, BasicAssertions) {
  // Expect two strings not to be equal.
  EXPECT_STRNE("hello", "world");
  // Expect equality.
  EXPECT_EQ(7 * 6, 42);
}
`````

另新建一个 ``CMakeLists.txt`` ，使用 [FetchContent](https://cmake.org/cmake/help/latest/module/FetchContent.html) 声明对 GoogleTest 的依赖，并声明要构建的 C++ 测试二进制文件:
````` shell
cmake_minimum_required(VERSION 3.14)
project(unittest-cpp)

# GoogleTest requires at least C++14
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/ff233bdd4cac0a0bf6e5cd45bda3406814cb2796.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

enable_testing()

# Define test executable name and source file
set(TEST_EXECUTABLE_NAME hello_test)
set(TEST_SOURCE_FILE hello_test.cc)

add_executable(${TEST_EXECUTABLE_NAME} ${TEST_SOURCE_FILE})
target_link_libraries(${TEST_EXECUTABLE_NAME} GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(${TEST_EXECUTABLE_NAME})
`````

构建并运行测试：
````` bash
my_project$ cmake -S . -B build
-- The C compiler identification is GNU 10.2.1
-- The CXX compiler identification is GNU 10.2.1
...
-- Build files have been written to: .../my_project/build

my_project$ cmake --build build
Scanning dependencies of target gtest
...
[100%] Built target gmock_main

my_project$ cd build && ctest
Test project .../my_project/build
    Start 1: HelloTest.BasicAssertions
1/1 Test #1: HelloTest.BasicAssertions ........   Passed    0.00 sec

100% tests passed, 0 tests failed out of 1

Total Test time (real) =   0.01 sec
`````

### 1.3 GoogleTest语法介绍

在GoogleTest中，定义了多种宏来编写测试。其中常用的包括：
#### TEST
`````C++
TEST(TestSuiteName, TestName) {
  ... statements ...
}
`````
在测试套件``TestSuiteName``中定义一个名为``TestName``的测试。
#### TEST_F 
`````C++
TEST_F(TestFixtureName, TestName) {
  ... statements ...
}
`````
定义一个名为``TestName``的测试，使用测试夹具类 ``TestFixtureName``。在测试的时候，我们经常遇到一个对象需要初始化，测试完可能还需要清理的情况，使用测试夹具可以批量完成此类操作。

使用 TEST_F 能够复用夹具中定义的代码，使得测试更加模块化，并减少了重复代码。
#### TEST_P
`````C++
TEST_P(TestFixtureName, TestName) {
  ... statements ...
}
`````
定义一个名为``TestName``的值参数化测试，使用测试夹具类 ``TestFixtureName``。测试套件名称为 ``TestFixtureName``。 

使用 TEST_P 能够实现值参数化测试，即在一个测试下对不同参数值进行测试。这可以有效减少重复代码，提高测试覆盖率。

#### INSTANTIATE_TEST_SUITE_P
`````C++
INSTANTIATE_TEST_SUITE_P(InstantiationName,TestSuiteName,param_generator)
INSTANTIATE_TEST_SUITE_P(InstantiationName,TestSuiteName,param_generator,name_generator)
`````
实例化TEST_P定义的值参数化测试套件 ``TestSuiteName``。

#### TYPED_TEST_SUITE
`````C++
TYPED_TEST_SUITE(TestFixtureName,Types) TYPED_TEST_SUITE(TestFixtureName,Types,NameGenerator)
`````
定义一个基于测试夹具 ``TestFixtureName`` 的类型参数化测试套件。使用参数 ``Types`` 表示要运行测试的数据类型列表。

#### TYPED_TEST
`````C++
TYPED_TEST(TestSuiteName, TestName) {
  ... statements ...
}
`````
在类型参数化测试套件中定义一个具体的测试用例。在测试体内部，可以使用特殊名称 ``TypeParam`` 来引用类型参数，使用 ``TestFixture`` 来引用测试夹具类。

更多测试用宏的资料可参考[官方文档](https://google.github.io/googletest/reference/testing.html)。 

断言(Assertion)是单元测试中不可缺少的重要部分。在GoogleTest中，定义了多种断言宏：

- 基本断言：如 EXPECT_TRUE、EXPECT_FALSE、ASSERT_TRUE 和 ASSERT_FALSE，用于检查测试中的条件。
- 二元比较断言：比较两个值，包括 EXPECT_EQ、EXPECT_NE 等及其 ASSERT_ 对应形式。
- 字符串比较断言：专门用于比较 C 字符串，包括 EXPECT_STREQ 和 EXPECT_STRCASEEQ 等。
- 浮点数比较断言：如 EXPECT_FLOAT_EQ 和 EXPECT_NEAR，处理浮点数的精度问题。
- 异常断言：检查预期的异常，如 EXPECT_THROW 和 EXPECT_NO_THROW。
- 谓词断言：允许复杂逻辑检查，包括 EXPECT_PRED1、EXPECT_PRED2 等。

每一类断言又分为两种：
- **EXPECT断言**：在条件不满足时记录断言失败，但不终止当前测试用例。
- **ASSERT断言**：在条件不满足时终止当前测试用例，不再执行后续的代码。

更多断言宏相关资料可参考[官方文档](https://google.github.io/googletest/reference/assertions.html)。 

## 1.4 实验内容

本部分将通过数个例子，利用 googletest 功能进行单元测试实践。

### 1.4.1 创建第一个单元测试

在本节中，我们对一个计算器类进行测试，它提供了四个基本的数学运算方法：加法、减法、乘法和除法。实验预先提供了计算器类的实现 ``Calculator.h``，并在 ``calculator_test.cc`` 设置了测试夹具,提供了测试用例示例:
`````C++
TEST_F(CalculatorTest, AddsTwoNumbers) {
    EXPECT_EQ(5, calc.add(2, 3));
}
`````

本部分的任务如下：
1. 在指定位置仿照示例完成 SubtractsTwoNumbers, MultipliesTwoNumbers, DividesTwoNumbers 的测试用例。（提示：由于 DividesTwoNumbers 涉及浮点运算，直接比较浮点数可能会因为极小的精度误差而导致测试失败，可考虑使用 [EXPECT_NEAR(val1,val2,abs_error)](https://google.github.io/googletest/reference/assertions.html#floating-point) 而不是 EXPECT_EQ 断言）。
2. 请在指定位置构建DivisionByZeroThrows测试用例，验证除以0是能否触发异常。在其中使用 EXPECT_THROW(statement,exception_type) 断言。由 ``Calculator.h`` 可知，除以0触发的异常类型为 ``std::invalid_argument``。

完成后，修改 ``CMakeLists.txt``，把 ``TEST_SOURCE_FILE`` 变量修改成 ``calculator_test.cc``，然后在 ``./unittest-cpp`` 目录下编译并运行测试：
`````bash
cmake --build build
cd build && ctest
`````
测试结果显示
`````bash
Test project /your/path
      Start  1: CalculatorTest.AddsTwoNumbers
 x/xx Test  #1: CalculatorTest.AddsTwoNumbers ............   Passed    0.05 sec
      Start  2: CalculatorTest.SubtractsTwoNumbers
 ...

100% tests passed, x tests failed out of x

Total Test time (real) =   0.xx sec
`````

完成用例编写之余请思考：上述内容使用的均为 EXCEPT 断言。那么，在什么场景下适合使用 ASSERT 断言？

### 1.4.2 值参数化测试

如 1.3 中所述，值参数化测试可以组织一组不同的测试数据，对其调用相同的测试方法进行测试。GoogleTest的官方文档详细阐述了如何使用 [值参数化测试](https://google.github.io/googletest/advanced.html#value-parameterized-tests)：
1. 定义测试夹具类。以 FooTest 为例：
    `````C++
    class FooTest :
        public testing::TestWithParam<absl::string_view> {
            // 部署测试夹具
    };
    `````
2. 使用 TEST_P 定义所需的测试用例。
   `````C++
   TEST_P(FooTest, DoesBlah) {
      // 使用 GetParam() 方法获取参数
      EXPECT_TRUE(foo.Blah(GetParam()));
      ...
    }

    TEST_P(FooTest, HasBlahBlah) {
      ...
    }
   `````
3. 使用 INSTANTIATE_TEST_SUITE_P 使用所需参数集来实例化测试套件。
   `````C++
   INSTANTIATE_TEST_SUITE_P(Default,
                              FooTest,
                              testing::Values("meeny", "miny", "moe"));
   `````

本部分的任务是，在指定位置完成 ``CanAddNumbers`` 用例的编写：
- 定义一个新的测试夹具 ``CalculatorParamTest`` ，使用 ``TestWithParam<int>`` 作为基类代替 ``Test``。
- 使用 TEST_P 定义 ``CanAddNumbers`` 用例，使用 ``GetParam()`` 调用一个参数，再加上一个常数，以测试 ``add`` 方法，并使用 EXPECT_EQ 作为断言。
- 使用 INSTANTIATE_TEST_SUITE_P(InstantiationName,TestSuiteName,param_generator) 实例化该测试套件，使用五个参数[1,2,3,4,5]。

在 ``./unittest-cpp`` 目录下编译并运行测试，观察结果。

### 1.4.3 在值参数化测试中考虑组合

在复杂软件系统中，经常会出现这样的现象:软件被安装在一个新的位置或者被不同用户使用后，出现了一组原本不存在的新错误。这是由于，这些变化导致了一组不同的输入，其中一些输入组合触发了故障。gtest 在参数化测试中引入了 ``Combine()`` 方法，将 n 个输入通过笛卡尔积的方式组合成 n 元组进行测试。

本部分的任务是，在指定位置完成 ``AddCombination`` 用例的编写。可参考官方文档 [参数化测试](https://google.github.io/googletest/advanced.html#value-parameterized-tests)：

- 定义一个新的测试夹具 ``CalculatorCombinedTest`` ，使用 ``TestWithParam`` 作为基类。注意此处的参数应当是两个 int 组成的 tuple。
- 使用 TEST_P 定义 ``AddCombination`` 用例，使用 ``GetParam()`` 调用两个参数，以测试 ``add`` 方法，并使用 EXPECT_EQ 作为断言。
- 使用 INSTANTIATE_TEST_SUITE_P(InstantiationName,TestSuiteName,param_generator) 实例化该测试套件，使用 Combine 组合两个 Values 参数集，参数任选。 

在 ``./unittest-cpp`` 目录下编译并运行测试，观察结果。完成用例编写之余请思考：如果输入参数的全排列面临组合爆炸问题，你有什么策略减少测试用例数量？

### 1.4.4 类型参数化测试

类型参数化测试可以在同一段测试代码中，使用不同数据类型进行测试,不必为每个数据类型单独编写测试逻辑。我们现在的计算器实现 ``Calculator.h`` 只能接受 ``int`` 作为输入，因此，你需要：
- (已完成)扩展计算器实现使其支持 ``double`` 和 ``float``。为此，在 ``UniversalCalculator.h`` 中进行[模板声明](https://learn.microsoft.com/en-us/cpp/cpp/templates-cpp) ``template <typename T>`` 并将四个基本的数学运算方法均改写为模板函数（e.g., ``T add(T a, T b)``）。
- 创建一个新的测试文件 ``universalCalculator_test.cc``，并在其中：
  - 定义测试套件 ``CalculatorTest``:
    `````C++
    template <typename T>
    class CalculatorTest : public ::testing::Test {};
    `````
  - 定义类型列表 ``MyTypes``，其中包含了我们要测试的类型（包括 ``int``, ``float``, ``double``）。
  - 使用 ``TYPED_TEST_SUITE(CalculatorTest, MyTypes)`` 绑定测试类和类型列表。
  - 使用``TYPED_TEST(CalculatorTest, AddTest)`` 编写测试逻辑。注意使用 ``TypeParam`` 引用类型参数，以实例化计算器类并定义输入参数。使用 EXPECT_EQ 测试一组用例即可。

在 ``./unittest-cpp`` 目录下编译并运行测试，观察结果。完成用例编写之余请思考：在类型参数化测试中，如何处理类型之间行为的差异？

## 2 Java 单元测试
### 2.1 实验目的

使用 Java 单元测试框架 JUnit 的特性，实践部分黑盒和白盒测试方法。

### 2.2 环境配置

安装 ≥ Java 8 的 Java Development Kit,本实验推荐版本为 OpenJDK 21。

Windows平台可：
- 通过[该链接](https://learn.microsoft.com/zh-cn/java/openjdk/download)由 msi 安装包安装。
- 通过包管理器安装。
  - WinGet ：``winget install Microsoft.OpenJDK.21``
  - Scoop: ``scoop bucket add java``添加库后，``scoop install openjdk``

Linux 和 Mac 端可直接通过包管理器安装：
- Debian/Ubuntu：``sudo apt install openjdk-21-jdk``
- Mac: ``brew install openjdk@21``

作为 Java 上最流行的单元测试框架， JUnit 可以方便地通过 Maven 和 Gradle 等构建工具集成到软件项目之中。在本实验中，我们使用 Maven 进行构建。Maven 依赖于 Java SDK 运行，因此 OpenJDK 和 Maven 的安装顺序不可颠倒。

Windows平台可：
- 通过 [Maven 官网](https://maven.apache.org/download.cgi) 下载压缩包。解压到任意位置，并将``Maven文件夹路径/bin``目录添加到系统环境变量 ``PATH`` 中。Windows的环境变量可通过“控制面板”>“系统和安全”>“系统”>“高级系统设置”，“系统属性”窗口中，点击“环境变量”，在其中找到“系统变量”区域下的“PATH”变量，选择它，然后点击“编辑”即可。
- 通过包管理器安装。
  - Scoop: ``scoop install maven``

Linux和Mac端可直接通过包管理器安装：
- Debian/Ubuntu：``sudo apt install maven``
- Mac: ``brew install maven``

在 ``unittest-java`` 文件夹中，项目文件结构如下：
`````
unittest-java/
|-- pom.xml
`-- src/
    |-- main/
    |   `-- java/
        `-- resources/
    `-- test/
        `-- java/
        `-- resources/    
`````

其中 ``src/main/java`` 存放项目的主要 Java 源代码,``src/test/java`` 存放项目的测试代码，``pom.xml`` 定义了项目的依赖、插件和其他构建相关的设置。

### 2.3 JUnit 用法介绍

JUnit 的核心注解和断言语法使得它非常易于使用。以下是 JUnit 中常用的基本语法：

#### 注解（Annotations）

JUnit 通过注解来标记测试方法和测试生命周期，常用注解包括：

- @Test：标记一个方法为测试方法。
- @Before：每个测试方法执行前执行，用于准备工作（JUnit 4）。
- @BeforeEach：每个测试方法执行前执行，用于初始化资源（JUnit 5）。
- @After：每个测试方法执行后执行，用于清理工作（JUnit 4）。
- @AfterEach：每个测试方法执行后执行，用于清理资源（JUnit 5）。
- @BeforeClass：在所有测试方法之前只执行一次，用于全局初始化（JUnit 4）。
- @BeforeAll：在所有测试方法之前只执行一次（JUnit 5）。
- @AfterClass：在所有测试方法之后只执行一次，用于全局清理（JUnit 4）。
- @AfterAll：在所有测试方法之后只执行一次（JUnit 5）。
- @Ignore：忽略该测试方法，不执行。

#### 断言（Assertions）

断言用于验证测试执行的预期结果，JUnit 提供的断言方法包括：

- assertEquals(expected, actual)：断言两个值相等。
- assertNotEquals(unexpected, actual)：断言两个值不相等。
- assertTrue(condition)：断言条件为 true。
- assertFalse(condition)：断言条件为 false。
- assertNull(object)：断言对象为 null。
- assertNotNull(object)：断言对象不为 null。
- assertArrayEquals(expectedArray, actualArray)：断言数组相等。
- assertThrows()：断言抛出指定的异常。

### 2.4 实验内容

接下来我们将使用 JUnit 实现几种经典的黑盒和白盒测试方法。

#### 2.4.1 等价类划分

等价类划分是将所有可能的输入数据（包括输出）按照规则划分为若干个“等价类”，每个等价类内的数据从程序的角度来看是相同的。对每个等价类至少选取一个代表性数据作为测试案例。这些类通常被分为两大类：

- 有效等价类：合法的、预期能被系统正确处理的输入数据。
- 无效等价类：不合法的、预期会被系统拒绝或特殊处理的输入数据。

本部分的测试对象是 ``Date`` 类中的 ``next()`` 方法，它会提供当前日期的下一天。对于该问题，可以通过查看 ``Date.java`` 的源码，观察程序如何处理不同种类日期，以划分等价类。``DateTests.java`` 已提供了一个普通月份中间日的测试用例，请完成剩余等价类的测试用例，并在实验报告中列出具体的划分策略。

完成用例后，在 ``./unittest-java`` 目录下使用 ``mvn test`` 运行测试。完成用例编写之余请思考：在设计等价类测试用例时，如何确保测试用例的代表性？

#### 2.4.2 边界值分析

根据软件测试实践经验来看，错误往往发生在输入或输出范围的边界而非中间值上。因此，边界值分析方法侧重于选取等价类的边界值。

以密码验证功能为例，该功能通常包含一系列规则，比如密码的最小长度、最大长度、必须包含的字符种类等。现有一个密码验证类 ``PasswordValidator``，要求对输入的密码进行验证。密码规则如下：

- 密码长度：至少8个字符，最多20个字符。
- 必须包含至少一个数字。
- 必须包含至少一个大写字母。
- 必须包含至少一个特殊字符（特殊字符范围为!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~）。

现提供了一个 ``PasswordValidator`` 的实现。请注意，这个实现是有缺陷的。请在 ``PasswordValidatorTests`` 用边界值分析的方法对密码验证功能进行测试，找到该缺陷，并修复它。

完成用例后，在 ``./unittest-java`` 目录下使用 ``mvn test`` 运行测试。思考：为什么边界值容易出错？边界值分析和等价类划分如何结合使用？

#### 2.4.3 覆盖率度量

在白盒测试中，覆盖率分析对于优化测试策略，提升代码质量的意义重大。本节将应用覆盖率分析工具 OpenClover，生成行、分支、条件、方法等多种覆盖率度量，并以可视化覆盖率报告的形式。

为在项目中引入 OpenClover，你需要修改 ``pom.xml``，引入 OpenClover 插件。完成后，在 ``./unittest-java`` 目录下使用 ``mvn clean test`` 运行测试并生成覆盖率报告，默认报告路径在 ``.\target\site\index.html`` 中。

请分析可视化 HTML 报告中各个覆盖率数据的含义，它们对于指导软件测试的意义。
