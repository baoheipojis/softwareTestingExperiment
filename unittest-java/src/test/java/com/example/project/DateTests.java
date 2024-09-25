package com.example.project;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class DateTests {
    @Test
    public void testMiddleOfMonth() {
        Date date = new Date(2021, 1, 10); // 普通月份的中间日
        Date expected = new Date(2021, 1, 11);
        assertTrue(date.next().equals(expected));
    }
    
    // 完成剩余等价类的测试用例

    
}