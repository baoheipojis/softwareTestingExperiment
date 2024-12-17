package com.example.project;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class PasswordValidatorTests {

    @Test
    public void testValidMinLengthPassword() {
        assertTrue(PasswordValidator.isValid("A1@bcdef"));
    }
    // 用边界值分析的方法对密码验证功能进行测试
    @Test
    public void testInvalidShortPassword() {
        assertFalse(PasswordValidator.isValid("A1@bcd"));
    }
    @Test
    public void testValidMaxLengthPassword() {
        assertTrue(PasswordValidator.isValid("1bA@fghijklmnopqrst"));
    }
    @Test
    public void testInvalidLongPassword() {
        assertFalse(PasswordValidator.isValid("A1@bcdefghijklmnopqrstuv"));
    }
    @Test
    public void testInvalidNoDigitPassword() {
        assertFalse(PasswordValidator.isValid("Ab@bcdef"));
    }
    @Test
    public void testInvalidNoUpperCasePassword() {
        assertFalse(PasswordValidator.isValid("a1@bcdef"));
    }
    @Test
    public void testInvalidNoSpecialCharPassword() {
        assertFalse(PasswordValidator.isValid("A1bcdefg"));
    }

}