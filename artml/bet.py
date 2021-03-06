
# coding: utf-8

# In[23]:

import math
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import chisqprob
import warnings
warnings.filterwarnings('ignore')


# In[24]:

def create_bet(df):
    
    """ BET function constructs the Basic Element Table for the Dataframe. BET is the key step for ARTML and 
    it can be updated with the new data.
    
    BET function returns basic element table as Pandas Dataframe
    
    Notes:
    -----
    see 'Real Time Data Mining' by Prof. Sayad
    
    (https://www.researchgate.net/publication/265619432_Real_Time_Data_Mining)
    
    """
    col = df.columns.tolist()
    l = len(col)                                                              
    x ={}                                                                   # Creating empty dictionary                                 
    for m in range(l):
        for n in range(l):
            x[m,n] = []                                      # Creating keys in dictionary with empty lists
        
    for i in range(l):
        for j in range(l):
            y=col[j]
            z=col[i]
            
            """
            This code makes calculations for all the basic elements in the table. They are appended to 
            a lists of a dictionary.
            
            """
            count_x = len(df[col[i]])                                           # count in particular X column
            x[i,j].append(count_x)
            
            sum_x = df[col[i]].sum()                                                 # Sum of elemensts in y
            x[i,j].append(sum_x)
            
            sum_x2 = (df[z]*df[z]).sum()                                             # Sum of elemensts in x2
            x[i,j].append(sum_x2)
            
            sum_x3 = (df[col[i]]*df[col[i]]*df[col[i]]).sum()                        # Sum of elemensts in x3
            x[i,j].append(sum_x3)
            
            sum_x4 = (df[col[i]]*df[col[i]]*df[col[i]]*df[col[i]]).sum()             # Sum of elemensts in x4
            x[i,j].append(sum_x4)
            
            count_y = len(df[col[j]])                                          # count in particular Y column
            x[i,j].append(count_y)
            
            sum_y = df[col[j]].sum()                                                 # Sum of elemensts in y
            x[i,j].append(sum_y)
            
            sum_y2 = (df[col[j]]*df[col[j]]).sum()                                  # Sum of elemensts in y2
            x[i,j].append(sum_y2) 
            
            sum_y3 = (df[col[j]]*df[col[j]]*df[col[j]]).sum()                       # Sum of elemensts in y3
            x[i,j].append(sum_y3)
            
            sum_y4 = (df[col[j]]*df[col[j]]*df[col[j]]*df[col[j]]).sum()            # Sum of elemensts in y4
            x[i,j].append(sum_y4)
            
            sum_xy = (df[col[i]]*df[col[j]]).sum()                                  # Sum of elemensts in xy
            x[i,j].append(sum_xy)
            
            sum_xy2 = (df[col[i]]*df[col[j]]*df[col[i]]*df[col[j]]).sum()           # Sum of elemensts in (xy)2
            x[i,j].append(sum_xy2)       
            
    z={}
    for m in range(l):                                                    # converting the dictionary to DataFrame
        z[m] = []  
    for i in range(l):
        for j in range(l):
            z[i].append(x[j,i])
    result = pd.DataFrame(z, index=col)
    result.columns = col
    return(result)


# In[25]:

def calculate_basic_elements1(x,key,e,c,i,const):
    
    """ This is an inner function used in learn_by_index & grow_by_index functions for making 
    calculations to update the BET
    
    This takes (BET_dictionary, feature_name, feature_index, values_list, i, +1/-1 (const)) as arguments 
    for making the calculations
    """
    
    x[key][e][0] = (x[key][e][0]+(const*1))

    x[key][e][1] = (x[key][e][1]+(const*c[i]))

    x[key][e][2] = (x[key][e][2]+(const*(c[i]*c[i])))
            
    x[key][e][3] = (x[key][e][3]+(const*(c[i]*c[i]*c[i])))
            
    x[key][e][4] = (x[key][e][4]+(const*(c[i]*c[i]*c[i]*c[i])))

    x[key][e][5] = (x[key][e][5]+(const*1))

    x[key][e][6] = (x[key][e][6]+(const*c[i]))

    x[key][e][7] = (x[key][e][7]+(const*(c[i]*c[i])))
            
    x[key][e][8] = (x[key][e][8]+(const*(c[i]*c[i]*c[i])))
            
    x[key][e][9] = (x[key][e][9]+(const*(c[i]*c[i]*c[i]*c[i])))

    x[key][e][10] = (x[key][e][10]+(const*(c[i]*c[i])))
                               
    x[key][e][11] = (x[key][e][11]+(const*(c[i]*c[i]*c[i]*c[i])))
    
    return x[key][e]


