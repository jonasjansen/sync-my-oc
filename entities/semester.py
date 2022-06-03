class Semester:

    semester_name = ""
    semester_alternative_name = ""
    course_list = list()

    def __init__(self, semester_name, semester_alternative_name, course_list = list() ):
        self.semester_name = semester_name
        self.semester_alternative_name = semester_alternative_name
        self.course_list = course_list
        return
