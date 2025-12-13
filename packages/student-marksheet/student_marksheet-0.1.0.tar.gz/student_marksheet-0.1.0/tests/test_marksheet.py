from student_marksheet import Marksheet

def test_basic():
    m = Marksheet("Swami", 1)
    m.add_mark("Math", 90)
    m.add_mark("Science", 80)

    assert m.total() == 170
    assert round(m.percentage(), 2) == 85
    assert m.grade() == "A"
