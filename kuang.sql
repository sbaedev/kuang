-- Users 테이블 (Oauth2.0 로그인을 위해 사용자 정보 관리 필드 추가 필요)
CREATE TABLE Users (
  user_uuid TEXT PRIMARY KEY NOT NULL,
  username TEXT NOT NULL UNIQUE,  -- 사용자 이름은 유일해야 함
  tier ENUM('IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER') NOT NULL,
  primary_line ENUM('TOP', 'JUG', 'MID', 'AD', 'SUP') NOT NULL,
  secondary_line ENUM('TOP', 'JUG', 'MID', 'AD', 'SUP') NOT NULL,
  is_captain BOOLEAN NOT NULL DEFAULT FALSE,
  base_price INTEGER NOT NULL DEFAULT 0 CHECK (base_price >= 0),
  profile_image_path TEXT,
  current_team_uuid TEXT,  -- 현재 소속 팀 UUID 추가
  CHECK (primary_line <> secondary_line),
  FOREIGN KEY (current_team_uuid) REFERENCES Teams(team_uuid)  -- 외래 키 제약 조건 추가
);

-- Teams 테이블
CREATE TABLE Teams (
  team_uuid TEXT PRIMARY KEY NOT NULL,
  team_name TEXT NOT NULL UNIQUE,  -- 팀 이름은 유일해야 함
  captain_uuid TEXT NOT NULL,
  budget INTEGER NOT NULL CHECK (budget >= 0) DEFAULT 1000,
  FOREIGN KEY (captain_uuid) REFERENCES Users(user_uuid)
);

-- 한 명의 플레이어가 여러 팀에 속하도록 수정필요
CREATE TABLE TeamPlayers (
  team_player_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 고유 ID 추가
  team_uuid TEXT NOT NULL,
  player_uuid TEXT NOT NULL,
  FOREIGN KEY (team_uuid) REFERENCES Teams(team_uuid),
  FOREIGN KEY (player_uuid) REFERENCES Users(user_uuid)
);

-- 경매 중 사용할 테이블
CREATE TABLE Auctions (
  auction_room_name TEXT PRIMARY KEY,
  team_uuid TEXT NOT NULL,
  player_uuid TEXT NOT NULL,
  bid_amount INTEGER NOT NULL,
  start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  end_time DATETIME,
  auction_status ENUM('OPEN', 'CLOSE', 'IN_PROGRESS', 'PENDING') NOT NULL,
  FOREIGN KEY (team_uuid) REFERENCES Teams(team_uuid),
  FOREIGN KEY (player_uuid) REFERENCES Users(user_uuid)
);

-- 최종 경매 기록을 보여줄 테이블
CREATE TABLE AuctionRecords (
  record_id INTEGER PRIMARY KEY AUTOINCREMENT,
  auction_room_name TEXT NOT NULL,
  bidder_uuid TEXT NOT NULL,
  bid_amount INTEGER NOT NULL,
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