
class user_info:
    def __init__(self, user_info_dict: dict):
        try:
            self._name = user_info_dict["name"]
            self._email = user_info_dict["email"]
            self._contact_number = user_info_dict["contact_number"]

        except Exception as e:
            raise ValueError(f"invalid user_info dict, {str(e)}")
        
        self._linkedin_url = user_info_dict["linkedin url"]
        self._personal_url = user_info_dict["personal url"]

    def name(self) -> str:
        return self._name
    
    def email(self) -> str:
        return self._email
    
    def contact_number(self) -> str:
        return self._contact_number
    
    def linkedin_url(self) -> str | None:
        try:
            return self._linkedin_url
        except:
            return None
        
    def personal_url(self) -> str | None:
        try: 
            return self._personal_url
        except:
            return None
        
    def jsonify(self) -> dict:
        output = dict()
        output["name"] = self.name()
        output["email"] = self.email()
        output["linkedin url"] = self.linkedin_url()
        output["personal url"] = self.personal_url()
        output["contact_number"] = self.contact_number()
        return output

class education:
    def __init__(self, education_dict: dict, university_name: str):
        try:
            if not "location (city/country)" in education_dict:
                education_dict["location (city/country)"] = None 
            self._location = education_dict["location (city/country)"]
            if not "degree" in education_dict:
                education_dict["degree"] = None 
            self._degree = education_dict["degree"]
            if not "year status" in education_dict:
                education_dict["year status"] = None 
            self._year_status = education_dict["year status"]
            if not "expected graduation" in education_dict:
                education_dict["expected graduation"] = None 
            self._expected_graduation = education_dict["expected graduation"]
            self._university = university_name

        except Exception as e:
            raise ValueError(f"invalid education dict, {str(e)}")
        
        try:
            self._gpa = education_dict["gpa"]
        except:
            pass

    def location(self) -> str:
        return self._location
    
    def degree(self) -> str:
        return self._degree
    
    def year_status(self) -> str:
        return self._year_status
    
    def expected_graduation(self) -> str:
        return self._expected_graduation
    
    def university(self) -> str:
        return self._university
    
    def latex_university(self) -> str:
        lst = self.university().split('!]?.')
        return lst[-1]
    
    def gpa(self) -> str:
        try:
            return self._gpa
        except:
            None
    
    def jsonify(self) -> dict:
        output = dict()
        output["location (city/country)"] = self.location()
        output["degree"] = self.degree()
        output["year status"] = self.year_status()
        output["expected graudation"] = self.expected_graduation()
        try:
            output["gpa"] = self.gpa()
        except:
            pass
        return output

class skills:
    def __init__(self, skills_list: list, skill_category: str):
        try:
            self._skill_category = skill_category
            self._skills_list = skills_list
        except Exception as e:
            raise ValueError(f"invalid skills input, {str(e)}")
        
    def skill_category(self) -> str:
        return self._skill_category
    
    def latex_skill_category(self) -> str:
        lst = self.skill_category().split('!]?.')
        return lst[-1]
    
    def skills_list(self) -> list:
        return self._skills_list
    
    def jsonify(self):
        return self.skills_list()

class perspective:
    def __init__(self, perspective_name: str, perspective_bullets: list[str]):
        try:
            self._perspective_name = perspective_name
            self._perspective_bullets = perspective_bullets

        except Exception as e:
            raise ValueError(f"Invalid perspective")
    
    def perspective_name(self) -> str:
        return self._perspective_name
    
    def perspective_bullets(self) -> list[str]:
        return self._perspective_bullets

class experiences:
    def __init__(self, experience_dict: dict, job_title: str):
        try:
            self._job_title = job_title
            if not "company" in experience_dict:
                experience_dict["company"] = None
            self._company = experience_dict["company"]
            if not "job dates" in experience_dict:
                experience_dict["job dates"] = None
            self._job_dates = experience_dict["job dates"]
            self._perspectives = [perspective(perspective_name, perspective_bullets) \
                                  for perspective_name, perspective_bullets \
                                    in experience_dict["perspectives"].items()]

        except Exception as e:
            raise ValueError(f"Invalid experience dict, {str(e)}")
        
    def job_title(self) -> str:
        return self._job_title
    
    def company(self) -> str:
        return self._company
    
    def job_dates(self) -> str:
        return self._job_dates
    
    def perspectives(self) -> list[str]:
        return self._perspectives
    
    def jsonify(self) -> dict:
        output = dict()
        output["company"] = self.company()
        output["job_dates"] = self.job_dates()
        output["perspectives"] = {x.perspective_name(): x.perspective_bullets() for x in self.perspectives()}

        return output

