import pytest

from google_parser import retreive_google_career_qualification
from meta_parser import retrieve_meta_career_qualification
from gemini_summarizer import return_gemini_summary


def test_google_parser():
    url = "https://www.google.com/about/careers/applications/jobs/results/75038123993506502-associate-product-manager-university-graduate-2026-start"
    answer = {'Minimum qualifications:': ['Currently enrolled in or graduated from a degree program within Product Management, Computer Science, Engineering, Data Science, Mathematics, Statistics, or a related technical field, or equivalent practical experience.', 'Internship or Teaching Assistant experience in product management, software development or a similar technical field.', 'Experience leading entrepreneurial efforts or outreach within organizations while building cross-functional relationships.', 'Experience preparing and delivering technical presentations to an audience through internships, coursework, or extracurriculars.'],
              'Preferred qualifications:': ['Experience with methodologies aimed to drive product development and delivery.', 'Experience applying AI/ML concepts to build products or features through relevant internship, capstone projects, or other academic work.', 'Technical experience with programming languages, data analysis, business case/modeling, pricing, or design.', 'Ability to start full-time in the primary cohort onboarding cycle between April and August 2026.', 'Ability to communicate in English fluently to support cross-functional business relationships in the region.', 'Excellent problem-solving, organizational, investigative, and critical thinking skills.']}
    returned_output = retreive_google_career_qualification(url)
    assert answer == returned_output


def test_meta_parser():
    url = 'https://www.metacareers.com/jobs/1516686172846137'
    answer = {'Minimum Qualifications': ['Bachelor\'s degree (or foreign degree equivalent) in Computer Science, Engineering, Information Systems, Analytics, Mathematics, Physics, Applied Sciences, or a related field and 1 year of experience in the job offered or a computer-related field. Experience must include 1 year of experience in the following:',
                                         '1. Coding in at least one of the following industry-standard languages: C, C++, Java, or C#',
                                         '2. Building large-scale infrastructure applications',
                                         '3. Creating web applications using at least one of the following: Python, PHP, or Ruby',
                                         '4. Relational databases',
                                         '5. SQL',
                                         '6. Implementing web interfaces using at least one of the following: JavaScript, HTML, or CSS',
                                         ]}
    returned_output = retrieve_meta_career_qualification(url)
    assert returned_output == answer


@pytest.mark.timeout(240)
def test_gemini_summary():
    input = {'Minimum Qualifications': ["Bachelor's degree in Computer Science, Computer Engineering,\
                                    relevant technical field, or equivalent practical experience",
                                        '8+ years of experience (4 years+ of experience post Ph.D.)\
                                     with advanced SQL in big data environments (e.g., Hive, Presto, Spark)\
                                     and data modeling',
                                        '8+ years of experience (4 years+ of experience post Ph.D.) managing\
                                     and analyzing large-scale data using Python, R, or similar languages',
                                        'Hands-on programming experience in one or more of:\
                                    AI/ML, LLM, NLP, Statistical modeling'],
             'Preferred Qualifications': ['Technical knowledge of data center operations',
                                          'Masters degree in Computer Science, Engineering,\
                                       Mathematics, Statistics, Operations Research,\
                                       or a related analytical field']}
    output = return_gemini_summary(input)
    assert "Python" in output and "Spark" in output


def test_gemini_pep8():
    """Ensure code passes pycodestyle with fewer than 5 issues"""
    import subprocess
    result = subprocess.run(
        ["pycodestyle", "gemini_summarizer.py"],
        capture_output=True,
        text=True
    )
    errors = result.stdout.strip().splitlines()
    assert len(errors) < 2, f"Too many PEP8 issues:\n{errors}"


def test_meta_pep8():
    """Ensure code passes pycodestyle with fewer than 5 issues"""
    import subprocess
    result = subprocess.run(
        ["pycodestyle", "meta_parser.py"],
        capture_output=True,
        text=True
    )
    errors = result.stdout.strip().splitlines()
    assert len(errors) < 2, f"Too many PEP8 issues:\n{errors}"


def test_google_pep8():
    """Ensure code passes pycodestyle with fewer than 5 issues"""
    import subprocess
    result = subprocess.run(
        ["pycodestyle", "google_parser.py"],
        capture_output=True,
        text=True
    )
    errors = result.stdout.strip().splitlines()
    assert len(errors) < 5, f"Too many PEP8 issues:\n{errors}"
