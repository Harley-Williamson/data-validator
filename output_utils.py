from pathlib import Path
import datetime as dt

"""
A function to create a log file.
"""
def logging(input_file, rows_processed):
    file_path_string = input_file
    filename = Path(file_path_string).name
    current_time = dt.datetime.now()
    time_string = current_time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{rows_processed} lines read from {filename} at {time_string}\n"
    with open("logging.txt", "a") as logfile:
        logfile.write(log_entry)

"""
A function to write the data frame out to the output specified by the user.
"""
def write_output(output_file, data_to_write, file_ext):
    if file_ext == ".csv":
        data_to_write.to_csv(output_file, index = False)
    else:
        data_to_write.to_excel(output_file, index= False)

"""
A function called with the issues_only flag. It creates an output file which only includes rows which have content
the "Issues" column.
"""
def write_file_with_only_errors(data, ext, output_file):

    data_to_write = data[data["Issues"].notnull()]
    if ext == ".csv":
        data_to_write.to_csv(output_file, index = False)
    else:
        data_to_write.to_excel(output_file, index=False)

"""
A function to print a summary to the screen
"""
def print_summary(error_summary, invalid_dates, phone_errors, email_errors, data):
    
    print("*"*30)
    print("Summary Report")
    print("*"*30)
    print("\n")
    print(f"{len(data)} rows processed successfully.")
    print("Columns with missing data:")
    print(error_summary)
    print(f"Invalid dates in last_service_date: {invalid_dates}")
    
    print(f"Invalid numbers in phone: {phone_errors}")
    print(f"Invalid emails: {email_errors}")
