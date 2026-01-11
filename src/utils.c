// Local
#include "utils.h"
#include <math.h>


/**
 * Compute the sum of an array
 *
 * @param array     the array to sum
 * @param len       the length of the array
**/
int sum(int array[], unsigned long len)
{
    int i;
    int sum = 0;
    for (i = 0; i < len; i++)
    {
        sum += array[i];
    }

    return sum;
}


/**
 * Return max of two integers
 *
 * @param a     first integer
 * @param b     second integer
**/
int max(int a, int b)
{
    return a < b ? b : a;
}


/**
 * Return min of two integers
 *
 * @param a     first integer
 * @param b     second integer
**/
int min(int a, int b)
{
    return a < b ? a : b;
}


/**
 * Return max of two doubles
 *
 * @param a     first double
 * @param b     second double
**/
double fmax(double a, double b)
{
    return a < b ? b : a;
}


/**
 * Return min of two doubles
 *
 * @param a     first double
 * @param b     second double
**/
double fmin(double a, double b)
{
    return a < b ? a : b;
}


/**
 * Return doubles capped by absolute limit
 *
 * @param x     double
 * @param b     limit
**/
double flimit(double x, double limit)
{
    double y = fabs(x) < limit ? fabs(x) : limit;
    return y * (1.0 - 2.0 * (x < 0));
}
