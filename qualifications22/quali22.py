class Project():
    def __init__(self, name : str, days_to_complete : int, score_awarded : int, best_before : int, number_of_roles : int, skills):
        self.name = name
        self.days_to_complete = int(days_to_complete)
        self.score_awarded = int(score_awarded)
        self.best_before = int(best_before)
        self.number_of_roles = int(number_of_roles)
        self.skills = skills
        self.members = []
        self.is_full = False

    def get_skill(self, skill_name):
        return [skill for skill in self.skills if skill.name == skill_name][0]

class Contributor():
    def __init__(self, name : str, skills):
        self.name = name
        self.skills = skills
        self.is_mentor = False
        if len([skill for skill in skills if int(skill.level) > 0]) > 0:
            self.can_mentor = True
        else:
            self.can_mentor = False
        self.mentorable_skills = []
        self.is_available = True
        self.being_mentored = False

    def has_skill(self, skill_name):
        return len([skill for skill in self.skills if skill.name == skill_name]) > 0

    def get_skill(self, skill_name):
        return [skill for skill in self.skills if skill.name == skill_name][0]

    def can_mentor(self, potential_student, skills_needed):
        # returns true if the potential_student
        # can be mentored by self
        valid_skills = 0
        for skill_needed in skills_needed:
            if self.has_skill(skill_needed.name):
                if self.get_skill(skill_needed.name).level > potential_student.get_skill(skill_needed.name).level:
                    valid_skills += 1
        return valid_skills == len(skills_needed)


    def valid_skills(self, required_skills):
        # returns the skills that the contributor is valid
        matching_skills = []
        for required_skill in required_skills:
            new_matching_skills = [
                skill for skill in self.skills
                if required_skill.name == skill.name
                and skill.level >= required_skill.level
            ]
            for matching_skill in new_matching_skills:
                if matching_skill not in matching_skills:
                    matching_skills.append(matching_skill)
        return matching_skills


class Skill():
    def __init__(self, name : str, level : int):
        self.name = name
        self.level = level

def import_from_file(filename):
    # oh dear god this entire function needs cleaning up
    # please help me oh
    lines = [line for line in open(filename)]
    first_line = lines[0].replace("\n", "").split(" ")
    num_contributors = int(first_line[0])
    projects = first_line[1]
    lines.pop(0)
    print(f"number of contributors: {num_contributors}")
    print(f"number of projects: {projects}")

    projects = []
    contributors = []
    current_contributor_skills = []
    current_project_skills = []

    contributer_count = 0
    line_num = 0
    looking_at_contributors = True
    at_end_of_contributor = False
    for line in lines:
        line = line.replace("\n", "")
        if looking_at_contributors:
            if line_num == 0:
                name = line.split(" ")[0]
                number_of_skills = int(line.split(" ")[1])
                #print("\n")
                #print(f"Name: {name}, num skills: {number_of_skills}")
                contributer_count += 1
            else:
                skill = line.split(" ")[0]
                skill_level = line.split(" ")[1]
                current_contributor_skills.append(Skill(skill, skill_level))
                #print(f"Skill: {skill}, skill level: {skill_level}")
            line_num += 1
            if line_num > number_of_skills:
                line_num = 0
                at_end_of_contributor = True
                contributors.append(Contributor(name, current_contributor_skills))
                current_contributor_skills = []
            else:
                at_end_of_contributor = False
            
        else:
            #print("No longer as contributor!")
            if line_num == 0:
                line_as_list = line.split(" ")
                #print(line_as_list)
                name = line_as_list[0]
                days_to_complete = line_as_list[1]
                score_awarded = line_as_list[2]
                best_before = line_as_list[3]
                number_of_roles = line_as_list[4]
            else:
                current_project_skills.append(Skill(line.split(" ")[0], line.split(" ")[1]))
            line_num += 1
            if line_num > int(number_of_roles):
                projects.append(Project(name,days_to_complete, score_awarded, best_before, number_of_roles, current_project_skills))
                current_project_skills = []
                line_num = 0

        # now on the projects
        if looking_at_contributors and at_end_of_contributor and contributer_count == num_contributors:
            line_num = 0
            looking_at_contributors = False

    return projects, contributors


def run_project(project : Project):
    print([member.name for member in project.members])
    mentor_exists = False   
    for person in project.members:
        if person.is_mentor == True:
            print(person)
            mentor_exists = True
            break

    for person in project.members:
        if mentor_exists == True and person.is_mentor == False:
            print(person)
            person.skill.level +=1


def assign_contributors_to_projects(contributors, projects):
    for contributor in contributors:
        print([(skill.name, skill.level) for skill in contributor.skills])
    #1-days to complete, 2-score awarded, 3-best before days, 4-num roles
    recheck_projects = []
    for project in projects:
        for contributor in contributors:
            # returns skills that person can mentor
            matching_skills = contributor.valid_skills(project.skills)
            # if has at least one required skill.
            if (
                len(matching_skills) > 0
                and project.is_full == False
                and contributor.is_available == True
                ): #cum on ken ;D
                project.members.append(contributor)
                if project.number_of_roles <= len(project.members):
                    project.is_full == True
            # if contributor needs to be mentored
            #elif (contributor.skill.level - project.skill.level == -1):
            elif [
                matching_skill
                for matching_skill in matching_skills
                if matching_skill.level == project.get_skill(matching_skill.name).level-1
                ]:
                print("finding someone to mentor them")
                # find someone to mentor them
                mentor_found = False
                # check for existing member in team
                for member in project.members:
                    if member.can_mentor == True:
                        member.is_mentor = True
                        mentor_found == True
                # if no member in team, check all possible contributors
                if mentor_found == False:
                    for person in contributor:
                        if contributor.skill.level >= project.skill.level:
                            project.members.append(contributor)
                            contributor.being_mentored = True
                            project.members.append(person)
                            person.is_mentor = True
                            break

            if project.is_full:
                break
        if len(project.members) > 0:
            run_project(project)
        else:
            projects.append(project)

        
    return projects

def projects_to_submission_file(projects):
    file_str = ""
    file_str += str(len(projects)) + "\n"
    for project in projects:
        file_str += project.name + "\n"
        first = True
        for member in project.members:
            if not first:
                file_str += " " + member.name
            else:
                file_str += member.name
            first = False
        if len(project.members) > 0:
            file_str += "\n"
    my_file = open("submission_file.txt", "wt")
    my_file.write(file_str)
    my_file.close()

def dirty_af(contributors, projects):
    for project in projects:
        for contributor in contributors:
            if contributor.valid_skills(project.skills):
                project.members.append(contributor)
                contributors.remove(contributor)
    print("Dirty af has completed")
    projects_to_submission_file(projects)



(projects, contributors) = import_from_file("data_sets/a_an_example.in.txt")


assign_contributors_to_projects(contributors, projects)
