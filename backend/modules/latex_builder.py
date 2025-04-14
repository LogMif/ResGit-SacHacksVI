import os
import subprocess
import history_class


def _get_contact_information(user_info: history_class.user_info) -> str:
    """adds contact information"""
    name = "Kierann"
    linkedin_url = "https://www.linkedin.com/in/kierann-chong"
    email = "kierann.schong@gmail.com"
    website_url = "https://green-kiwie.github.io/Kierann\_Resume.github.io"
    contact_number = "(949) 822-4004"

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

def _get_education(educations: list[history_class.education]) -> str:
    output =  f"""
        \\begin{{description}}"""
    
    for education in educations:
        output += f"""
        \\item \\ressubheading{{{education.latex_university()}}}{{{education.location()}}}{{{education.degree()}, {education.year_status()}, GPA: {education.gpa()}}}{{Expected graduation: {education.expected_graduation()}}}
        """
    
    output += f"""\\end{{description}}"""

    return output

def _get_technical_skills(skills: list[history_class.skills]) -> str:
    output = f"""
        \\vspace{{-1pt}}
        \\resheading{{Technical Skills}}
        \\vspace{{-12pt}}

        \\begin{{description}}
        \\itemsep0em """
    
    for skill in skills:
        output += f"""\\resitem{{\\textbf{{{skill.latex_skill_category()}}}}}{', '.join(skill.skills_list())}"""


    output += f"""\\end{{description}}"""

    return output

def _get_work_experience(work_experiences: list[history_class.experiences]) -> str:
    output = f"""
        \\vspace{{-5pt}}
        \\resheading{{Internships}}
        \\vspace{{-7pt}}
        
        \\begin{{description}}
        """
    
    for experience in work_experiences:
        output += f"""
            \\item \\singlesubheading{{\\textbf{{{experience.job_title()}}} \\textbar  \\textit{{{experience.company()}}}}}{{}}{{{experience.job_dates()}}}
                        \\begin{{itemize}}
                            {"".join([f"\\resitem{{{bullet}}}" for perspective in experience.perspectives() for bullet in perspective.perspective_bullets()])}
                        \\end{{itemize}}
            """

    output += f"""\\end{{description}}"""
    return output

def _get_awards(awards: list[history_class.awards]) -> str:
    output = f"""
    \\vspace{{-5pt}}
    \\resheading{{Awards}}
    \\vspace{{-7pt}}

    \\begin{{description}}
    """

    for award in awards:
        
        output += f"""
            \\item \\singlesubheading{{\\textbf{{{award.award_title()}}} \\textbar \\textit{{{award.institution()}}}}}{{}}{{{award.award_date()}}}
            \\begin{{itemize}}
            {"".join([f"\\resitem{{{item}}}" for item in award.award_description()])}
            \\end{{itemize}}
            """
        
    output += f"""\\end{{description}}"""
    return output

def _compile_latex(latex_code: str) -> None:
    latex_filename = "resume.tex"
    with open(latex_filename, "w", encoding="utf-8") as f:
        f.write(latex_code)

    subprocess.run(["pdflatex", "-interaction=nonstopmode", latex_filename])

def _generate_resume(history: history_class.history) -> None:
    """generates all resumes"""
    latex_code = ""
    latex_code += _get_preamble() 
    latex_code += _get_contact_information(history.user_info())
    latex_code += _get_education(history.education())
    latex_code += _get_technical_skills(history.technical_skills())
    latex_code += _get_work_experience(history.experiences())
    latex_code += _get_awards(history.awards())

    latex_code += _get_postamble()
    _compile_latex(latex_code)

def _remove_latex_files() -> None:
    files_to_delete = ["resume.tex", "resume.aux", "resume.fdb_latexmk", "resume.fls", "resume.log", "resume.out"]
    
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)

def get_resume(history: history_class.history) -> bytes:
    _generate_resume(history)

    with open("resume.pdf", "rb") as pdf_file:
        binary_data = pdf_file.read()

    _remove_latex_files()
    return binary_data


if __name__ == "__main__":
    history_template = {
    "user_info":{

    },
    "education": {
        "UC I": {
            "location (city/country)": "US",
            "degree": "BSc in stupidify",
            "year status": "freshjuice",
            "expected graduation": "June 2020"
        }
    },
    "technical skills": {
        "interpersonal": ["kindness", "empathetic", "pathetic"],
        "hard skills": ["excel", "powerpoint"]
    },
    "experiences": {
        "microsfot server": {
            "company": "microsoft",
            "job dates": "insert fake dates here",
            "perspectives": {
                "my first idea": ["hehe", "haha"],
                "second idea": ["sad", "sadly"]
            }
        },
        "google clown": {
            "company": "clown inc",
            "job dates": "whoop",
            "perspectives": {
                "happy": ["hah", "hoho"],
                "sad": ["womp womp", "woomp"]
            }
        }
    },
    "awards": {
        "best person award": {
            "institution": "white house",
            "award date": "2003",
            "award description": ["Voted most loved person ever"]
        },
        "stupidest person award": {
            "institution": "fund house",
            "award date": "2100",
            "award description": ["lost the company 10 trillion"]
        }
    }
};

    get_resume(history_class.history(history_template))
    # print(history1.jsonify())