# In[26]:

def calculate_basic_elements2(x,key,k,b,c,i,m,const):    
    
    """ This is an inner function used in learn_by_index & grow_by_index functions for making 
    calculations to update the BET
    
    This takes (BET_dictionary, feature_name, feature_index,feature_names_list, values_list, i, m, +1/-1 (const)) as arguments 
    for making the calculations
    """
    
    x[key][k][0] = (x[key][k][0]+(const*1))

    x[key][k][1] = (x[key][k][1]+(const*c[b.index(m)]))

    x[key][k][2] = (x[key][k][2]+(const*(c[b.index(m)]*c[b.index(m)])))
                    
    x[key][k][3] = (x[key][k][3]+(const*(c[b.index(m)]*c[b.index(m)]*c[b.index(m)])))
            
    x[key][k][4] = (x[key][k][4]+(const*(c[b.index(m)]*c[b.index(m)]*c[b.index(m)]*c[b.index(m)])))
     
    x[key][k][5] = (x[key][k][5]+(const*1))

    x[key][k][6] = (x[key][k][6]+(const*c[i]))

    x[key][k][7] = (x[key][k][7]+(const*(c[i]*c[i])))
                               
    x[key][k][8] = (x[key][k][8]+(const*(c[i]*c[i]*c[i])))
            
    x[key][k][9] = (x[key][k][9]+(const*(c[i]*c[i]*c[i]*c[i])))

    x[key][k][10] = (x[key][k][10]+(const*(c[i]*c[b.index(m)])))

    x[key][k][11] = (x[key][k][11]+(const*(c[i]*c[b.index(m)]*c[i]*c[b.index(m)])))
    
    return x[key][k]


# In[27]:

def learnbyindex(BET, *args):
    
    """ This function takes Basic Element Table and feature_names & values as arguments to update the 
        given list of feature column & rows in the BET by corresponding values.
        
        Examples
        --------
        learnbyindex(Basic_Element_Table, 'feature_1','feature_2', 1, 2 )
        
        The above function updates feature_1, feature_2 in the BET by values 1 and 2 respectively.
    
    """
   
    BET.reset_index(drop = True, inplace = True)                               # convert BET to dictionary
    x = BET.to_dict(orient='list')
    keys = list(x.keys())
    arguments_list = [item for item in args]
    n_features = int(len(arguments_list)/2)                          # no of features given as input for updating BET
    
    if (len(arguments_list))%2 != 0:                    
        print("Error: Give correct set of Feature_names & corresponding parameters")
    
    else:  
        feature_names = arguments_list[0:n_features]
        values=  arguments_list[n_features::]
        
        for i in range(len(feature_names)):
            key = feature_names[i]
            e = keys.index(key)
            calculate_basic_elements1(x,key,e,values,i,1)                           # function for updating elements  BET
            
            for m in feature_names: 
                 if m != feature_names[i]:
                    k = keys.index(m)
                    calculate_basic_elements2(x,key,k,feature_names,values,i,m,1)   # function for updating elements  BET
                    
    df = pd.DataFrame(x)
    df.index = keys
    df = df[keys]
    return df



# In[28]:

