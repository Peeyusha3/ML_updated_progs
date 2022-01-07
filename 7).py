experiment = [[8, 2],
            [5, 5],
            [9, 1],
            [4, 6],
            [7, 3]]

theta_1 = 0.6918
theta_2 = 0.5597
tow_1 = 0.7593
tow_2 = 0.2407

iterations = 0


def computeProb():
    global theta_1,theta_2,tow_1, tow_2,iterations,experiment
    while iterations < 1:
        inter_tow_1 = 0
        inter_tow_2 = 0
        mew_1 = 0
        mew_2 = 0
        if iterations == 0:
            print("\n Probability values are: ")
        for i in range(len(experiment)):
            inter_p_1 = tow_1 * (theta_1 ** experiment[i][0]) * ((1 - theta_1) ** experiment[i][1])
            inter_p_2 = tow_2 * (theta_2 ** experiment[i][0]) * ((1 - theta_2) ** experiment[i][1])
            p_1 = (inter_p_1 / (inter_p_1 + inter_p_2))
            p_2 = (inter_p_2/ (inter_p_1 + inter_p_2))
    
            if iterations == 0:
                print ("P - (1,",str(i)+") :",p_1)
                print ("P - (2,",str(i)+") :",p_2)
    
            inter_tow_1 += p_1
            inter_tow_2 += p_2
            mew_1 += p_1 * experiment[i][0]
            mew_2 += p_2 * experiment[i][0]
    
        tow_1 = inter_tow_1 / len(experiment)
        tow_2 = inter_tow_2 / len(experiment)
        theta_1 = mew_1 / (10 * len(experiment) * tow_1)
        theta_2 = mew_2 / (10 * len(experiment) * tow_2)
        iterations += 1
    
computeProb()

