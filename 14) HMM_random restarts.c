#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#include<ctype.h>
#include<string.h>
#define size 26 //size of hidden states N
#define obs_size 300 // size of observation seq set to 50000
#define n 10
static int N = size;
static int M = size; // size of observation states 
static int T = obs_size; // length of observation 
static int obs[obs_size]; //size set to 50000
static double A[size][size]; //state probability distribution
static double B[size][size]; // state transition probability
static double pi[size]; //initial probability distribution
static double c[obs_size]; //scaling factors
static double alphas[obs_size][size];
static double betas[obs_size][size];
static double gamma[obs_size][size];
static double digamma[obs_size][size][size];
static int iterarions = 0;
static int miniterations = 200; //mininum iterations set to 200
static double epsilon = 0.001; //used to compare for logProb
static double logProb = 0;
static double oldLogProb = -INFINITY;
static char chars[26] = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'};
static double modelscores[n];
static int z=0;
void calls(); //function definition

//initialize the matrix A,B and pi with random values and normalize

//to obtain the row position in Digraph
int Row(char cur_row) {
    for (int i = 0; i < size; i++)
    {
        if (chars[i]==cur_row)
        {
            return i;
        }
        
    }
}

//to obtain the column position in Digraph
int col(char cur_col) {
    for (int j = 0; j < size; j++)
    {
        if (chars[j]==cur_col)
        {
            return j;
        }
        
    }
    
}

//scoring model to obtain putative key
void scoreModel(double B[size][size]) {

    double score = 0.0;

    for (int i = 0; i < 23; i++)
    {
        if (B[i][i+3]>=0.5 && i<26) //caeser cipher condition
        {
            score++;
        }
        
    }

    for (int i = 0; i < 4; i++)
    {
        if (B[i][i+3]>=0.5)
        {
            score++;
        }
        
    }
    score = (score/26)*100;
    modelscores[z] = score;
    z++;
    
}
//initialize matrices
void initialize_A_B_pi() {
    
    srand(time(0));
    //initialize matrix A
    /*for (int i = 0; i < N; i++)
    {
        int total = 0;
        for (int j = 0; j < N; j++)
        {
            int randomnum = rand() % 100;
            total = total + randomnum;
            A[i][j] = randomnum;
        }

        for (int j = 0; j < N; j++)
        {
            A[i][j] = A[i][j]/total;
        }
        
        
    }
    */
    FILE *fp1,*fp2;
    fp1 = fopen("C:\\Users\\peeyu\\Downloads\\Brown\\corpus.dos\\","r");
    fp2 = fopen("C:\\Users\\peeyu\\OneDrive\\Documents\\c\\op.txt","w");
    int count = 0;
    
    for (int i = 0; i < 1; i++)
    {
        while (count<1000000) 
        {
            char c = fgetc(fp1);
            if(isalpha(c)) {
                c = tolower(c);
                fputc(c,fp2);
                count++;
            }
            else if (c == EOF)
            {
                break;
            }
            
        }
        fclose(fp1);
        fclose(fp2);
        
    }
    //update digraph
    fp2 = fopen("C:\\Users\\peeyu\\OneDrive\\Documents\\c\\op.txt","r");
    while(!feof(fp2))
    {
        char line[30];
        fgets(line,30,fp2);
        for (int i = 0; i < strlen(line); i++)
        {
            A[Row(line[i])][col(line[i+1])] = A[Row(line[i])][col(line[i+1])] + 1; 
        }
        
    }
    //add 5 to each value to avoid zero
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            A[i][j] = A[i][j]+5;
        }
        
    }

    double sum = 0.0;
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            sum=sum+A[i][j];
        }
        //row stochastic 
        for (int k = 0; k < N; k++)
        {
            A[i][k] = A[i][k]/sum;
        }
        sum = 0;
    }
    
    printf("Generated digraph A from 1000000 characters: \n");
    for (int j = 0; j < N; j++)
    {
        for (int k = 0; k < N; k++)
        {
            printf("%.2f",A[j][k]);
        }
        printf("\n");
        
    }
    
    

    //initialize B matrix
    for (int i = 0; i < N; i++)
    {
        int total = 0;
        for (int j = 0; j < M; j++)
        {
            int randomnum = rand() % 100;
            total = total + randomnum;
            B[i][j] = randomnum;
        }

        for (int j = 0; j < M; j++)
        {
            B[i][j] = B[i][j]/total;
        }
        
        
    }

    //initialize pi matrix
    int total = 0;

    for (int i = 0; i < N; i++)
    {
        
        int randomnum = rand() % 100;
        total = total + randomnum;
        pi[i] = randomnum;

    }
    for (int i = 0; i < N; i++)
    {
        pi[i] = pi[i]/total;
    }
}

//print matrix A, B, pi
void print_matrix() {

    //print matrix A
    printf("Value of A: \n");
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            printf("%f,",A[i][j]);
        }
        printf("\n");
    }
    //print matrix B
    printf("Value of B: \n");
    for (int j = 0; j < N; j++)
    {
        for (int i = 0; i < M; i++)
        {
            printf("%.3f,",B[i][j]);
        }
        printf("\n");
    }
    //print matrix pi
    printf("Value of pi: \n");
    for (int i = 0; i < N; i++)
    {
        printf("%f,",pi[i]);
    }
    printf("\n");
    
}

//open the text files and read for dataset

