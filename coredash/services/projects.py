from sqlalchemy import or_, select
from coredash.model.project import Project


def project_search_query(search_data=None):
    q = select(Project)

    search_data = search_data or []

    if x := search_data.get('search'):
        for word in x.split():
            q = q.where(or_(
                Project.title.like(f"%{word}%"),
                Project.summary.like(f"%{word}%"),
                Project.comments.like(f"%{word}%"),
                Project.local_rec_number.like(f"%{word}%"),
                Project.iras_number.like(f"%{word}%"),
            ))

    return q
