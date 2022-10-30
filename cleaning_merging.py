#import all necessary packages and libraries
import pandas as pd
import numpy as np

#set options so you can see all columns in snapshots, not just a truncated list
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#import csvs
df_lexmach =  pd.read_csv("LexMach.csv", low_memory=False)
df_intel_ma = pd.read_csv("Intel_MA.csv", low_memory=False)
df_intel_ro =  pd.read_csv("Intel_RO.csv", low_memory=False)
stylebook = pd.read_csv('stylebook.csv')

# Remove rows without data and firms that do not qualify for ranking (duplicated data,
# international firms with less than 50 attys in US) that are labeled 0 in specificed qualifying column
def take_out_the_trash(df, data_col, qualify_col):
    new_df = df.dropna(subset=[data_col])
    new_df = new_df.drop(new_df.loc[new_df[qualify_col]==0].index)
    return new_df

# Remove specific rows from Lex Machina and Intelligize data
df_lexmach = take_out_the_trash(df_lexmach, 'Total Cases', 'qualify_LM')
df_intel_ma = take_out_the_trash(df_intel_ma, 'DealCount', 'qualify_MA')
df_intel_ro = take_out_the_trash(df_intel_ro, 'Last Offerings Count', 'qualify_RO')

# ID columns that can sum up for LM

lex_cols_to_int = ['Total Cases',
 'As Plaintiff',
 'As Defendant',
 'Districts',
 'States / Territories Count',
 'Judges',
 'Antitrust',
 'Bankruptcy',
 'Civil Rights',
 'Consumer Protection',
 'Contracts',
 'Copyright',
 'Employment',
 'Environmental',
 'ERISA',
 'False Claims',
 'Insurance',
 'Patent',
 'Product Liability',
 'Securities',
 'Surety Bond',
 'Tax',
 'Torts',
 'Trademark',
 'Trade Secret',
 'D.Me.',
 'D.Mass.',
 'D.N.H.',
 'D.R.I.',
 'D.P.R.',
 'D.Conn.',
 'E.D.N.Y.',
 'N.D.N.Y.',
 'S.D.N.Y.',
 'W.D.N.Y.',
 'D.Vt.',
 'D.Del.',
 'D.N.J.',
 'E.D.Pa.',
 'M.D.Pa.',
 'W.D.Pa.',
 'D.V.I.',
 'D.Md.',
 'E.D.N.C.',
 'M.D.N.C.',
 'W.D.N.C.',
 'D.S.C.',
 'E.D.Va.',
 'W.D.Va.',
 'N.D.W.Va.',
 'S.D.W.Va.',
 'E.D.La.',
 'M.D.La.',
 'W.D.La.',
 'N.D.Miss.',
 'S.D.Miss.',
 'E.D.Tex.',
 'N.D.Tex.',
 'S.D.Tex.',
 'W.D.Tex.',
 'E.D.Ky.',
 'W.D.Ky.',
 'E.D.Mich.',
 'W.D.Mich.',
 'N.D.Ohio',
 'S.D.Ohio',
 'E.D.Tenn.',
 'M.D.Tenn.',
 'W.D.Tenn.',
 'C.D.Ill.',
 'N.D.Ill.',
 'S.D.Ill.',
 'N.D.Ind.',
 'S.D.Ind.',
 'E.D.Wis.',
 'W.D.Wis.',
 'E.D.Ark.',
 'W.D.Ark.',
 'N.D.Iowa',
 'S.D.Iowa',
 'D.Minn.',
 'E.D.Mo.',
 'W.D.Mo.',
 'D.Neb.',
 'D.N.D.',
 'D.S.D.',
 'D.Alaska',
 'D.Ariz.',
 'C.D.Cal.',
 'E.D.Cal.',
 'N.D.Cal.',
 'S.D.Cal.',
 'D.Guam',
 'D.Haw.',
 'D.Idaho',
 'D.Mont.',
 'D.Nev.',
 'D.N.Mar.I.',
 'D.Or.',
 'E.D.Wash.',
 'W.D.Wash.',
 'D.Colo.',
 'D.Kan.',
 'D.N.M.',
 'E.D.Okla.',
 'N.D.Okla.',
 'W.D.Okla.',
 'D.Utah',
 'D.Wyo.',
 'M.D.Ala.',
 'N.D.Ala.',
 'S.D.Ala.',
 'M.D.Fla.',
 'N.D.Fla.',
 'S.D.Fla.',
 'M.D.Ga.',
 'N.D.Ga.',
 'S.D.Ga.',
 'D.D.C.']

intelma_cols_to_int = ['AggregatedDealvalue']
intelro_cols_to_int = ['Offering Volume']

