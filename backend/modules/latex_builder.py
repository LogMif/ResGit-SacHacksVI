import os
import subprocess

def _get_contact_information() -> str:
    """adds contact information"""
    name = "Kierann"
    linkedin_url = "https://www.linkedin.com/in/kierann-chong"
    email = "kierann.schong@gmail.com"
    website_url = "https://green-kiwie.github.io/Kierann\_Resume.github.io"
    contact_number = "(949) 822-5054"

    output = f"""
        \\begin{{tabular*}}{{7in}}{{l@{{\\extracolsep{{\\fill}}}}r}}
        \\textbf{{\\Large {name}}}  \\\\
        \\href{{{linkedin_url}}}{{{linkedin_url}}} & {email} \\\\
        \\href{{{website_url}}}{{{website_url}}} & {contact_number} \\\\
        \\end{{tabular*}}
        \\vspace{{-5pt}}
        """
    
    return output

def _get_preamble() -> str:
    """returns preamble"""
    return r"""
        \documentclass[letterpaper,10pt]{article}
        \newlength{\outerbordwidth}
        \pagestyle{empty}
        \raggedbottom
        \raggedright
        \usepackage[svgnames]{xcolor}
        \usepackage{framed}
        \usepackage{tocloft}
        \usepackage{etoolbox}
        \robustify\cftdotfill
        \usepackage[colorlinks=true, urlcolor=blue, linkcolor=red]{hyperref}
        \usepackage{enumitem}
        \usepackage{array}
        
        \setlength{\outerbordwidth}{3pt}  
        \definecolor{shadecolor}{gray}{0.75}
        \definecolor{shadecolorB}{gray}{0.93}

        \setlength{\evensidemargin}{-0.25in}
        \setlength{\headheight}{0in}
        \setlength{\headsep}{0in}
        \setlength{\oddsidemargin}{-0.25in}
        \setlength{\paperheight}{11in}
        \setlength{\paperwidth}{8.5in}
        \setlength{\tabcolsep}{0in}
        \setlength{\textheight}{9.5in}
        \setlength{\textwidth}{7in}
        \setlength{\topmargin}{-0.3in}
        \setlength{\topskip}{0in}
        \setlength{\voffset}{0.1in}

        \newcommand{\resitem}[1]{\item #1 \vspace{-3pt}}
        \newcommand{\resheading}[1]{%
        \vspace{7pt} 
        \noindent\underline{\textbf{\sffamily{\large #1}}}%
        \vspace{3pt}
        }

        \newcommand{\ressubheading}[4]{
        \begin{tabular*}{6.9in}{l@{\cftdotfill{\cftsecdotsep}\extracolsep{\fill}}r}
                \textbf{#1} & #2 \\
                \textit{#3} & #4 \\
        \end{tabular*}\vspace{-8pt}}

        \newcommand{\singlesubheading}[3]{ 
        \begin{tabular*}{6.9in}{@{\extracolsep{\fill}}l l r} 
            #1 & \textit{#2} & {#3} 
        \end{tabular*}\vspace{-8pt} 
        }

        \begin{document}
        """

def _get_postamble() -> str:
    return r"""
        \end{document}
        """

def _get_education() -> str:
    university_name = "University of California, Irvine"
    location = "California"
    degree = "BSc in Computer Science"
    year_status = "Sophomore"
    gpa = "3.92"
    graduation_date = "May 2027"

    return f"""
        \\begin{{description}}

        \\item \\ressubheading{{{university_name}}}{{{location}}}{{{degree}, {year_status}, GPA: {gpa}}}{{Expected graduation: {graduation_date}}}

        \\end{{description}}
        """

def _get_technical_skills() -> str:
    coursework = "Supervised Machine Learning, Advanced Learning Algorithms (DeepLearning.AI)"
    languages = ["Python", "Pandas", "Tensorflow", "Gensim", "LangChain", "Yfinance", "Huggingface", "C++", "SQL", "HTML"]
    ml_algorithms = "Classification, Neural Networks, Text Embedding, Clustering"
    tools = ["AWS (Bedrock, Glue, Lambda, DynamoDB, S3 Bucket)", "Sharepoint", "PowerApps", "Git"]

    return f"""
        \\vspace{{-1pt}}
        \\resheading{{Technical Skills}}
        \\vspace{{-12pt}}

        \\begin{{description}}
        \\itemsep0em 
            \\resitem{{\\textbf{{Coursework: }}}}{coursework}
            \\resitem{{\\textbf{{Languages: }}}}{{{', '.join(languages)}}}
            \\resitem{{\\textbf{{Machine Learning Algorithms: }}}}{ml_algorithms}
            \\resitem{{\\textbf{{Tools: }}}}{{{', '.join(tools)}}}
        \\end{{description}}
        """

