import requests

from bs4 import BeautifulSoup


def retrieve_meta_career_qualification(url: str) -> dict:
    """
    For the given Meta Career URL, retrieve all the "qualification" sections.
    This should return a dictionary format of the qualification string
    (Ex. Minimum qualification) as a key,
    and a list of paragraphs given under the qualifiaction string.
    {'Minimum qualifications:': ['Currently enrolled in or graduated from a
    degree program within Product Management, Computer Science, Engineering,
    Data Science, Mathematics, Statistics, or a related technical field,
    or equivalent practical experience.',
    'Internship or Teaching Assistant experience in product management,
    software development or a similar technical field.',
    'Experience leading entrepreneurial efforts or outreach
    within organizations while building cross-functional relationships.',
    'Experience preparing and delivering technical presentations to
    an audience through internships, coursework, or extracurriculars.'],
     'Preferred qualifications:': ['Experience with methodologies aimed to
     drive product development and delivery.',
     'Experience applying AI/ML concepts to build products or features
     through relevant internship, capstone projects, or other academic work.',
     'Technical experience with programming languages, data analysis,
     business case/modeling, pricing, or design.',
     'Ability to start full-time in the primary cohort onboarding cycle
     between April and August 2026.',
     'Ability to communicate in English fluently to
     support cross-functional business relationships in the region.',
     'Excellent problem-solving, organizational, investigative,
     and critical thinking skills.']}
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    qual_div = soup.find_all("div", class_="_8mlh")

    if not qual_div:
        return None

    qualifications = {}
    for section in qual_div:
        header_divs = section.find_all("div", class_="_1n-z")
        for div in header_divs:
            qualification = div.text.strip()
            if qualification in ("Minimum Qualifications",
                                 "Preferred Qualifications"):
                li_texts = [li.text.strip() for li in section.find_all("li")]
                qualifications[qualification] = li_texts

    return qualifications if qualifications else None
