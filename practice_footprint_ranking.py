#import all necessary packages and libraries
import pandas as pd
import numpy as np

#set options so you can see all columns in snapshots, not just a truncated list
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df_lexmach_intel = pd.read_csv('lexmach_intel.csv')

# Calculate Practice Footprint Ranking
# Calculate litigation footprint

# Calculate geographic reach

# Get total cases
total_cases = df_lexmach_intel['Total Cases'].sum()

districts = ['D.Me.',
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

 # Sum each column for total cases per district and calculate percentage of cases per district for weighting
district_weight = {}
for x in districts:
    district_sum = df_lexmach_intel[x].sum()
    district_score = district_sum / total_cases
    district_weight[x] = district_score

busiest_district = max(district_weight, key=district_weight.get)

busy_districts = sorted(district_weight, key=district_weight.get, reverse=True)[:5]

for district in busy_districts:
    df = df_lexmach_intel[['firm_name', 'Total Cases', 'Districts', district]].sort_values(by=district, ascending=False)
    display(df)

# If a firm has at least 1 cases in that district, that firm earns that district's score
geographic_footprint_score_raw = []
for row in df_lexmach_intel.iterrows():
    firm_id = row[1]['firm_id']
    score = 0
    for district in districts:
        district_count = row[1][district]
        if district_count > 0:
            score += district_weight[district]
        else:
            continue
    geographic_footprint_score_raw.append(score)

df_lexmach_intel['geo_score_raw'] = geographic_footprint_score_raw

# percentile rank the geo scores
df_lexmach_intel['Geo_Percentile_Rank'] = df_lexmach_intel.geo_score_raw.rank(pct=True)

geo_eval = df_lexmach_intel[['firm_name', 'Total Cases', 'Districts', 'Geo_Percentile_Rank']].sort_values(by='Geo_Percentile_Rank', ascending=False)

case_types = ['Antitrust',
 'Consumer Protection',
 'Contracts',
 'Copyright',
 'Employment',
 'Insurance',
 'Patent',
 'Product Liability',
 'Securities',
 'Torts']

 # Calculate all-around depth and breadth by taking the perc rank of each case type for each firm
df_lexmach_intel['Antitrust_Perc_Rank'] = df_lexmach_intel['Antitrust'].rank(pct=True)
df_lexmach_intel['Consumer_Protection_Perc_Rank'] = df_lexmach_intel['Consumer Protection'].rank(pct=True)
df_lexmach_intel['Contracts_Perc_Rank'] = df_lexmach_intel['Contracts'].rank(pct=True)
df_lexmach_intel['Copyrights_Perc_Rank'] = df_lexmach_intel['Copyright'].rank(pct=True)
df_lexmach_intel['Employment_Perc_Rank'] = df_lexmach_intel['Employment'].rank(pct=True)
df_lexmach_intel['Insurance_Perc_Rank'] = df_lexmach_intel['Insurance'].rank(pct=True)
df_lexmach_intel['Patent_Perc_Rank'] = df_lexmach_intel['Patent'].rank(pct=True)
df_lexmach_intel['Product_Liability_Perc_Rank'] = df_lexmach_intel['Product Liability'].rank(pct=True)
df_lexmach_intel['Securities_Perc_Rank'] = df_lexmach_intel['Securities'].rank(pct=True)
df_lexmach_intel['Torts_Perc_Rank'] = df_lexmach_intel['Torts'].rank(pct=True)

# Average all perc ranked case types by firm
df_lexmach_intel['Case_Type_Percentile_Rank'] = df_lexmach_intel[['Antitrust_Perc_Rank', 'Consumer_Protection_Perc_Rank', 'Contracts_Perc_Rank', 'Copyrights_Perc_Rank', 'Employment_Perc_Rank', 'Insurance_Perc_Rank', 'Patent_Perc_Rank', 'Product_Liability_Perc_Rank', 'Securities_Perc_Rank', 'Torts_Perc_Rank']].mean(axis=1)

case_type_eval = df_lexmach_intel[['firm_name', 'Total Cases', 'Case_Type_Percentile_Rank']].sort_values(by='Case_Type_Percentile_Rank', ascending=False)

# Calculate transactions footprint

# Calculate completed public deal volume
df_lexmach_intel['Public_Deals_Percentile_Rank'] = df_lexmach_intel['AggregatedDealvalue'].rank(pct=True)

# Calculate completed offering volumne
df_lexmach_intel['Offering_Volume_Percentile_Rank'] = df_lexmach_intel['Offering Volume'].rank(pct=True)

# Calculate practice footprint ranking
df_lexmach_intel['Practice_Footprint_Percentile_Rank'] = df_lexmach_intel[['Geo_Percentile_Rank', 'Case_Type_Percentile_Rank', 'Public_Deals_Percentile_Rank', 'Offering_Volume_Percentile_Rank']].mean(axis=1)

df_lexmach_intel['Practice_Footprint_Rank'] = df_lexmach_intel['Practice_Footprint_Percentile_Rank'].rank(ascending=False)

rank_eval = df_lexmach_intel[['firm_name', 'Practice_Footprint_Score', 'Practice_Footprint_Rank']].sort_values(by='Practice_Footprint_Rank')

df_lexmach_intel['Practice_Footprint_Score'] = round(df_lexmach_intel['Practice_Footprint_Percentile_Rank']*100, 1)

df_lexmach_intel.to_csv('practice_footprint_ranking_2022.csv')
