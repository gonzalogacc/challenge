import sqlalchemy as sa
from models.models import Files, Tags, FileTags
from sqlalchemy.orm import Session


def tags_from_filename(
        filename: str
        ):
    """ Given a filename return a list of tags
    assumes:
        - the filename is the name_surname format separated by underscores. 
        - the last component is the image number in the file

    """
    return filename.split("_")[:-1]


def get_or_create_tag(
        name: str,
        ses: Session
        ):
    """ Given a tag name, return the tag object
    """
    stmt = sa.select(Tags).filter(Tags.name == name)
    tag = ses.execute(stmt).one_or_none()
    if tag is None:
        tag = Tags(name=name)
        ses.add(tag)
        ses.commit()
        ses.refresh(tag)
        return tag
    else:
        return tag[0]

def process_name_tags(
        filename: str,
        ses: Session
    ):
    tags = tags_from_filename(filename)
    tags_objs = []
    for tag in tags:
        print(f"XXXXXX Ttag: {tag}")
        tag_obj = get_or_create_tag(tag, ses)
        tags_objs.append(tag_obj)
    return tags_objs
