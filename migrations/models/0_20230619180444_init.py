from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL,
    "bio" VARCHAR(512),
    "photo" TEXT NOT NULL,
    "age" SMALLINT NOT NULL,
    "need_age" SMALLINT NOT NULL,
    "sex" SMALLINT NOT NULL,
    "need_sex" SMALLINT NOT NULL,
    "country" VARCHAR(64) NOT NULL,
    "state" VARCHAR(64) NOT NULL,
    "city" VARCHAR(64) NOT NULL,
    "latitude" DOUBLE PRECISION NOT NULL,
    "longitude" DOUBLE PRECISION NOT NULL
);
COMMENT ON COLUMN "users"."sex" IS 'FEMALE: 1\nMALE: 2\nANY: 3';
COMMENT ON COLUMN "users"."need_sex" IS 'FEMALE: 1\nMALE: 2\nANY: 3';
CREATE TABLE IF NOT EXISTS "reactions" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "type" SMALLINT NOT NULL,
    "is_read" BOOL NOT NULL,
    "date" DATE NOT NULL,
    "receiver_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "sender_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "reactions"."type" IS 'RECIPROCITY: 1\nFOLLOWER: 2\nUSER: 3\nHATER: 4\nOTHER: 5';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
