class Course:

    course_name = ""
    course_lecturer = ""
    course_link = ""
    event_list = list()

    def __init__(self, course_name, course_link, course_lecturer):
        self.course_name = course_name
        self.course_lecturer = course_lecturer
        self.course_link = course_link
        self.event_list = list()
        return
