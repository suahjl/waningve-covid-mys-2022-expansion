# Replication codes for estimating VE against severe outcomes over time

import pandas as pd
import numpy as np
import time
import telegram_send
import dataframe_image as dfi
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

import statsmodels.formula.api as smf

time_start = time.time()

# 0 --- Preliminaries
file_input = 'Data/CasesDeaths_WaningImmunity_WithAZ_Severe_Data_ANONYMISED.parquet'
# Load data frame
print('\n----- Reading input file -----')
time_start_interim = time.time()
df = pd.read_parquet(file_input)
print('\n----- Input file read in ' + "{:.0f}".format(time.time() - time_start_interim) + ' seconds -----')

# I --- Regression setup
print('\n----- Setting up model -----')
time_start_interim = time.time()
# Controls
list_X = ['age', 'comorb', 'male', 'C(malaysian)', 'C(frontliner)', 'trace_count', 'C(state_id)']
controls_X = '+'.join(list_X)
# Treatment
treatment_D = 'C(type_timing)'
# Optimisation method
opt_method = 'ncg'
opt_maxiter = 250 # maximum iterations
# Number of vax combos considered
n_treatment_D = len(list(df['type_timing'].unique())) # first one is omitted
print('\n----- Model set up in ' + "{:.0f}".format(time.time() - time_start_interim) + ' seconds -----')

# II --- Functions
print('\n----- Defining functions -----')
time_start_interim = time.time()


def logitVE(equation='',
            method=opt_method,
            maxiter=opt_maxiter,
            data=df,
            n_keep=n_treatment_D,
            output_suffix=''):
    _mod = smf.logit(equation, data=data)
    _result = _mod.fit(method=method, maxiter=maxiter)
    print(_result.summary())
    _VE = 100 * (1 - np.exp(_result.params))
    _VE = _VE.iloc[1:n_keep]
    _CI = 100 * (1 - np.exp(_result.conf_int()))
    _CI = _CI.iloc[1:n_keep, :]
    _CI.rename(columns={0: 'UB', 1: 'LB'}, inplace=True)
    _CI = _CI[['LB', 'UB']]
    _VE = pd.concat([_VE, _CI], axis=1)
    _VE.rename(columns={0:'VE'}, inplace=True)
    _VE = _VE.round(2)

    _VE.index = _VE.index.str.replace('C(type_timing)[T.', '', regex=False)
    _VE.index = _VE.index.str.replace('1]', '_7to14Weeks', regex=False)  # early
    _VE.index = _VE.index.str.replace('2]', '_0to7Weeks', regex=False)  # late

    fig = plt.figure()
    labels = _VE.copy()
    # d = np.log(_VE)
    # d = d.replace(np.inf, np.nan)  # log(0)
    # d = d.replace(-np.inf, np.nan)  # log(0)
    sns.heatmap(_VE, annot=labels, cmap='magma', center=0, annot_kws={'size': 20}, fmt='g', cbar=False)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    fig.tight_layout()
    fig.savefig('Output/MYSWaningImmunity_WithAZ_Severe_Est1a_VE_' + output_suffix + '_Heatmap.png')

    dfi.export(_VE, 'Output/MYSWaningImmunity_WithAZ_Severe_Est1a_VE_' + output_suffix + '.png')
    _VE.to_csv('Output/MYSWaningImmunity_WithAZ_Severe_Est1a_VE_' + output_suffix + '.csv')

    return _VE, _result, _mod


print('\n----- Functions defined in ' + "{:.0f}".format(time.time() - time_start_interim) + ' seconds -----')

# IV --- Estimation
print('\n----- Estimating models -----')
# Consolidated
VE_consol = pd.DataFrame(columns=['Outcome', 'VE', 'LB', 'UB'])
for i, j in tqdm(zip(['icu', 'dead'], ['ICU', 'Death'])):
    VE, result, mod = logitVE(equation=i + ' ~ ' + treatment_D + ' + ' + controls_X, output_suffix='Full_' + i)
    VE['Outcome'] = j  # nice label
    VE_consol = pd.concat([VE_consol, VE], axis=0)
dfi.export(VE_consol, 'Output/MYSWaningImmunity_WithAZ_Severe_Est1a_VE_consol.png')
VE_consol.to_csv('Output/MYSWaningImmunity_WithAZ_Severe_Est1a_VE_consol.csv', index=True)
print('\n----- Models estimated in ' + "{:.0f}".format(time.time() - time_start_interim) + ' seconds -----')

# End
print('\n----- Ran in ' + "{:.0f}".format(time.time() - time_start) + ' seconds -----')