def _get_work_experience() -> str:
    internship_1_title = "Chatbot Developer Intern"
    internship_1_company = "RenalWorks Pte Ltd, Malaysia"
    internship_1_dates = "July 2024-September 2024"
    internship_1_responsibilities = [
        "Collaborated to develop a Claude 3 chatbot with SQL data retrieval and token tracking with LangGraph API, AWS DynamoDB and AWS Bedrock.",
        "Innovatively optimized SQL query process for 500\% less token usage, enabled SQL function"
    ]

    internship_2_title = "Data Scientist Intern"
    internship_2_company = "Ascentis CRM, Singapore"
    internship_2_dates = "February 2024-July 2024"
    internship_2_responsibilities = [
        "Analyzed, prepared, researched and trained a text-based classification algorithm on 2 million data entries using AWS Glue and S3 Bucket.",
        "Solved the optimization problem for algorithm to process 7 million data entries in 15 minutes with 80\% accuracy."
    ]

    internship_3_title = "Physics Tutor"
    internship_3_company = "Kaizen Learning, Singapore"
    internship_3_dates = "January 2024-August 2024"
    internship_3_responsibilities = [
        "Topped school in Physics HL: 92\%, International Baccalaureate Score: 44/45.",
        "Delivered individualized tuition to 3 students, totaling 6 hours a week.",
        "Catalyzed students' improvement from 8\% to 50\% in 2 months."
    ]

    internship_4_title = "Platoon Sergeant"
    internship_4_company = "Singapore Armed Forces, Singapore"
    internship_4_dates = "January 2022-November 2023"
    internship_4_responsibilities = [
        "Accomplished the Guards Conversion Course as one of the top 5 graduates. Promoted to 2nd Sergeant.",
        "Motivated, led, and trained a platoon of 20 in the elite rapid deployment infantry formation (guards).",
        "Spearheaded the revamp of a 300-page knowledge base. Conferred the title: Subject Matter Expert."
    ]

    internship_5_title = "Research Attachment"
    internship_5_company = "Defence Science Organization, Singapore"
    internship_5_dates = "October 2021-January 2022"
    internship_5_responsibilities = [
        "Spearheaded the comparison of two approaches to break quantum computer-resistant Lattice-based cryptography.",
        "Achieved finalist in the Singapore Science and Engineering Fair (SSEF) with research paper."
    ]



    work_experiences = [[internship_1_title, internship_1_company, internship_1_dates, internship_1_responsibilities], 
                        [internship_2_title, internship_2_company, internship_2_dates, internship_2_responsibilities],
                        [internship_3_title, internship_3_company, internship_3_dates, internship_3_responsibilities],
                        [internship_4_title, internship_4_company, internship_4_dates, internship_4_responsibilities],
                        [internship_5_title, internship_5_company, internship_5_dates, internship_5_responsibilities]]


    output = f"""
        \\vspace{{-5pt}}
        \\resheading{{Internships}}
        \\vspace{{-7pt}}
        
        \\begin{{description}}
        """
    
    for experience in work_experiences:
        output += f"""
            \\item \\singlesubheading{{\\textbf{{{experience[0]}}} \\textbar  \\textit{{{experience[1]}}}}}{{}}{{{experience[2]}}}
                        \\begin{{itemize}}
                            {"".join([f"\\resitem{{{item}}}" for item in experience[3]])}
                        \\end{{itemize}}
            """

    output += f"""\\end{{description}}"""
    return output

def _get_awards() -> str:
    award_1_title = "Undergraduate Research Fellow"
    award_1_institution = "UC Irvine, California"
    award_1_dates = "2024-2025"
    award_1_responsibilities = [
        "Awarded for research on the statistical distribution of distant galaxies to analyze the young universe."
    ]

    award_2_title = "Undergraduate Research Fellow"
    award_2_institution = "UC Irvine, California"
    award_2_dates = "2024-2025"
    award_2_responsibilities = [
        "Awarded for research on item classification algorithm based on text-embedding (natural language processing)."
    ]

    awards = [[award_1_title, award_1_institution, award_1_dates, award_1_responsibilities],
              [award_2_title, award_2_institution, award_2_dates, award_2_responsibilities]]

    output = f"""
    \\vspace{{-5pt}}
    \\resheading{{Awards}}
    \\vspace{{-7pt}}

    \\begin{{description}}
    """

    for award in awards:
        output += f"""
            \\item \\singlesubheading{{\\textbf{{{award_1_title}}} \\textbar \\textit{{{award_1_institution}}}}}{{}}{{{award_1_dates}}}
            \\begin{{itemize}}
            {"".join([f"\\resitem{{{item}}}" for item in award_1_responsibilities])}
            \\end{{itemize}}
            """
        
    output += f"""\\end{{description}}"""
    return output

def _compile_latex(latex_code: str) -> None:
    latex_filename = "resume.tex"
    with open(latex_filename, "w", encoding="utf-8") as f:
        f.write(latex_code)

    subprocess.run(["pdflatex", "-interaction=nonstopmode", latex_filename])

print("PDF compilation completed!")


def _generate_resume() -> None:
    """generates all resumes"""
    latex_code = ""
    latex_code += _get_preamble() 
    latex_code += _get_contact_information()
    latex_code += _get_education()
    latex_code += _get_technical_skills()
    latex_code += _get_work_experience()
    latex_code += _get_awards()

    latex_code += _get_postamble()
    _compile_latex(latex_code)

def _remove_latex_files() -> None:
    files_to_delete = ["resume.tex", "resume.aux", "resume.fdb_latexmk", "resume.fls", "resume.log", "resume.out"]
    
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)

def get_resume() -> bytes:
    _generate_resume()

    with open("resume.pdf", "rb") as pdf_file:
        binary_data = pdf_file.read()

    _remove_latex_files()
    return binary_data


if __name__ == "__main__":
    get_resume()