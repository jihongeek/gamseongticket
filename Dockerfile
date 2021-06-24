# 1. 우분투 설치
FROM debian:buster

# 2. 메타데이터 표시
LABEL "purpose"="basic image for gamseongticket"

# 3. apt 업데이트 및 관련 패키지 설치
RUN apt update && apt -y install wget uwsgi python3 python3-pip
RUN pip3 install uwsgi flask imgkit
RUN cd /var && mkdir www
WORKDIR /var/www/

# wkhtmltopdf 다운로드 및 설치
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb
RUN dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb; exit 0
RUN apt -f -y install
RUN dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb 

# 파일,디렉터리 복사 붙혀넣기
COPY . /var/www
# wkhtmltopdf 설치파일 삭제 및 uwsgi 서버 실행 
RUN rm /var/www/wkhtmltox_0.12.6-1.buster_amd64.deb
CMD uwsgi --ini /var/www/gamseongticket.ini
# 7. 포트 5000번 노출 지정
EXPOSE 5000

