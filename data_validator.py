"""
Name: Flawed Data Report Generator
Author: Harley Williamson
Description: A script to check the contents of a data set (CSV or Excel) for errors including 
missing fields, and invalid date formats in fields.

"""
import pandas_utils as pu
import argparse as ap
import output_utils as ou

def main():

    parser = ap.ArgumentParser()

    parser.add_argument("input_file")
    parser.add_argument("output_file")
    parser.add_argument("--silent", action='store_true')
    parser.add_argument("--issues_only", action='store_true')
    
    args = parser.parse_args()
    
    config_data = pu.open_json()

    data, ext = pu.open_file_with_pandas(args.input_file)

    error_summary, invalid_dates, invalid_phone, invalid_email = pu.find_issues(data, config_data)

    if args.issues_only:
        
        ou.write_file_with_only_errors(data, ext, args.output_file)
    else:
        ou.write_output(args.output_file, data, ext)
    if not args.silent:
       ou.print_summary(error_summary, invalid_dates, invalid_phone, invalid_email, data)    
    
    ou.logging(args.input_file, len(data))
    
    exit_code = 0

    if error_summary.any():
       exit_code |= 1
    if invalid_dates > 0:
       exit_code |= 2
    if invalid_phone > 0:
        exit_code |= 3
    if invalid_email > 0:
        exit_code |= 4
    raise SystemExit(exit_code)

if __name__ == "__main__":
    main()