import streamlit as st
import pandas as pd
import openpyxl

class LoadData:
    def __init__(self):
        # Open dataset and read data into a DataFrame object.
        self.dyad_df = pd.read_csv("Datasets/dyadic_mid_4.02.csv", parse_dates=['year'], dtype={"fatlev": int})
        # COW Country Codes Dataset
        self.ccodes_df = pd.read_csv("Datasets/COW country codes (1).csv")
        self.ccodes_df.set_index('CCode', inplace=True)
        self.ccodes_dict = self.ccodes_df.to_dict()
        # Initialize a copy of our original DataFrame
        self.dyad_2 = self.dyad_df.copy()

        # Execute Class Methods
        self.add_country_codes()
        self.modify_date_cols()
        self.drop_replace()
        self.open_highact_codes()

        # self.dyad_2.to_excel("dyadic_mid_4.02_reformatted.xlsx")

    def add_country_codes(self):
        # Using the Country Codes we just used to create our dictionary 'ccodes_dict', now
        # create a new dataframe column with this information with the full state name.
        stateA_name_col = [self.ccodes_dict['StateNme'][cc] for cc in self.dyad_df['statea']]  # Get name of STATE A
        stateB_name_col = [self.ccodes_dict['StateNme'][cc] for cc in self.dyad_df['stateb']]  # Get name of STATE B
        # Insert StateA and StateB lists into DataFrame.
        self.dyad_2.insert(3, 'State Name A', stateA_name_col)
        self.dyad_2.insert(6, 'State Name B', stateB_name_col)

    def modify_date_cols(self):
        # Create a new column where each value is a single Start Date, do the same for the End Date.
        # Create new Dataframe column containing the START Date of each MID Conflict.
        start = self.dyad_df["strtmnth"].astype(str) + "-" + self.dyad_df["strtday"].astype(str) + "-" + self.dyad_df["strtyr"].astype(
            str)
        # Convert datetime objects to format 'MM-YYYY'
        self.dyad_2.insert(6, "StartDate", start.astype("datetime64").dt.to_period('M'))
        # Create new Dataframe column containing the END Date of each MID Conflict.
        end = self.dyad_df["endmnth"].astype(str) + "-" + self.dyad_df["endday"].astype(str) + "-" + self.dyad_df["endyear"].astype(
            str)
        # Convert datetime objects to format 'MM-YYYY'
        self.dyad_2.insert(7, "EndDate", end.astype("datetime64").dt.to_period('M'))

    def drop_replace(self):
        # Drop columns containing start/end day, month, and year.
        self.dyad_2.drop(
            columns=["statea", "stateb", "dyindex", "dyad", "changetype_1", "endday", "endmnth", "endyear", "strtday",
                    "strtmnth", "strtyr"], inplace=True)

        # Cast specified Dataframe columns to dtype of String because these are Categorical Variables.
        self.dyad_2[["disno", "fatlev", "highact", 'hihost', "mid5hiact", "mid5hiacta", "outcome", "mid5hiactb", "settlmnt"]] = \
            self.dyad_2[["disno", "fatlev", "highact", 'hihost', "mid5hiact", "mid5hiacta", "outcome", "mid5hiactb",
            "settlmnt"]].astype('string')

        # Replace numerical string value for Outcome with what it represents.
        self.dyad_2["outcome"] = self.dyad_2["outcome"].replace(
            {'0': 'Ongoing MID','1': 'Win State A', '2': 'Win State B', '3': 'Yield by A', '4': 'Yield by B', '5': 'Stalemate', '6': 'Compromise'})

        # Replace numerical string value for Outcome with what it represents.
        self.dyad_2["settlmnt"] = self.dyad_2["settlmnt"].replace(
            {'1': 'Negotiated', '2': 'Imposed', '3': 'None', '4': 'Unclear', '0': 'Missing', '-9': 'Missing'})

        # Replace numerical string value for Outcome with what it represents. Fatality level of dyadic dispute
        self.dyad_2["fatlev"] = self.dyad_2["fatlev"].replace(
            {'0': 'None','1': '1-25', '2': '26-100', '3': '101-250', '4': '251-500', '5': '501-999', '6': '+1000', '-9': 'Unknown'})

    def open_highact_codes(self):
        highact_codes = open("Datasets/HIGHACT.txt").readlines()
        codes_dict = {}
        num = 1
        for line in highact_codes:
            if num == 11 or num == 21:
                num += 1
            act = line.strip()
            codes_dict[str(num)] = act
            num += 1
        for i in range(1, 25):
            if i == 11 or i == 21:
                pass
            else:
                self.dyad_2["highact"] = self.dyad_2["highact"].replace({str(i): codes_dict[str(i)]})

    def get_dyadic_df(self):
        return self.dyad_2

class Streamlit:
    def __init__(self, load):
        st.set_page_config(page_title="War Correlates Data Dashboard", page_icon="☢️️", layout="wide")
        st.write("""
                # War Correlates Data Dashboard
                """)
        st.write("1816-2014")
        st.write("---")

        # Dyadic War Df
        self.dyadic_df = load.get_dyadic_df()
        # self.plot_stateA()
        self.group_by_disno()

    def plot_stateA(self):
        stateA_count = self.dyadic_df["State Name A"].value_counts()[:10].sort_index(ascending=True)
        countries = [i for i in stateA_count.index]
        country_select = st.multiselect("Filter Data by Country", countries)

    def group_by_disno(self):

        group = self.dyadic_df.groupby(by='disno', as_index=False)
        for item in group:
            print(item[0])









# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    loadData = LoadData()
    streamlitClass = Streamlit(loadData)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
