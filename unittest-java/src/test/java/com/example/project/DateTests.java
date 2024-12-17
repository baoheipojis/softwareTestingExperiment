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
    @Test
    public void testEndOfMonth() {
        Date date = new Date(2021, 1, 31); // 普通月份的最后一天
        Date expected = new Date(2021, 2, 1);
        assertTrue(date.next().equals(expected));
    }

    @Test
    public void testEndOfLeapYear() {
        Date date = new Date(2020, 2, 29); // 闰年的最后一天
        Date expected = new Date(2020, 3, 1);
        assertTrue(date.next().equals(expected));
    }

    @Test
    public void testEndOfYear() {
        Date date = new Date(2021, 12, 31); // 年末的最后一天
        Date expected = new Date(2022, 1, 1);
        assertTrue(date.next().equals(expected));
    }

    @Test
    public void testInvalidDate() {
        assertThrows(IllegalArgumentException.class, () -> new Date(2021, 2, 29)); // 2021年2月29日是无效日期
    }

    @Test
    public void testInvalidMonth() {
        assertThrows(IllegalArgumentException.class, () -> new Date(2021, 13, 1)); // 13月1日是无效日期
    }

    @Test
    public void testInvalidDay() {
        assertThrows(IllegalArgumentException.class, () -> new Date(2021, 1, 32)); // 1月32日是无效日期
    }


    
}