# Remove commas, dollar signs, dashes, and spaces from columns to be converted to int
def remove_characters_int(df, cols):
    for x in cols:
        try:
            df[x] = df[x].str.replace(',','')
            df[x] = df[x].str.replace('$', '')
            df[x] = df[x].str.replace('-', '')
            df[x] = df[x].str.replace(' ', '')
            df = df.replace(r'^\s*$', 0, regex=True)
        except:
            continue
        df[x] = df[x].astype(float)
    return df

df_lexmach = remove_characters_int(df_lexmach, lex_cols_to_int)
df_intel_ma = remove_characters_int(df_intel_ma, intelma_cols_to_int)
df_intel_ro = remove_characters_int(df_intel_ro, intelro_cols_to_int)

# Given the dupe label and the combine firm ID, replace a row with the sum of that row and the combining row.
def combine_firms(df, dupe_col, new_id, old_id, sum_cols):

# isolate those firms labeled to be merged
    temp = df[~df[dupe_col].isnull()]

# Define the vars needed to combine firms that merged or relabel firms that no longer exist if acquiring firm isn't already in dataset
    for row in temp.iterrows():

# the firm ID of the acquiring firm
        firm_id = row[1][new_id]

# the firm ID of the acquired firm
        old_firm_id = row[1][old_id]

# the row that will be either added to the acquired firm figures or relabeled to be the acquired firm
        acquired_firm = temp.loc[df[new_id] == firm_id]

# the row of the acquiring firm
        main_firm = df.loc[df[old_id] == firm_id]

# if the acquiring firm is not in the dataset, replace firm id and firm name with the acquiring firm's
# instead of adding, we are just relabeling
        if len(main_firm) == 0:
            df.loc[df[new_id] == firm_id, old_id] = firm_id
            new_firm = stylebook.loc[stylebook['firm_id'] == firm_id]
            new_firm = new_firm.reset_index()
#             new_id = new_firm['firm_id'][0]
            new_name = new_firm['Short Form Origin Match Law Firm Name'][0]
#             df.loc[df[new_id] == firm_id, old_id] = new_id
            df.loc[df[new_id] == firm_id, 'law360_firm_name'] = new_name

# logic to aggregate the figures of the acquiring firm and the acquired firm and remove the acquired firm from dataset
        else:
            to_sum = pd.concat([acquired_firm, main_firm])
            for x in sum_cols:
                new_sum = to_sum[x].sum()
                main_firm = main_firm.reset_index(drop=True)
                df.loc[df[old_id] == main_firm[old_id][0], x] = new_sum

# Combine list of States / Territories Names (Only needed for Lex Machina data,
# but there are currently no cases where the acquiring firm does not already
# have all of the states the acquired firm has cases in. Also, this column is
# currently irrelevant to the Practice Footprint Ranking methodology)



# remove acquired firm from temporary dataframe, a key error rises as it seems to try to remove a row that no longer exists.
# How to iterate through temporary dataset based on length of the set of the values in the column combine_LM?
        try:
            temp = temp[temp[new_id] != firm_id]
        except:
            continue

# Remove rows without firm_ID
    df = df.dropna(subset=[old_id]).reset_index(drop=True)

    return df

df_lexmach = combine_firms(df_lexmach, 'dupe_LM', 'combine_LM', 'law360_firm_id', lex_cols_to_int)
df_intel_ma = combine_firms(df_intel_ma, 'dupe_MA', 'combine_MA', 'law360_firm_id', intelma_cols_to_int)
df_intel_ro = combine_firms(df_intel_ro, 'dupe_RO', 'combine_RO', 'law360_firm_id', intelro_cols_to_int)

# Merge datasets
df_lexmach_intelma = pd.merge(df_lexmach, df_intel_ma, how='outer', on='law360_firm_id')
df_lexmach_intel = pd.merge(df_lexmach_intelma, df_intel_ro, how='outer', on='law360_firm_id')

# if law360_firm_name_x is nan, fill with Lawfirm, if law360_firm_name_x is blank, fill with intel_firm_name_RO_2022
df_lexmach_intel.law360_firm_name_x.fillna(df_lexmach_intel.Lawfirm, inplace=True)
df_lexmach_intel.law360_firm_name_x.fillna(df_lexmach_intel.intel_firm_name_RO_2022, inplace=True)

# rename law360_firm_name_x as firm_name and law360_firm_id as firm_id
df_lexmach_intel = df_lexmach_intel.rename(columns={'law360_firm_id': 'firm_id', 'law360_firm_name_x':'firm_name'})


# fill nans with 0
df_lexmach_intel = df_lexmach_intel.fillna(0)

df_lexmach_intel.to_csv('lexmach_intel.csv', index=False)
