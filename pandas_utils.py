"""
Name: Pandas Utilities
Author: Harley Williamson
Description: A group of functions which use the pandas library to open files, find errors, and write output
files, and create log files.
"""
import pandas as pd
from pathlib import Path

import json



def open_json():
    with open("config.json", "r") as config_file:
        config_data = json.load(config_file)
        
    return config_data



"""
A function to determine the file type of the input file with the Pathlib library.
"""
def get_file_type(input_file):
    ext = Path(input_file).suffix.lower()
    return ext

"""
A function to open the input file with the pandas library.
"""
def open_file_with_pandas(input_file):
    ext = get_file_type(input_file)
    
    if ext == ".csv":
        return_df = pd.read_csv(input_file)
    elif ext in {".xlsx",".xls"}:
        return_df = pd.read_excel(input_file)
    else:
        raise ValueError(f"Unsupported file type {ext}, valid types .csv, .xlsx, .xls.")
    
    return return_df, ext

"""
A function to process the date field, to remove the process from the find_issues function.
Returns the invalid_dates counter for the summary report.
"""
def process_date_fields(data_frame, config):
    date_columns = [
        col for col, rules in config["columns"].items()
        if rules.get("validate") == "date"
        ]
    
    invalid_dates = 0

    for date_col in date_columns:
        if date_col not in data_frame.columns:
            print(f'Input file does not have column named "{date_col}"')
            continue
                                                                                                       
        raw_dates = data_frame[date_col]

        
        parsed_dates = pd.to_datetime(raw_dates, errors="coerce", format=config["validation"]["date_format"])
        

        invalid_masks = raw_dates.notna() & parsed_dates.isna()
       
        data_frame[date_col] = parsed_dates
        data_frame[f"_invalid_{date_col}"] = invalid_masks

        invalid_dates += invalid_masks.sum()

    return invalid_dates
"""
This function finds issues in the data frame of the data from the input file, adds a new column, and populates that
column with what issues are found in each row.
Issues searched for:
-Missing data in columns
-Incorrect date format
"""
def find_issues(data_frame, config):
    error_summary = data_frame.isnull().sum()
    
    invalid_dates = process_date_fields(data_frame, config)

    phone_errors = process_phone(data_frame, config)    

    email_errors = process_email(data_frame, config)
 
    data_frame["Issues"] = data_frame.apply(build_issue_string, axis=1, args=(config,))

    drop_columns = data_frame.filter(like="_invalid_", axis = 1).columns.tolist()
    data_frame.drop(drop_columns, axis=1, inplace=True)
    
    return error_summary, invalid_dates, phone_errors, email_errors


def process_email(data_frame, config):
    email_regex = config["validation"]["email_regex"]

    email_cols = [col for col, rules in config["columns"].items()
                  if rules.get("validate") == "email"
                  ]
    email_errors = 0
    for email_col in email_cols:
        if email_col not in data_frame.columns:
            print(f"Input file does not have column named {email_col}")
            continue
    
        raw_email = data_frame[email_col]
        
        parsed_email = raw_email.str.match(email_regex, na=False)
        
        invalid_email_mask = ~parsed_email & raw_email.notna()
       
        
        data_frame[f"_invalid_{email_col}"] = invalid_email_mask
        email_errors += invalid_email_mask.sum()
    return email_errors
        
"""
Processes the phone numbers in a data frame.
"""
def process_phone(data_frame, config):
    
    phone_regex = config["validation"]["phone_regex"]
    
    phone_cols = [col for col, rules in config["columns"].items()
                 if rules.get("validate") == "phone"
                 ]
    phone_errors = 0   
    for phone_col in phone_cols:
        if phone_col not in data_frame.columns:
            print(f"Input file does not have column named {phone_col}")
            continue
        original_phone = data_frame[phone_col]
        raw_phone = original_phone.astype(str)

        parsed_phone = raw_phone.str.match(phone_regex, na=False)

        invalid_phone_mask = ~parsed_phone & original_phone.notna()
        data_frame[f"_invalid_{phone_col}"] = invalid_phone_mask
        phone_errors += invalid_phone_mask.sum()
    
    return phone_errors
        

"""
A function to build issue strings to populate the column any issues are listed in.
"""
def build_issue_string(row,config):
    issues = []

    date_cols = {
                 col for col, rules in config["columns"].items()
                 if rules.get("validate")=="date"
                 }

    phone_cols = {
                col for col, rules in config["columns"].items()
                if rules.get("validate")=="phone"
                }
    email_cols = {
                col for col, rules in config["columns"].items()
                if rules.get("validate")=="email"
                }
    for col, value in row.items():
        if col in date_cols:
            continue
        if col in email_cols:
            continue
        if col in phone_cols:
            continue
        if pd.isna(value):
            issues.append(f"missing {col}")
            
    #invalid date
    for date_col in date_cols:
        flag_col = f"_invalid_{date_col}"
        if row.get(flag_col, False):
            issues.append(f"invalid {date_col}")
        elif pd.isna(row[date_col]):
            issues.append(f"missing  {date_col}")
    
    for phone_col in phone_cols:
        phone_flag = f"_invalid_{phone_col}"
        if row.get(phone_flag, False):
            issues.append(f"Invalid {phone_col}")
        elif pd.isna(row[phone_col]):
            issues.append(f"missing {phone_col}")
        
    for email_col in email_cols:
        email_flag = f"_invalid_{email_col}"
        
        if row.get(email_flag, False):
            issues.append(f"invalid {email_col}")
        elif pd.isna(row[email_col]):
            issues.append(f"missing {email_col}")
            
    
    if not issues:
        return pd.NA
    
    return ",".join(issues)

