import requests
from typing import List, Optional
from .models import Course, Instructor, Professor, TA, Grade, SearchResult


class PlanetTerp:
    BASE_URL = "https://planetterp.com/api/v1"

    def __init__(self):
        self.session = requests.Session()

    def _get(self, endpoint: str, params: dict = None) -> any:
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def course(self, name: str, reviews: bool = False) -> Course:
        """
        Get a specific course by name.
        """
        params = {"name": name, "reviews": "true" if reviews else "false"}
        data = self._get("/course", params=params)
        return Course.from_dict(data)

    def courses(
        self,
        department: str = None,
        reviews: bool = False,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Course]:
        """
        Get a list of courses.
        """
        params = {
            "reviews": "true" if reviews else "false",
            "limit": limit,
            "offset": offset,
        }
        if department:
            params["department"] = department

        data = self._get("/courses", params=params)
        return [Course.from_dict(item) for item in data]

    def professor(self, name: str, reviews: bool = False) -> Instructor:
        """
        Get a specific professor by name.
        """
        params = {"name": name, "reviews": "true" if reviews else "false"}
        data = self._get("/professor", params=params)
        return Instructor.from_dict(data)

    def professors(
        self,
        type_: str = None,
        reviews: bool = False,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Instructor]:
        """
        Get a list of professors.
        type_: 'professor' or 'ta'
        """
        params = {
            "reviews": "true" if reviews else "false",
            "limit": limit,
            "offset": offset,
        }
        if type_:
            params["type"] = type_

        data = self._get("/professors", params=params)
        return [Instructor.from_dict(item) for item in data]

    def grades(
        self,
        course: str = None,
        professor: str = None,
        semester: str = None,
        section: str = None,
    ) -> List[Grade]:
        """
        Get grades data. At least one of course or professor is required.
        """
        if not course and not professor:
            raise ValueError(
                "At least one of 'course' or 'professor' must be provided."
            )

        params = {}
        if course:
            params["course"] = course
        if professor:
            params["professor"] = professor
        if semester:
            params["semester"] = semester
        if section:
            params["section"] = section

        data = self._get("/grades", params=params)
        return [Grade.from_dict(item) for item in data]

    def search(
        self, query: str, limit: int = 30, offset: int = 0
    ) -> List[SearchResult]:
        """
        Search for professors and courses.
        """
        params = {"query": query, "limit": limit, "offset": offset}
        data = self._get("/search", params=params)
        return [SearchResult.from_dict(item) for item in data]
