#include<stdio.h>
#include<math.h>
#include<stdlib.h>
#include<ctype.h>

static int N = 2;
static int M = 3;
static int T = 4;
static double A[2][2] = {{0.7,0.3},{0.4,0.6}};
static double B[2][3] = {{0.1,0.4,0.5},{0.7,0.2,0.1}};
static double pi[2] = {0.6,0.4};
static int obs[4];
static double directcomp = 0.0;
static double alphasum = 0.0;
static int observationsequence[4];
static int states[16][4]= {{0,0,0,0},{0,0,0,1},{0,0,1,0},{0,0,1,1,},{0,1,0,0},{0,1,0,1},{0,1,1,0},{0,1,1,1},{1,0,0,0},{1,0,0,1},{1,0,1,0},{1,0,1,1},{1,1,0,0},{1,1,0,1},{1,1,1,0},{1,1,1,1}};
static double alpha[4][2];

//direct computation
void direct_computation() {
    double prob = 0.0;

    for (int i = 0; i < 16; i++)
    {
        prob = pi[states[i][0]]*B[states[i][0]][observationsequence[0]]*A[states[i][0]][states[i][1]]*
                B[states[i][1]][observationsequence[1]]*A[states[i][1]][states[i][2]]*B[states[i][2]][observationsequence[2]]*
                A[states[i][2]][states[i][3]]*B[states[i][3]][observationsequence[3]];
    directcomp = directcomp + prob;
    }
    printf("\nProbability by direct calculation: %.9f \t",directcomp,"\n");
}

//alpha-pass
void alpha_calculate() {
    for (int i = 0; i < N; i++)
    {
        alpha[0][i] = pi[i]*B[i][observationsequence[0]];
    }
    
    for (int t = 1; t < T; t++)
    {
        for (int i = 0; i < N; i++)
        {
            alpha[t][i] = 0;

            for (int j = 0; j < N; j++)
            {
                alpha[t][i] = alpha[t][i] + alpha[t-1][j]*A[j][i];
            }
            alpha[t][i] = alpha[t][i] * B[i][observationsequence[t]];
        }
        
    }
    alphasum = alphasum + alpha[T-1][0] + alpha[T-1][1];
    printf("\nProbability by Alpha pass: %.9f \t",alphasum,"\n");
}

//main function
int main() {
    for (int i = 0; i < M; i++)
    {
        for (int j = 0; j < M; j++)
        {
            for (int k = 0; k < M; k++)
            {
                for (int l = 0; l < M; l++)
                {
                    observationsequence[0] = i;
                    observationsequence[1] = j;
                    observationsequence[2] = k;
                    observationsequence[3] = l;
                    direct_computation();
                    alpha_calculate();
                }
                
            }
            
        }
        
    }
    printf("\n\nSum of probabilities by Direct calculation: %.9f\t",directcomp,"\n");
    printf("\n\nSum of probabilities by Alpha pass: %.9f\t",alphasum,"\n");
    printf("\n");
}