void read_files(){
    int z=0;
    FILE *fp1;
    char filepath[] = "C:\\Users\\peeyu\\Downloads\\Brown\\corpus.dos\\";
    fp1 = fopen(filepath,"r");
    for (int i = 0; i < T; i++) {
        char c = fgetc(fp1);

        //if EOF break the loop
        if( c==EOF ){
            //fclose(fp);
            break;
        }

        //read the character and add the ascii value to observation matrix
        else if(isalpha(c)) {
            c = tolower(c);
            c = c + 3; //shift by 3
            obs[z]=((c-97)%25);
            int d = (int) c;
        } 

        //update space value as 26
        /*else if(c == ' '){
            obs[z] = 26;
        }*/
        z=z+1;
    }
    fclose(fp1);
}

//alpha-pass
void alpha_calculate() 
{
    //compute alpha(0) and c(0)
    c[0]=0.0; 
    for (int i = 0; i < N; i++)
    {
        alphas[0][i] = pi[i] * B[i][obs[0]];
        c[0]=c[0]+alphas[0][i];
    }

    //scaling
    c[0]=1/c[0];
    for (int i = 0; i < N; i++)
    {
        alphas[0][i] = c[0]*alphas[0][i];
    }

    //compute alpha(t) and c(t)
    for (int t = 1; t < T; t++)
    {
        c[t]=0.0;
        for (int i = 0; i < N; i++)
        {
            alphas[t][i]=0.0;
            for (int j = 0; j < N; j++)
            {
                alphas[t][i] = alphas[t][i]+(alphas[t-1][j]*A[j][i]);
            }
            alphas[t][i] = alphas[t][i]*B[i][obs[t]];
            c[t] = c[t] + alphas[t][i];
        }

        //scaling
        c[t]=1/c[t];
        for (int i = 0; i < N; i++)
        {
            alphas[t][i] = c[t]*alphas[t][i];
        }
    }
    
}

//beta-pass
void beta_calculate() {
    for (int i = 0; i < N; i++)
    {
        betas[T-1][i] = c[T-1];
    }
    
    for (int t = T-2; t>= 0; t--)
    {
        for (int i = 0; i < N; i++)
        {
            betas[t][i] = 0;
            for (int j = 0; j < N; j++)
            {
                betas[t][i] = betas[t][i] + A[i][j]*B[j][obs[t+1]]*betas[t+1][j];
            }
            //scaling
            betas[t][i] = c[t]*betas[t][i];
        }
        
    }
    
}

//compute gamma and digamma
void gamma_digamma_cal() {
    for (int t = 0; t < T - 1; t++)
    {
        for (int i = 0; i < N; i++)
        {
            gamma[t][i]=0;
            for (int j = 0; j < N; j++)
            {
                digamma[t][i][j] = (alphas[t][i]*A[i][j]*B[j][obs[t+1]]*betas[t+1][j]);
                gamma[t][i] = gamma[t][i] + digamma[t][i][j];
            }
            
        }
        
    }
    //special case for gamma
    for (int i = 0; i < N; i++)
    {
        gamma[T-1][i] = alphas[T-1][i];
    }
    
}

void re_estimate(){

    //re-estimate pi
    for (int i = 0; i < N; i++)
    {
        pi[i] = gamma[0][i];
    }
    /*
    //re-estimate A
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            double denom = 0;
            double numer = 0;
            for (int t = 0; t < T-1; t++)
            {
                numer = numer + digamma[t][i][j];
                denom = denom + gamma[t][i];
            }
            A[i][j] = numer /denom;
        }

    }
    */
    //re-estimate B
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < M; j++)
        {
            double numer = 0;
            double denom = 0;
            for (int t = 0; t < T; t++)
            {
                if(obs[t]==j) {
                    numer = numer + gamma[t][i];
                }
                denom = denom + gamma[t][i];
            }
            B[i][j] = numer / denom;
        }
        
    }
    
}

//compute logProb 
void compute_log() {
    logProb = 0;
    for (int i = 0; i < T; i++)
    {
        logProb = logProb + log(c[i]);
    }
    logProb = -1*logProb;
    printf("\n the log value is: %f\n",logProb);
}

//decide to iterate or stop
void decision() {
    iterarions = iterarions + 1;
    double delta = abs(logProb - oldLogProb);
    if ( iterarions < miniterations || delta>epsilon)
    {
        oldLogProb = logProb;
        //printf("this iteration is: %d ",iterarions+1);
        calls();
    }
    else{
        printf("\n the log value is: %f\n",logProb);
        printf("\nThe final matrices of A, B and pi are: \n\n");

        //print_matrix();
        scoreModel(B);
    }
}

//call functions
void calls() {
    alpha_calculate();
    beta_calculate();
    gamma_digamma_cal();
    re_estimate();
    compute_log();
    //print_matrix();
    decision();
}

//main function
int main() {
    int n = n;
    double maxi = 0.0;
    int index = 0;
    for (int i = 0; i < n; i++)
    {
        
        initialize_A_B_pi();
        read_files();
        calls();

    }
    printf("\nAccuracies at indexes:[");
        for (int i = 0; i < n; i++)
        {
            printf("%f,",modelscores[i]);
        }
        //printf("..........\n");
        for (int i = 0; i < n; i++)
        {
            maxi = __max(maxi,modelscores[i]);
        }
        for (int i = 0; i < n; i++)
        {
            double key = maxi;
            if(key==modelscores[i]) {
                index = i;
                break;
            }
        }
        printf("\nn = %d T = %d\n ",n,T);
        printf("\nAt index: %d, The max accuracy is: %f",index,maxi);  
}