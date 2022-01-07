#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#include<ctype.h>
#include<string.h>
#define N_size 26 //size of hidden states N
#define obs_size 425 // size of observation seq set to 50000
#define M_size 54
static int N = 26;
static int M = 54; // size of observation states 
static int T = obs_size; // length of observation 
//static int obs[obs_size]; //size set to 50000
static double A[N_size][N_size]; //state probability distribution
static double B[N_size][M_size]; // state transition probability
static double pi[N_size]; //initial probability distribution
static double c[obs_size]; //scaling factors
static double alphas[obs_size][N_size];
static double betas[obs_size][N_size];
static double gamma[obs_size][N_size];
static double digamma[obs_size][N_size][N_size];
static int iterarions = 0;
static int miniterations = 100; //mininum iterations set to 200
static double epsilon = 0.001; //used to compare for logProb
static double logProb = 0;
static double oldLogProb = -INFINITY;
static char chars[26] = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'};
//zodiac 408 symbols
static int obs[425] = {0,1,2,3,4,3,5,6,1,7,8,9,10,11,12,10,6,13,14,15,16,17,18,19,20,0,21,2,22,23,24,25,18,16,
	        26,27,18,28,5,29,7,30,25,31,32,33,34,18,35,36,37,38,39,3,0,40,6,2,8,9,41,5,1,42,9,43,25,44,7,28,45,26,4,27,
	        46,47,48,11,19,21,14,13,16,49,18,22,15,25,17,35,0,23,29,37,20,25,12,49,36,50,38,39,22,15,25,17,35,0,23,29,
	        37,20,25,12,49,36,50,38,39,9,33,32,29,18,44,43,8,49,25,17,6,31,34,38,40,6,45,46,3,2,40,6,22,12,25,44,21,26,5,
	        28,9,9,7,51,4,23,25,11,29,37,13,25,24,49,36,45,26,47,0,40,6,2,35,9,15,53,10,20,48,33,39,16,44,5,21,7,19,4,51,
	        11,8,14,13,29,36,15,32,45,37,43,28,9,20,21,29,0,35,9,52,31,18,47,48,46,16,3,22,12,27,34,41,2,36,26,49,9,5,32,
	        1,45,37,33,14,44,23,21,10,17,47,29,24,27,7,36,0,49,45,26,43,33,41,37,4,39,2,50,5,11,7,41,0,40,6,14,13,48,15,
	        14,31,32,8,2,28,10,38,47,43,42,5,16,20,30,35,50,17,1,1,29,26,33,7,37,38,51,44,3,0,1,1,4,42,41,2,40,6,14,11,
	        16,12,25,13,25,52,19,40,49,51,15,22,0,41,0,6,1,8,31,36,9,5,51,15,52,46,18,25,52,28,38,25,13,14,4,16,17,18,23,
	        44,52,31,18,41,0,1,40,45,32,52,21,24,19,6,12,0,50,12,41,35,46,48,30,45,24,10,25,52,16,46,40,40,20,16,36,2,8,9,
	        12,34,19,1,17,51,4,22,27,31,32,25,52,49,27,29,15,47,6,2,34,13,20,14,44,12,47,0,13,29,20,25,44,21,26,37,10,5,29,7};
static double modelscores[1000];
static int z=0;
//zodiac symbols mapping to plain text "Ilikeki...."
static int zodiacMapping[26][7] = {{43,17,49,38,54,54,54},{14,54,54,54,54,54,54},{16,54,54,54,54,54,54},{50,42,54,54,54,54,54},{15,11,13,33,4,20,44},
                {27,34,54,54,54,54,54},{9,54,54,54,54,54,54},{26,37,54,54,54,54,54},{5,7,0,2,54,54,54},{54,54,54,54,54,54,54},
                {3,54,54,54,54,54,54},{6,1,40,54,54,54,54},{25,54,54,54,54,54,54},{8,39,28,35,54,54,54},{46,31,12,24,54,54,54},
                {10,54,54,54,54,54,54},{54,54,54,54,54,54,54},{32,47,48,54,54,54,54},{19,23,30,22,54,54,54},{36,45,21,29,54,54,54},
                {18,54,54,54,54,54,54},{51,54,54,54,54,54,54},{41,54,54,54,54,54,54},{53,54,54,54,54,54,54},{52,54,54,54,54,54,54},
                {54,54,54,54,54,54,54}};
void calls(); //function definition

//initialize the matrix A,B and pi with random values and normalize

//to obtain the row position in Digraph
int Row(char cur_row) {
    for (int i = 0; i < 26; i++)
    {
        if (chars[i]==cur_row)
        {
            return i;
        }
        
    }
}

//to obtain the column position in Digraph
int col(char cur_col) {
    for (int j = 0; j < 26; j++)
    {
        if (chars[j]==cur_col)
        {
            return j;
        }
        
    }
    
}

//scoring model to obtain putative key
void scoreModel(double B[26][54]) {

    double score = 0.0;

    for (int i = 0; i < N; i++)
    {
        if(i==9||i==16||i==25) //squares of 3,4,5 corresponding to non alphabetic 
        {
            score++;
            continue;
        }

        for (int j = 0; j < 7; j++) //each set of 7
        {
            if (zodiacMapping[i][j]==54)
            {
                continue;
            }
            
            if(B[i][zodiacMapping[i][j]]>0.1)
            {
                score++;
            }
        }  
        
    }

    
    score = (score/54)*100; //putative key score
    modelscores[z] = score;
    z++;
    printf("Model Score: %.5f\n",score);
    
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
    
    /*printf("Generated A from 1000000");
    for (int j = 0; j < N; j++)
    {
        for (int k = 0; k < N; k++)
        {
            printf("%.2f",A[j][k]);
        }
        printf("\n");
        
    }*/
    
    

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
    /*int z=0;
    FILE *fp1;
    char filepath[] = "C:\\Users\\peeyu\\Downloads\\Brown\\corpus.dos\\";
    fp1 = fopen(filepath,"r");
    for (int i = 0; i < T; i++) {
        char c = fgetc(fp1);

        //if EOF break the loop
        if( c==EOF ){
            //printf(" eof ");
            //fclose(fp);
            break;
        }

        //read the character and add the ascii value to observation matrix
        else if(isalpha(c)) {
            c = tolower(c);
            c = c + 3;
            obs[z]=((c-97)%25);
            //printf("%d",obs[z]);
            int d = (int) c;
        } 

        //update space value as 26
        /*else if(c == ' '){
            obs[z] = 26;
        }
        z=z+1;
    }
    fclose(fp1); */
    

    static char plaintext[] = "ilikekillingpeoplebecauseitissomuchfunitismorefunthankillingwildgameintheforrestbecausemanisthemostdangeroueanamalofalltokillsomethinggivesmethemostthrillingexperenceitisevenbetterthangettingyourrocksoffwithagirlthebestpartofitisthaewhenidieiwillbereborninparadiceandalltheihavekilledwillbecomemyslavesiwillnotgiveyoumynamebecauseyouwilltrytosloidownoratopmycollectiogofslavesformyafterlifeebeorietemethhpiti";
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
    //printf("\n the log value is: %f\n",logProb);
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
        //printf("\n the log value is: %f\n",logProb);
        //printf("\nThe final matrices of A, B and pi are: \n\n");
        iterarions = 0;
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
    int n = 1000;
    double maxi = 0.0;
        int index = 0;
    for (int i = 0; i < n; i++)
    {
        initialize_A_B_pi();
        read_files();
        calls();
    }
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
        printf("\n Maximum Accuracy after n %d",n);
        printf("\nAt index: %d, The max accuracy is: %f",index,maxi);
      
}