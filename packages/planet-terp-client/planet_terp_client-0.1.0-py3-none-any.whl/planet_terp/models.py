from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Course:
    department: str
    course_number: str
    title: str
    description: str
    credits: int
    professors: List[str]
    average_gpa: Optional[float] = None

    @staticmethod
    def from_dict(data: dict) -> "Course":
        return Course(
            department=data.get("department"),
            course_number=data.get("course_number"),
            title=data.get("title"),
            description=data.get("description"),
            credits=data.get("credits"),
            professors=data.get("professors", []),
            average_gpa=data.get("average_gpa"),
        )


@dataclass
class Instructor:
    name: str
    slug: str
    type: str
    courses: List[str]
    average_rating: Optional[float] = None
    reviews: Optional[List[dict]] = None

    @staticmethod
    def from_dict(data: dict) -> "Instructor":
        # make a factory method to return either Professor or TA
        if data.get("type") == "ta":
            cls = TA
        else:
            cls = Professor

        return cls(
            name=data.get("name"),
            slug=data.get("slug"),
            type=data.get("type"),
            courses=data.get("courses", []),
            average_rating=data.get("average_rating"),
            reviews=data.get("reviews"),
        )


@dataclass
class Professor(Instructor):
    pass


@dataclass
class TA(Instructor):
    pass


@dataclass
class Grade:
    course: str
    professor: str
    semester: str
    section: str
    A_plus: int
    A: int
    A_minus: int
    B_plus: int
    B: int
    B_minus: int
    C_plus: int
    C: int
    C_minus: int
    D_plus: int
    D: int
    D_minus: int
    F: int
    W: int
    Other: int

    @staticmethod
    def from_dict(data: dict) -> "Grade":
        return Grade(
            course=data.get("course"),
            professor=data.get("professor"),
            semester=data.get("semester"),
            section=data.get("section"),
            A_plus=data.get("A+"),
            A=data.get("A"),
            A_minus=data.get("A-"),
            B_plus=data.get("B+"),
            B=data.get("B"),
            B_minus=data.get("B-"),
            C_plus=data.get("C+"),
            C=data.get("C"),
            C_minus=data.get("C-"),
            D_plus=data.get("D+"),
            D=data.get("D"),
            D_minus=data.get("D-"),
            F=data.get("F"),
            W=data.get("W"),
            Other=data.get("Other"),
        )


@dataclass
class SearchResult:
    name: str
    slug: str
    type: str

    @staticmethod
    def from_dict(data: dict) -> "SearchResult":
        return SearchResult(
            name=data.get("name"), slug=data.get("slug"), type=data.get("type")
        )
