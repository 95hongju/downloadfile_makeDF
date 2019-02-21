# downloadfile_makeDF

18.12.21 search
19.01.02 infos 수정(테이블크기늘림)
19.01.08 rsID에 CHR/POS검색 추가
19.01.11 snpedia report generagtor (/snp/) 추가
19.01.18 GSA1.2와 snpedia 카테고리 중복 rsID들로 DB생성
19.01.22 DB에서 먼저 결과검색 후 API로 검색
19.01.22 snpedia 검색 한개만 하는 것 추가
19.01.23 API에서 검색한 것들을 파일로 남겨서 매주 일요일마다 DB update(snp/snpmaking 에 snp만드는데 썼던 ipynb/py코드 있음)
19.02.08 blacklist 기능추가(infos처럼 수정삭제추가 가능), infos 파일업로드 txt에서 csv로 바꿈
19.02.11 모든 기능들 파일업로드를 txt->csv파일로 수정. 모든 기능들 usage페이지 추가
19.02.21 blacklist 데이터가 2만개다보니까 한번에 다띄우는데 오래걸림-> pagination
         검색결과나 전체 결과를 (현재 창에 띄워지는 테이블) csv로 저장하는 기능 추가
        infos에도 같은 형식 적용함(pagination, csv다운로드) / infos 모델오브젝트 전체날릴수있는기능 추가