def forgetbyindex(BET, *args):
    
    """ This function takes Basic Element Table and feature name & values as arguments to update the 
        given list of features in the BET by corresponding values (deleting effect of those values from BET).
        
        Examples
        --------
        forgetbyindex(Basic_Element_Table, 'feature_1','feature_2', 1, 2 )
        
        The above function reduces feature_1, feature_2 in the BET by values 1 and 2 respectively.
    
    """
    
    BET.reset_index(drop = True, inplace = True)
    x = BET.to_dict(orient='list')                                                   # convert BET to dictionary
    keys = list(x.keys())
    arguments_list = [item for item in args]
    n_features = int(len(arguments_list)/2)  
    
    if (len(arguments_list))%2 != 0:                                        # no of features given as input for updating BET
        print("Give correct set of Index & parameters for function")
    else:  
        feature_names = arguments_list[0 : n_features]
        values=  arguments_list[n_features: :]
        for i in range(n_features):
            key = feature_names[i]
            e = keys.index(key)
            calculate_basic_elements1(x,key,e,values,i,-1)                                  # function for updating elements  BET
            
            for m in feature_names: 
                 if m != feature_names[i]:
                    k = keys.index(m)
                    calculate_basic_elements2(x,key,k,feature_names,values,i,m,-1)

    df = pd.DataFrame(x)
    df = df[keys]
    df.index = keys
    return df



# In[29]:


def growbyindex(BET, *args):
    
    """ This function takes Basic Element Table and feature name & values as arguments to update the 
        BET with new features and corresponding values.
        
        Examples
        --------
        growbyindex(Basic_Element_Table, 'new_feature_1','new_feature_2', 1, 2 )
        
        The above function adds new_feature_1, new_feature_2 in the BET with values 1 and 2 respectively.
    
    """
    
    main_list = list(BET.columns)
    arguments_list = [item for item in args]                                            # convert BET to dictionary
    n_features = int(len(arguments_list)/2)
    if (len(arguments_list))%2 != 0:
        print("Give correct set of Index & parameters for function")
    else:  
        feature_names = arguments_list[0:n_features]
        values =  arguments_list[n_features::]
    
        for i in range(n_features):
            
            elements = [[0]*12]*len(BET)                                         #Creating null  basic elements lists
            BET[feature_names[i]] = elements
            
            new_list = []
            for j in range(len(BET.columns)):               
                new_list.append(list(np.array([0]*12)))
    
            new_row = pd.DataFrame([new_list],columns= list(BET.columns),index = [feature_names[i]])
            BET = pd.concat([BET,new_row])
    
        BET.reset_index(drop = True, inplace = True)
        x = BET.to_dict(orient='list')
        keys = list(x.keys())  
           
        for i in range(n_features):
            key = feature_names[i]
            if key in main_list:
                print('feature already exsists! Use Learn function')
            else:        
                e = keys.index(key)
                calculate_basic_elements1(x,key,e,c,i,1)

    df = pd.DataFrame(BET)
    df.index = keys
    df = df[keys]
    return df


# In[30]:

def learn(BET, df):
          
    """ This function takes Basic Element Table and dataframe as inputs to update the 
        BET with new data in the dataframe. (Incremental Learning of BET with new dataframe as input)
        
        Examples
        --------
        learn(Basic_Element_Table, data_frame)
        
        The above function updates Basic_Element_Table with values in the new dataframe.
    
    """
    
    col = list(df.columns)
    for index, row in df.iterrows():
        row1 = []
        for e in col:
            row1.append(row[e])
        arguments  = col + row1
        BET = learnbyindex(BET, *arguments)
    return BET


# In[31]:

def forget(BET, df):
    
    """ This function takes Basic Element Table and dataframe as inputs to change and remove the  
        effect of that data in the BET. (Decremental Learning of BET with dataframe as input)
        
        Examples
        --------
        forget(Basic_Element_Table, data_frame)
        
        The above function updates Basic_Element_Table with values in the new dataframe.
    
    """
    
    col = list(df.columns)
    for index, row in df.iterrows():
        row1 = []
        for e in col:
            row1.append(row[e])
        arguments  = col + row1
        BET = forgetbyindex(BET, *arguments)
    return BET


