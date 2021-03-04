import pandas as pd
import scipy.stats as stats
from scipy.stats import chi2_contingency

class ChiSquare:

    def __init__(self, dataframe):
        self.df = dataframe

        self.p = None #P-Value
        self.chi2 = None #Chi Test Statistic
        self.dof = None
        self.dfObserved = None
        self.dfExpected = None

        self.important_vars = []
        self.non_important_vars = []
        
    def chisquare_result(self, colX, alpha):

        if self.p < alpha:
        #     display = "{0} is IMPORTANT for Prediction, p = {1}".format(colX, self.p)
        #     print(display)
            self.important_vars.append((colX, self.p, self.chi2))
        else:
            # display = "{0} is NOT an important predictor. (Discard {0} from model)".format(colX)
            # print(display)
            self.non_important_vars.append((colX, self.p, self.chi2))

        
    def test_independence(self, colX, colY, alpha=0.05):
        X = self.df[colX].astype(str)
        Y = self.df[colY].astype(str)
        
        self.dfObserved = pd.crosstab(Y,X) 
        chi2, p, dof, expected = stats.chi2_contingency(self.dfObserved.values)
        self.p = p
        self.chi2 = chi2
        self.dof = dof 
        
        self.dfExpected = pd.DataFrame(expected, columns=self.dfObserved.columns, index = self.dfObserved.index)
        
        self.chisquare_result(colX, alpha)