class awards:
    def __init__(self, award_dict: dict, award_title: str):
        try:
            self._award_title = award_title
            if not "company" in award_dict:
                award_dict["company"] = None
            self._institution = award_dict["institution"]
            if not "company" in award_dict:
                award_dict["company"] = None
            self._award_date = award_dict["award date"]
            self._award_description = award_dict["award description"]
        except Exception as e:
            raise ValueError(f"invalid awards dict, {str(e)}")
        
    def award_title(self) -> str:
        return self._award_title

    def institution(self) -> str:
        return self._institution
    
    def award_date(self) -> str:
        return self._award_date
    
    def award_description(self) -> str:
        return self._award_description
    
    def jsonify(self) -> dict:
        output = dict()
        output["institution"] = self.institution()
        output["award date"] = self.award_date()
        output["award description"] = self.award_description()
        return output

class history:
    def __init__(self, history_raw_dict: dict):
        if 'user info' in history_raw_dict:
            self._user_info = user_info(history_raw_dict["user info"])
        else:
            self._user_info = None
        self._education = [education(education_dict, institution) \
                            for institution, education_dict in \
                            history_raw_dict["education"].items()]
        self._technical_skills = [skills(skills_list, skill_category) \
                                    for skill_category, skills_list in \
                                    history_raw_dict["technical skills"].items()]
        self._experiences = [experiences(experience_dict, job_title) \
                                    for job_title, experience_dict in \
                                    history_raw_dict["experiences"].items()]
        if not 'awards' in history_raw_dict:
            history_raw_dict['awards'] = {}
        self._awards = [awards(award_dict, award_title) \
                    for award_title, award_dict in \
                        history_raw_dict["awards"].items()]
        
    def education(self) -> list[education]:
        return self._education
    
    def user_info(self) -> user_info:
        return self._user_info

    def technical_skills(self) -> list[skills]:
        return self._technical_skills

    def experiences(self) -> list[experiences]:
        return self._experiences        
    
    def awards(self) -> list[awards]:
        return self._awards
    
    def merge_histories(self, merging_history: 'history') -> None:
        """
        Merges the two histories, adding arcs if they do not exist in the original history,
        or just their perspectives to the existing arcs.
        """
        new_history_json = self.jsonify()
        merging_history_json = merging_history.jsonify()

        for merge_education in merging_history_json['education']:
            count = 1

            if merge_education in new_history_json['education']:
                while f'school-{count}!]?.{merge_education}' in new_history_json['education']:
                    if merging_history_json['education']['degree'] == new_history_json['education']['degree']:
                        break

                    count += 1
                                
            new_history_json['education'][f'school-{count}!]?.{merge_education}'] = merging_history_json['education'][merge_education]

        for merge_skill in merging_history_json['technical skills']:
            count = 1

            if merge_skill in new_history_json['technical skills']:
                while f'skill-{count}!]?.{merge_skill}' in new_history_json['technical skills']:
                    count += 1
                                
            new_history_json['technical skills'][f'skill-{count}]!]?.{merge_skill}'] = merging_history_json['technical skills'][merge_skill]

        for merge_arc in merging_history_json['experiences']:
            if not merge_arc in new_history_json['experiences']:
                new_history_json['experiences'][merge_arc] = merging_history_json['experiences'][merge_arc]
                continue

            for perspective in merging_history_json['experiences'][merge_arc]['perspectives']:                  
                new_history_json['experiences'][merge_arc]['perspectives'][merge_arc + perspective] = merging_history_json['experiences'][merge_arc]['perspectives'][perspective]

        for merge_award in merging_history_json['awards']:
            new_history_json['awards'][merge_award] = merging_history_json['awards'][merge_award]
        
        self.__init__(new_history_json)


    def jsonify(self) -> dict:
        output = dict()
        try:
            output["user info"] = self.user_info().jsonify()
        except:
            output["user info"] = {}
        try:
            output["education"] = {x.university(): x.jsonify() for x in self.education()}
        except:
            output["education"] = {}

        try:
            output["technical skills"] = {x.skill_category(): x.jsonify() for x in self.technical_skills()}
        except:
            output["technical skills"] = {}

        try:
            output["experiences"] = {x.job_title(): x.jsonify() for x in self.experiences()}
        except:
            output["experiences"] = {}

        try:
            output["awards"] = {x.award_title(): x.jsonify() for x in self.awards()}
        except:
            output["awards"] = {}

        return output