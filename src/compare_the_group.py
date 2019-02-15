import scipy.stats as scs

def compare_the_groups(df, cats, sig_level):
    significant_comparisons = []
    for cat1 in cats:
        for cat2 in cats:
            cat1_sample = df['Percent_Return'][df['Category_Name'] == cat1]
            cat2_sample = df['Percent_Return'][df['Category_Name'] == cat2]  
            test, p_value = scs.ttest_ind(cat1_sample, cat2_sample)
            if p_value < sig_level:
                significant_comparisons.append([cat1, cat2])
    return significant_comparisons