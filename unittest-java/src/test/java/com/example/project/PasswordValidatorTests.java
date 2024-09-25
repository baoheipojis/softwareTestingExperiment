package com.example.project;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class PasswordValidatorTests {

    @Test
    public void testValidMinLengthPassword() {
        assertTrue(PasswordValidator.isValid("A1@bcdef"));
    }
    // 用边界值分析的方法对密码验证功能进行测试
}