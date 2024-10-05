/* sample db 및 데이터 생성 */
-- 1. db 생성
-- DROP DATABASE if exists blog_db;
CREATE DATABASE blog_db;

-- 2. 테이블 생성
-- 테이블 이미 존재하면 삭제 하고 진행
DROP TABLE if exists blog;
-- 테이블 생성
-- Integer display width is deprecated and will be removed in a future release.

CREATE TABLE blog (
  id int NOT NULL AUTO_INCREMENT, -- int(11) -> int로 변경: int(크기)는 deprecated
  title varchar(200) NOT NULL,
  author varchar(100) NOT NULL,
  content varchar(4000) NOT NULL,
  image_loc varchar(300) DEFAULT NULL,
  modified_dt datetime NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- 데이터 인서트
INSERT INTO blog_db.blog(title, author, content, modified_dt) values('테스트 title 1', '둘리', '테스트 컨텐츠 1', now());
INSERT INTO blog_db.blog(title, author, content, modified_dt) values('테스트 title 2', '길동', '테스트 컨텐츠 2', now());
INSERT INTO blog_db.blog(title, author, content, modified_dt) values('테스트 title 3', '도넛', '테스트 컨텐츠 3', now());
INSERT INTO blog_db.blog(title, author, content, modified_dt) values('테스트 title 4', '희동', '테스트 컨텐츠 4', now());

COMMIT;

/* connection 모니터링 스크립트. root로 수행 필요. */
select * from sys.session where db='blog_db' order by conn_id;
