import cpg_islands_preprocessing as cip

def main():
    progres_report_dir = "../"
    input_dir = progres_report_dir + 'sekvence gena/'
    output_dir = progres_report_dir + 'cpg_islands_input/'

    cip.reformat_files(input_dir, output_dir)

if __name__ == "__main__":
    main()