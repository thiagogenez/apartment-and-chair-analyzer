# Apartment and Chair Analyzer

The Apartment and Chair Analyzer is a command-line tool tailored for Apartment And Chair Delivery Limited, addressing the challenge of manually counting chair types specified in buyers' floor plans. The company's growth and reliance on outdated systems have made this process error-prone, affecting customer satisfaction. This tool automates chair counting and categorization from floor plans, enhancing accuracy and efficiency in furniture planning and delivery.

## Background

Apartment And Chair Delivery Limited specializes in constructing and furnishing residential buildings. Home buyers specify chair placements on floor plans, which have historically been counted manually. This outdated process, compounded by the company's legacy systems from the eighties, has led to inaccuracies and customer dissatisfaction. This tool brings a much-needed solution, automating the extraction and counting of chair types from these floor plans.



## Features

- **Automated Analysis**: Parses floor plans to identify and count chair types accurately.
- **Detailed Output**: Provides both the total number of different chair types required for an apartment and the counts per room.
- **Legacy System Compatibility**: Designed for ease of use with outdated systems through a command-line interface.

## Solution

The Apartment and Chair Analyzer employs the _Breadth-First Search (BFS) algorithm_, viewing the floor plans as matrices to systematically and accurately identify the positions of chairs specified by home buyers. It adeptly navigates through these matrix-represented floor plans, allowing for precise room-by-room exploration and the enumeration of Wooden (W), Plastic (P), Sofa (S), and China (C) chairs. This approach ensures the generation of detailed chair counts tailored to each apartment's layout, with outputs formatted for seamless integration with legacy systems. This strategy not only meets but exceeds the company's needs for a comprehensive and error-free analysis of chair placements within their construction projects.

## Assumptions

For the Analyzer to function correctly and efficiently using the BFS algorithm, it operates under a set of predefined assumptions about the format and representation of the floor plans:

- **Floor Plan:** The legacy floor plan is given as an ASCII file.

- **Wall Representation**: The walls within the floor plans are denoted by a specific set of characters: ``{"+", "-", "|", "/", "\\"}``. These characters are crucial for the algorithm to identify the boundaries of each room and navigate the matrix accurately.

- **Room Labeling**: Room labels in floor plans are strictly defined to be enclosed in parentheses `(a-Z)`, with `a-Z` denoting the alphanumeric room name. This precise convention is critical for the algorithm to identify and classify rooms accurately within the apartment, ensuring exact chair counts for each area. Labels are meticulously placed within the room's boundaries, avoiding any extension beyond or overlap with walls, which is essential for the algorithm's correct room recognition and subsequent chair count accuracy.

## Installation

Ensure Python 3.10 is installed on your system. Follow the steps below to set up the tool:

```bash
git clone https://github.com/thiagogenez/apartment-and-chair-analyzer.git
cd apartment-and-chair-analyzer
python -m venv venv
source venv/bin/activate  # On macOS and Linux
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

## Execution
To analyze a floor plan, run the tool with the path to the floor plan file:


```bash
python process_floor_plan.py /path/to/floor_plan.txt
```

## Example

Given a floor plan indicating the desired positions of different chair types (W for wooden chair, P for plastic chair, S for sofa chair, C for china chair), the tool outputs the count of each chair type both for the entire apartment and per room, sorted alphabetically by room names:

File `example_floor_plan.txt`
```text
+-----------+------------------------------------+
|           |                                    |
| (closet)  |                                    |
|         P |                            S       |
|         P |         (sleeping room)            |
|         P |                                    |
|           |                                    |
+-----------+    W                               |
|           |                                    |
|        W  |                                    |
|           |                                    |
|           +--------------+---------------------+
|                          |                     |
|                          |                W W  |
|                          |    (office)         |
|                          |                     |
+--------------+           |                     |
|              |           |                     |
| (toilet)     |           |             P       |
|   C          |           |                     |
|              |           |                     |
+--------------+           +---------------------+
|              |           |                     |
|              |           |                     |
|              |           |                     |
| (bathroom)   |           |      (kitchen)      |
|              |           |                     |
|              |           |      W   W          |
|              |           |      W   W          |
|       P      +           |                     |
|             /            +---------------------+
|            /                                   |
|           /                                    |
|          /                          W    W   W |
+---------+                                      |
|                                                |
| S                                   W    W   W |
|                (living room)                   |
| S                                              |
|                                                |
|                                                |
|                                                |
|                                                |
+--------------------------+---------------------+
                           |                     |
                           |                  P  |
                           |  (balcony)          |
                           |                 P   |
                           |                     |
                           +---------------------+
```

Call the `process_floor_plan`
```bash
python process_floor_plan.py example_floor_plan.txt
```

Output
```
total:
W: 14, S: 3, P: 7, C: 1
balcony:
W: 0, S: 0, P: 2, C: 0
bathroom:
W: 0, S: 0, P: 1, C: 0
closet:
W: 0, S: 0, P: 3, C: 0
kitchen:
W: 4, S: 0, P: 0, C: 0
living room:
W: 7, S: 2, P: 0, C: 0
office:
W: 2, S: 0, P: 1, C: 0
sleeping room:
W: 1, S: 1, P: 0, C: 0
toilet:
W: 0, S: 0, P: 0, C: 1
```


## Summary

The Apartment and Chair Analyzer offers a comprehensive solution for Apartment And Chair Delivery Limited's challenge of accurately counting and categorizing chair types from floor plans. By leveraging Breadth-First Search (BFS) algorithms and precise room labeling conventions, the tool ensures precise identification and counting of chair types, significantly improving operational efficiency and customer satisfaction.
