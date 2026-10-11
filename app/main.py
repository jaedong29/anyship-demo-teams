import os
import random
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Team Split", version="1.0.0")


class TeamRequest(BaseModel):
    participants: list[str] = Field(min_length=2, max_length=60)
    team_count: int = Field(ge=2, le=12, strict=True)
    seed: int = Field(default=1, ge=0, le=999999, strict=True)

    @field_validator("participants")
    @classmethod
    def check_names(cls, names: list[str]) -> list[str]:
        names = [name.strip() for name in names]
        if any(not name or len(name) > 30 for name in names):
            raise ValueError("참가자 이름은 1~30자로 입력해 주세요.")
        if len(set(names)) != len(names):
            raise ValueError("같은 이름이 있으면 번호를 붙여 구분해 주세요.")
        return names


@app.get("/")
def index() -> FileResponse:
    return FileResponse(Path(__file__).with_name("index.html"))


@app.get("/healthz")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "team-split"}


@app.post("/api/teams")
def split_teams(request: TeamRequest) -> dict:
    from fastapi import HTTPException

    if request.team_count > len(request.participants):
        raise HTTPException(422, "팀 수는 참가자 수보다 많을 수 없습니다.")
    names = request.participants.copy()
    random.Random(request.seed).shuffle(names)
    groups = [
        {"name": f"{number + 1}팀", "members": names[number::request.team_count]}
        for number in range(request.team_count)
    ]
    return {"groups": groups, "participant_count": len(names), "seed": request.seed}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
