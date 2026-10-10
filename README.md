# Team Split

행사·스터디·워크숍에서 참가자 명단을 비슷한 인원의 팀으로 나누는 작은 FastAPI 앱입니다.
명단과 결과를 서버에 저장하지 않으며 DB나 외부 API가 필요하지 않습니다.

## 실행

Python 3.12 환경에서:

```sh
python -m pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

브라우저에서 `http://localhost:8080`을 엽니다.
컨테이너는 `PORT` 환경변수와 `/healthz`를 사용합니다.

```sh
docker build --platform linux/amd64 -t team-split:demo .
docker run --rm -p 8080:8080 --read-only --tmpfs /tmp -e PORT=8080 team-split:demo
```

루트의 `Dockerfile`과 `deploy-spec.yaml`은 AWS 상시 실행 및 온프레미스 컨테이너 배포용입니다.
실제 서버 연결·DNS·인증서는 배포 서비스의 환경 설정을 사용합니다.
