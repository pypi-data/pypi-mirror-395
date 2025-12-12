from src.planet_terp import PlanetTerp, TA


def main():
    client = PlanetTerp()

    print("Demo")

    # 1. Course
    print("\n1. Fetching Course: CMSC320")
    try:
        course = client.course("CMSC320")
        print(f"Name: {course.department}{course.course_number}")
        print(f"Title: {course.title}")
        print(f"Credits: {course.credits}")
        print(f"Average GPA: {course.average_gpa}")
    except Exception as e:
        print(f"Error: {e}")

    # 2. Courses
    print("\n2. Fetching Courses (Department: CMSC, Limit: 3)")
    try:
        courses = client.courses(department="CMSC", limit=3)
        for c in courses:
            print(f"- {c.department}{c.course_number}: {c.title}")
    except Exception as e:
        print(f"Error: {e}")

    # 3. Professor
    print("\n3. Fetching Professor: Clyde Kruskal")
    try:
        professor = client.professor("Clyde Kruskal")
        print(f"Name: {professor.name}")
        print(f"Type: {professor.type}")
        print(f"Rating: {professor.average_rating}")
        print(f"Courses Taught: {len(professor.courses)} courses")
    except Exception as e:
        print(f"Error: {e}")

    # 4. Search
    print("\n4. Search (Query: 'CMSC320', Limit: 3)")
    try:
        results = client.search("CMSC320", limit=3)
        for r in results:
            print(f"- {r.slug} ({r.type})")
    except Exception as e:
        print(f"Error: {e}")

    # 5. Grades
    print("\n5. Fetching Grades (CMSC351, Fall 2023)")
    try:
        grades = client.grades(course="CMSC351", semester="202308")
        print(f"Found {len(grades)} sections.")
        if grades:
            g = grades[0]
            print(
                f"Sample (Section {g.section}, Prof. {g.professor}): A={g.A}, B={g.B}, C={g.C}, D={g.D}, F={g.F}, W={g.W}"
            )
    except Exception as e:
        print(f"Error: {e}")

    # 6. Professors and TAs
    print("\n6. Fetching Professors and TAs (Limit: 10)")
    try:
        professors = client.professors(limit=10)
        print(f"Fetched {len(professors)} instructors.")
        for p in professors:
            role = "TA" if isinstance(p, TA) else "Professor"
            print(f"- {p.name} ({role})")
    except Exception as e:
        print(f"Error: {e}")

    # 7. Type-Safe Review Access
    print("\n7. Review Access (Checking reviews for Clyde Kruskal)")
    try:
        prof = client.professor("Clyde Kruskal", reviews=True)
        if prof.reviews:
            print(f"Found {len(prof.reviews)} reviews.")
            first_review = prof.reviews[0]
            print(
                f"First review course: {first_review.course} (Rating: {first_review.rating})"
            )
            print(f"Created at: {first_review.created}")
    except Exception as e:
        print(f"Error: {e}")

    # 8. Professor Ratings for a Course
    print("\n8. Professor Ratings for CMSC330")
    try:
        course = client.course("CMSC330")
        for name in course.professors[:5]:
            try:
                p = client.professor(name)
                if p.average_rating:
                    print(f"- {p.name}: {p.average_rating}")
            except:
                pass
    except Exception as e:
        print(f"Error: {e}")

    # 8. Pass Rate Calculation
    print("\n8. Pass Rate for CMSC351")
    try:
        grades = client.grades(course="CMSC351")
        total_students = 0
        passed_students = 0

        for g in grades:
            section_total = (
                g.A_plus
                + g.A
                + g.A_minus
                + g.B_plus
                + g.B
                + g.B_minus
                + g.C_plus
                + g.C
                + g.C_minus
                + g.D_plus
                + g.D
                + g.D_minus
                + g.F
                + g.W
                + g.Other
            )

            # assuming C- or better is passing for major reqs
            section_pass = (
                g.A_plus
                + g.A
                + g.A_minus
                + g.B_plus
                + g.B
                + g.B_minus
                + g.C_plus
                + g.C
                + g.C_minus
            )

            total_students += section_total
            passed_students += section_pass

        if total_students > 0:
            print(
                f"Pass Rate: {(passed_students / total_students) * 100:.2f}% (Total Students: {total_students})"
            )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
