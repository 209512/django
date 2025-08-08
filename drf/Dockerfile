# Dockerfile
FROM python:3.13-slim

# 작업 디렉토리 설정
WORKDIR /code

# 의존성 복사 및 설치
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# 전체 프로젝트 복사
COPY . /code/

# 외부 포트 노출 (docker-compose.yml에서 포트 매핑 별도 설정)
EXPOSE 8000

# Django 개발서버 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
