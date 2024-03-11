# IP Address Examiner

## Overview

This Python script easily compares two lists of IP addresses from two files, letting you choose a reference. It helps identify differences.

## How to Use

1. **Installation:**
   - Clone the repository to your local machine:

     ```bash

     git clone https://github.com/darrenoshan/compare_iplist.git
     cd compare_iplist

     ```
2. **Dependencies:**
   - Install the required dependencies:

    git
    python3

      **Ubuntu/Debian:**

        ```bash
        apt-get update ; apt-get install python3 git -y
        ```

      **Fedora Linux/Rocky Linux:**

        ```bash
          dnf install python3 git -y
        ```


3. **Usage:**
   - Execute the script, providing the file paths for the two lists of IP addresses:

     ```bash
        git clone https://github.com/darrenoshan/compare_iplist.git
        cd compare_iplist

     ```


## Example

      ```bash
        ./cmd.py  sample_refrence_ip_list.txt sample_ip_list.txt

      ```
 Replace `01_sample_refrence_ip_list.txt` and `02_sample_ip_list.txt` with the actual file paths.