select * from [user]
select * from chd
drop table chd
-- Tạo bảng chd
CREATE TABLE chd (
  IDCHD INT IDENTITY(1,1) PRIMARY KEY,
  IDuser INT,
  sbp FLOAT,
  tobacco FLOAT,
  ldl FLOAT,
  adiposity FLOAT,
  famhist INT,
  typea FLOAT,
  obesity FLOAT,
  alcohol FLOAT,
  age FLOAT,
  prediction INT,
  CONSTRAINT FK_chd_user FOREIGN KEY (IDuser) REFERENCES [user] (IDuser)
);

-- Tạo bảng user
CREATE TABLE [user] (
  IDuser INT IDENTITY(1,1) PRIMARY KEY,
  fullname VARCHAR(255) NOT NULL,
  username VARCHAR(255) NOT NULL,
  [password] VARCHAR(255) NOT NULL
);

-- Tạo chỉ mục cho bảng chd
CREATE INDEX IDX_chd_IDuser ON chd (IDuser);

-- Tạo chỉ mục cho bảng user
CREATE INDEX IDX_user_IDuser ON [user] (IDuser);


