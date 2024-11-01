-- Users 테이블 (Oauth2.0 로그인을 위해 사용자 정보 관리 필드 추가 필요)
CREATE TABLE Users (
  user_uuid TEXT PRIMARY KEY NOT NULL,                              -- 사용자 UUID를 저장
  username TEXT NOT NULL UNIQUE,                                    -- 사용자 이름은 고유해야 함
  -- provider TEXT UNIQUE                                              -- google, facebook, kakao, naver 등
  -- email TEXT NOT NULL UNIQUE,                                       -- provider email OAuth를 통해 필수로 제공됨
  -- provider_id TEXT UNIQUE,                                          -- provider ID (provider에서 발급한 사용자 고유 ID)
  profile_image_url TEXT,                                           -- 사용자 프로필 이미지 URL (provider 프로필, 변경 하면 이미지 경로 저장)
  tier TEXT NOT NULL,                                               -- 게임 내 티어 게임 별로 정해진 값이 있음.
                                                                    -- ex) lol              : 'UNRANK', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER'
                                                                    -- ex) valorant         : 'UNRANK', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'IMMOTAL', 'RADIANT'
                                                                    -- ex) eternal return   : 'UNRANK', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'METEORITE', 'MYTHRIL', 'TITAN', 'IMMORTAL'
  primary_lane ENUM('TOP', 'JUG', 'MID', 'AD', 'SUP') NOT NULL,     -- 첫 번째로 선호하는 포지션
  secondary_lane ENUM('TOP', 'JUG', 'MID', 'AD', 'SUP') NOT NULL,   -- 두 번째로 선호하는 포지션
  is_captain BOOLEAN NOT NULL DEFAULT FALSE,                        -- 팀장 가능 여부
  status BOOLEAN NOT NULL DEFAULT TRUE,                             -- 유저 활성화, 비활성화 여부
  base_price INTEGER NOT NULL DEFAULT 0 CHECK (base_price >= 0),    -- 추후 개인 티어별로 나눌 점수
  -- profile_image_path TEXT,                                       -- profile_image_url로 대체
  current_team_uuid TEXT,                                           -- 현재 소속 팀 UUID 추가 (여러 팀을 가질 수 있음)
  CHECK (primary_lane <> secondary_lane),
  FOREIGN KEY (current_team_uuid) REFERENCES Teams(team_uuid)       -- 외래 키 제약 조건 추가
);

-- Teams 테이블
CREATE TABLE Teams (
  team_uuid TEXT PRIMARY KEY NOT NULL,                        -- 팀 UUID 저장
  team_name TEXT NOT NULL UNIQUE,                             -- 팀 이름은 유일해야 함
  captain_uuid TEXT NOT NULL,                                 -- 팀장 uuid
  budget INTEGER NOT NULL CHECK (budget >= 0) DEFAULT 1000,   -- 경매 시 필요한 기본 소유액
  FOREIGN KEY (captain_uuid) REFERENCES Users(user_uuid)
);

-- 한 명의 플레이어가 여러 팀에 속하도록 수정필요
CREATE TABLE TeamPlayers (
  team_uuid TEXT NOT NULL,
  player_uuid TEXT NOT NULL,
  FOREIGN KEY (team_uuid) REFERENCES Teams(team_uuid),
  FOREIGN KEY (player_uuid) REFERENCES Users(user_uuid)
);

-- 경매 중 사용할 테이블
CREATE TABLE Auctions (
  auction_room_name TEXT PRIMARY KEY,                                         -- 경매 방 이름
  team_uuid TEXT NOT NULL,
  player_uuid TEXT NOT NULL,
  bid_amount INTEGER NOT NULL,                                                -- 입찰 금액
  start_time DATETIME DEFAULT CURRENT_TIMESTAMP,                              -- 경매 시작 시간
  end_time DATETIME,                                                          -- 경매 유예 시간, 끝나는 시간
  auction_status ENUM('OPEN', 'CLOSE', 'IN_PROGRESS', 'PENDING') NOT NULL,    -- 경매 상태
                                                                              -- OPEN        : 경매 방이 열리기만 한 상태
                                                                              -- IN_PROGRESS : 경매가 진행 중인 상태
                                                                              -- PENDING     : 낙찰 후 다음 경매를 위한 휴식 상태
                                                                              -- CLOSE       : 모든 경매 종료 후 경매 방이 닫힌상태
  FOREIGN KEY (team_uuid) REFERENCES Teams(team_uuid),
  FOREIGN KEY (player_uuid) REFERENCES Users(user_uuid)
);

-- 최종 경매 기록을 보여줄 테이블
CREATE TABLE AuctionRecords (
  record_id INTEGER PRIMARY KEY AUTOINCREMENT,
  auction_room_name TEXT NOT NULL,
  bidder_uuid TEXT NOT NULL,                                                -- 입찰자 uuid
  remaining_bid_amount INTEGER NOT NULL,                                    -- 남은 입찰 금액
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (auction_room_name) REFERENCES Auctions(auction_room_name),
  FOREIGN KEY (bidder_uuid) REFERENCES Users(user_uuid)
);

-- -- OAuth2.0를 통한 로그인 관리를 위한 Tokens 테이블(쿠키, 세션으로 관리할 지 DB에 넣어서 관리할지 여부는 아직 모름)
-- CREATE TABLE Tokens (
--   token_id UUID PRIMARY KEY,                         -- 토큰 고유 ID
--   user_uuid UUID NOT NULL,                           -- 사용자 ID
--   refresh_token TEXT UNIQUE,                         -- refresh token
--   access_token TEXT,                                 -- access token (단기 유효)
--   id_token TEXT,                                     -- provider id_token (JWT 형식, 사용자 정보 포함)
--   expires_at TIMESTAMP NOT NULL,                     -- access token 만료 시간
--   FOREIGN KEY (user_uuid) REFERENCES Users(user_uuid) ON DELETE CASCADE
-- );