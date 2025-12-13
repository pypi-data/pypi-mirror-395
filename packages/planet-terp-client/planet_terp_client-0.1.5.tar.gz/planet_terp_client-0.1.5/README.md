# planet-terp

a python client for the planet terp api.

## installation

```bash
uv add planet-terp-client
```

## usage

### get a course

```python
from planet_terp import PlanetTerp

client = PlanetTerp()

course = client.course("CMSC320")
print(course.title)
```

### get a professor

```python
professor = client.professor("Clyde Kruskal")
print(professor.average_rating)
# 2.75
```

### search

```python
results = client.search("CMSC320")
for result in results:
    print(result.name)
```

### get grades

```python
grades = client.grades(course="CMSC351", semester="202308")
for grade in grades:
    print(f"{grade.section}: {grade.professor}")
```

### check if instructor is ta or professor

```python
from planet_terp import TA

professors = client.professors(limit=10)
for p in professors:
    if isinstance(p, TA):
        print(f"{p.name} is a ta")
    else:
        print(f"{p.name} is a professor")
```

## advanced examples

### get average rating of all professors for a course

```python
course = client.course("CMSC330")
for name in course.professors:
    try:
        p = client.professor(name)
        if p.average_rating:
            print(f"{p.name}: {p.average_rating}")
    except:
        print(f"could not fetch {name}")
```

### calculate pass rate for a course

```python
grades = client.grades(course="CMSC351")
total_students = 0
passed_students = 0

for g in grades:
    section_total = (g.A_plus + g.A + g.A_minus + 
                   g.B_plus + g.B + g.B_minus + 
                   g.C_plus + g.C + g.C_minus + 
                   g.D_plus + g.D + g.D_minus + 
                   g.F + g.W + g.Other)
    
    # assuming C- or better is passing for major reqs
    section_pass = (g.A_plus + g.A + g.A_minus + 
                  g.B_plus + g.B + g.B_minus + 
                  g.C_plus + g.C + g.C_minus)
    
    total_students += section_total
    passed_students += section_pass

if total_students > 0:
    print(f"pass rate: {(passed_students/total_students)*100:.2f}%")
```
