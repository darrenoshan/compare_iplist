#!/usr/bin/env python

import sys
import ipaddress
from datetime import datetime
import os
import logging

# Setup logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def get_ip_addresses_from_file(file_path, reference=False):
    ip_addresses = set()
    error_messages = []

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                network = ipaddress.IPv4Network(line, strict=False)
                ip_addresses.update(str(ip) for ip in network)
            except ValueError as e:
                error_messages.append(f"Error in line {line_number} of file '{file_path}': {e}")

    return ip_addresses, error_messages

def save_difference_to_file(file_path1, file_path2, ip_addresses1, ip_addresses2, report_folder):
    difference_file_path = os.path.join(report_folder, 'missing_ips_in_list2.txt')

    with open(difference_file_path, 'w') as difference_file:
        difference_set = ip_addresses2 - ip_addresses1
        difference_list = sorted(list(difference_set))
        difference_file.write('\n'.join(difference_list))

    return difference_file_path

def save_error_to_file(errors, report_folder):
    error_file_path = os.path.join(report_folder, 'extraction_errors.txt')

    with open(error_file_path, 'w') as error_file:
        error_file.write('\n'.join(errors))

    return error_file_path

def save_unique_to_reference(report_folder, unique_to_reference):
    unique_file_path = os.path.join(report_folder, 'unique_to_reference.txt')
    
    with open(unique_file_path, 'w') as unique_file:
        unique_list = sorted(list(unique_to_reference))
        unique_file.write('\n'.join(unique_list))

    return unique_file_path

def save_final_report(report_folder, file_path1, file_path2, ip_addresses1, ip_addresses2):
    final_report_file_path = os.path.join(report_folder, 'final_report.txt')

    with open(final_report_file_path, 'w') as final_report_file:
        final_report_file.write("Final Report:\n")
        final_report_file.write(f"Total IP addresses in {file_path1}: {len(ip_addresses1)}\n")
        final_report_file.write(f"Total IP addresses in {file_path2}: {len(ip_addresses2)}\n")
        final_report_file.write(f"Number of unique IP addresses in {file_path1}: {len(ip_addresses1)}\n")
        final_report_file.write(f"Number of unique IP addresses in {file_path2}: {len(ip_addresses2)}\n")
        final_report_file.write(f"Number of IP addresses unique to {file_path1}: {len(ip_addresses1 - ip_addresses2)}\n")
        final_report_file.write(f"Number of IP addresses unique to {file_path2}: {len(ip_addresses2 - ip_addresses1)}\n")

    return final_report_file_path

def save_overall_reports(report_folder, file_path1, file_path2, ip_addresses1, ip_addresses2, errors):
    overall_report_file_path = os.path.join(report_folder, 'overall_reports.txt')

    with open(overall_report_file_path, 'w') as overall_report_file:
        overall_report_file.write("Overall Reports:\n")
        overall_report_file.write(f"Total IP addresses in {file_path1}: {len(ip_addresses1)}\n")
        overall_report_file.write(f"Total IP addresses in {file_path2}: {len(ip_addresses2)}\n")
        overall_report_file.write(f"Number of IP addresses unique to {file_path1}: {len(ip_addresses1 - ip_addresses2)}\n")
        overall_report_file.write(f"Number of IP addresses unique to {file_path2}: {len(ip_addresses2 - ip_addresses1)}\n")
        overall_report_file.write("\nExtraction Errors:\n")
        overall_report_file.write('\n'.join(errors))

    return overall_report_file_path

def save_ips_unique_to_first(report_folder, ip_addresses1, ip_addresses2):
    unique_to_first_file_path = os.path.join(report_folder, 'unique_to_first.txt')

    with open(unique_to_first_file_path, 'w') as unique_to_first_file:
        unique_list = sorted(list(ip_addresses1 - ip_addresses2))
        unique_to_first_file.write('\n'.join(unique_list))

    return unique_to_first_file_path

def save_ips_unique_to_second(report_folder, ip_addresses1, ip_addresses2):
    unique_to_second_file_path = os.path.join(report_folder, 'unique_to_second.txt')

    with open(unique_to_second_file_path, 'w') as unique_to_second_file:
        unique_list = sorted(list(ip_addresses2 - ip_addresses1))
        unique_to_second_file.write('\n'.join(unique_list))

    return unique_to_second_file_path

def main():
    if len(sys.argv) < 3:
        logging.error("Usage: ./script.py iplist1.txt iplist2.txt")
        sys.exit(1)

    file_path1 = sys.argv[1]
    file_path2 = sys.argv[2]

    ip_addresses1, errors1 = get_ip_addresses_from_file(file_path1, reference=True)
    ip_addresses2, errors2 = get_ip_addresses_from_file(file_path2)

    report_folder_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(report_folder_name)

    logging.info(f"Extracting IP Addresses from {file_path1}")
    for ip in ip_addresses1:
        pass

    logging.info(f"Extracting IP Addresses from {file_path2}")
    for ip in ip_addresses2:
        pass

    logging.info(f"Saving difference to file")
    difference_file_path = save_difference_to_file(file_path1, file_path2, ip_addresses1, ip_addresses2, report_folder_name)

    logging.info(f"Saving error messages to file")
    error_file_path = save_error_to_file(errors1 + errors2, report_folder_name)

    unique_to_reference = ip_addresses1 - ip_addresses2
    
    logging.info(f"Saving IPs unique to reference to file")
    unique_file_path = save_unique_to_reference(report_folder_name, unique_to_reference)

    logging.info(f"Saving overall reports to file")
    overall_report_file_path = save_overall_reports(report_folder_name, file_path1, file_path2, ip_addresses1, ip_addresses2, errors1 + errors2)

    logging.info(f"Saving IPs unique to {file_path1} to file")
    unique_to_first_file_path = save_ips_unique_to_first(report_folder_name, ip_addresses1, ip_addresses2)

    logging.info(f"Saving IPs unique to {file_path2} to file")
    unique_to_second_file_path = save_ips_unique_to_second(report_folder_name, ip_addresses1, ip_addresses2)

    logging.info(f"\nReport files saved in folder '{report_folder_name}':")
    logging.info(f"- IPs unique to reference: {unique_file_path}")
    logging.info(f"- Missing IPs in {file_path2}: {difference_file_path}")
    logging.info(f"- Extraction errors: {error_file_path}")
    logging.info(f"- Overall Reports: {overall_report_file_path}")
    logging.info(f"- IPs unique to {file_path1}: {unique_to_first_file_path}")
    logging.info(f"- IPs unique to {file_path2}: {unique_to_second_file_path}")

    logging.info("\nProcessing completed. Report:")
    logging.info(f"Total IP addresses in {file_path1}: {len(ip_addresses1)}")
    logging.info(f"Total IP addresses in {file_path2}: {len(ip_addresses2)}")
    logging.info(f"Number of unique IP addresses in {file_path1}: {len(ip_addresses1)}")
    logging.info(f"Number of unique IP addresses in {file_path2}: {len(ip_addresses2)}")
    logging.info(f"Number of IP addresses unique to {file_path1}: {len(ip_addresses1 - ip_addresses2)}")
    logging.info(f"Number of IP addresses unique to {file_path2}: {len(ip_addresses2 - ip_addresses1)}")

if __name__ == "__main__":
    main()






