package com.example.project;

public class Date {
    private int year;
    private int month;
    private int day;

    public Date(int year, int month, int day) {
        if (!isValidDate(year, month, day)) {
            throw new IllegalArgumentException("Invalid date provided");
        }
        this.year = year;
        this.month = month;
        this.day = day;
    }

    private boolean isValidDate(int year, int month, int day) {
        int[] daysInMonth = {
            31, isLeapYear(year) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
        };
        return month >= 1 && month <= 12 && day >= 1 && day <= daysInMonth[month - 1];
    }

    public Date next() {
        int newDay = this.day + 1;
        int newMonth = this.month;
        int newYear = this.year;

        int[] daysInMonth = {
            31, isLeapYear(newYear) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
        };

        if (newDay > daysInMonth[this.month - 1]) {
            newDay = 1;
            newMonth++;
            if (newMonth > 12) {
                newMonth = 1;
                newYear++;
            }
        }

        return new Date(newYear, newMonth, newDay);
    }

    private boolean isLeapYear(int year) {
        return ((year % 4 == 0) && (year % 100 != 0)) || (year % 400 == 0);
    }

    // Getters to check the date values
    public int getYear() {
        return year;
    }

    public int getMonth() {
        return month;
    }

    public int getDay() {
        return day;
    }

    public boolean equals(Date date) {
        return this.year == date.year && this.month == date.month && this.day == date.day;
    }

    public static void main(String[] args) {
        Date date = new Date(2020, 2, 28);  // Example date
        Date nextDate = date.next();
        System.out.println("Next date is: " + nextDate.getYear() + "-" + nextDate.getMonth() + "-" + nextDate.getDay());
    }
}
