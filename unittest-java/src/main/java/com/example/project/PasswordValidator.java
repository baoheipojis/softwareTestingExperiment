package com.example.project;

public class PasswordValidator {
    public static boolean isValid(String password) {
        if (password == null || password.length() < 8 || password.length() > 20) {
            return false;
        }

        boolean hasDigit = false;
        boolean hasUpperCase = false;
        boolean hasSpecialChar = false;

        for (int i = 0; i < password.length(); i++) {
            char c = password.charAt(i);
            if (Character.isDigit(c)) {
                hasDigit = true;
            }
            if (Character.isUpperCase(c)) {
                hasUpperCase = true;
            }
            if (!Character.isLetterOrDigit(c)) {
                hasSpecialChar = true;
            }
        }

        return hasDigit && hasUpperCase && hasSpecialChar;
    }
}
