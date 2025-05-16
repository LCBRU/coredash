from sqlalchemy import or_, select
from coredash.model.people import Person


def person_search_query(search_data=None):
    q = select(Person)
    
    search_data = search_data or []

    if x := search_data.get('search'):
        for word in x.split():
            q = q.where(or_(
                Person.first_name.like(f"%{word}%"),
                Person.last_name.like(f"%{word}%"),
                Person.comments.like(f"%{word}%"),
                Person.orcid.like(f"%{word}%"),
            ))

    if x := search_data.get('job_title_id'):
        q = q.where(Person.job_title_id == x)

    if x := search_data.get('ukcrc_health_category_id'):
        q = q.where(Person.ukcrc_health_category_id == x)

    if x := search_data.get('professional_background_id'):
        q = q.where(Person.professional_background_id == x)

    if x := search_data.get('professional_background_detail_id'):
        q = q.where(Person.professional_background_detail_id == x)

    return q
