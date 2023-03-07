import pandas as pd

def calc(d):

    del d['Hour 0']
    del d['Hour 11']

    d = d.set_index('Date')

    pres = 0
    abse = 0
    un = 0
    od = 0
    ml = 0
    tot = 0
    for i in d.columns:
        temp = 0
        
        try:
            temp = d[i].value_counts()['P']
        except: 
            temp = 0
            
        pres += temp
        tot += temp
        
        try:
            temp = d[i].value_counts()['A']
        except: 
            temp = 0
            
        abse += temp
        tot += temp

        try:
            temp = d[i].value_counts()['U']
        except: 
            temp = 0
        
        tot += temp
        un += temp
        
        try:
            temp = d[i].value_counts()['O']
        except: 
            temp = 0
        
        od += temp
        tot += temp

        try:
            temp = d[i].value_counts()['M']
        except: 
            temp = 0
        
        ml += temp
        tot += temp

    
    assembly = {'Present': 0,
                'Absent': 0, 
                'Unmarked': 0}

    for i in d['Assembly']:
        if i == "P" or i == "O" or i == "M":
            assembly['Present'] += 1
        elif i == 'A':
            assembly['Absent'] += 1
        elif i == 'U':
            assembly['Unmarked'] += 1

    unmarked_dates = {}

    df = d.transpose()
    df.fillna(0)
    cols = d.columns

    for i in df:
        unmarked_dates[i] = []

    for i in df:
        temp = []
        
        for j in df[i]:
            temp.append(j)
        
        for j in range(len(temp)):
            if temp[j] == 'U':
                unmarked_dates[i].append(cols[j])

    unmarked_dates = {k: v for k, v in unmarked_dates.items() if v}

    results = {"Present": pres,
               "Absent": abse,
               "Unmarked": un,
               "On Duty": od,
               "Medical Leave": ml,
               "Total": tot,
               "Assemblies Present":assembly['Present'],
               "Assemblies Absent":assembly['Absent'],
               "Total Assembies":(assembly['Present']+assembly['Absent']),
               "Physical Attendance": round((((pres)/tot)*100),2),
               "Attendance (Unmarked and Absent)": round((100-(((abse+un)/tot) * 100)),2),
               "Attendance (Only Absent)":round((100-((abse/tot) * 100)),2),
               "Attendance (Without Unmarked)":round((100-((abse/(tot-un)) * 100)),2),
               "Assembly Attendance": round((assembly['Present']/(assembly['Present'] + assembly['Absent'] + assembly['Unmarked'])) * 100,2),
               "Final Attendance":round((((pres+od+ml)/tot) * 100),2)
               }
    

    return results, unmarked_dates
