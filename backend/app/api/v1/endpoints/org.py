from fastapi import APIRouter, HTTPException
from app.schemas.org import OrgContent
from app.utils.org_parser import OrgParser

router = APIRouter()
parser = OrgParser()

@router.post("/parse")
async def parse_org(content: OrgContent):
    try:
        parsed = parser.parse(content.content)
        html = parser.to_html(parsed)
        return {"html": html}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 