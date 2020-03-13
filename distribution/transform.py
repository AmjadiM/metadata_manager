import pandas as pd
import os

"""
Can create several files based off the master metadata for distribution
Pi Data Descriptors -- Pivotted version of master metadata for SQL Server
Subscriptions -- All tags with metric and server for PI data collector subscription file
Statuses -- All the tags and start date for PI data collector status file

"""


# TODO :: Create data cleaner
# TODO :: Create single insert to mssql for each new row in metadata
# TODO :: Create unit tests for the run methods


class metadata_manager:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

        print(os.getcwd())

    def extract_data(self):
        # Load metadata excel
        xl_file = pd.read_excel(self.input_file, sheet_name="PI_METADATA")
        return xl_file

    def write_data(self, df, filetype):
        # Option to write as CSV or excel
        if filetype.lower() == "excel":
            df.to_excel(self.output_file + ".xlsx", engine="openpyxl", index=False,
                        sheet_name=os.path.basename(self.output_file))
        elif filetype.lower() == "csv":
            df.to_csv(self.output_file + ".csv", index=False, header=False)
        else:
            raise ValueError

    def create_pi_data_descriptors(self):
        xl_file = self.extract_data()
        # pivot_df = self.pivot_data(xl_file)
        pivot_df = pd.melt(xl_file, ['tag']) \
            .rename(columns={"variable": "descriptor_name", "value": "descriptor_value"}) \
            .sort_values(['tag'])
        self.write_data(pivot_df, "excel")

    def create_pi_data_groupings(self):
        pass

    def create_subscriptions(self):
        # Create subscription tags for PI Data Collector
        xl_file = self.extract_data()
        xl_file['server'] = "PISERVER_MP"
        sub_df = xl_file[['tag', 'metric', 'server']]
        sub_df = sub_df[['tag', 'server', 'metric']]
        self.write_data(sub_df, "csv")
        return sub_df

    def create_statuses(self):
        # Create status file for PI Data Collector
        xl_file = self.extract_data()
        xl_file['last_updated'] = "19700101000000000"
        status_df = xl_file[['tag', 'last_updated']]
        self.write_data(status_df, "csv")
        return status_df

    def load_to_mssql(self):
        # Load the metadata to SQL server either using truncate and load or append
        pass

    def check_data(self):
        # Check for duplicates
        pass

    def clean_data(self):
        # Strip whitespace from ends
        pass


if __name__ == "__main__":
    metadata_manager(input_file="data/sql_metadata.xlsx", output_file="data/subscriptions").create_subscriptions()
