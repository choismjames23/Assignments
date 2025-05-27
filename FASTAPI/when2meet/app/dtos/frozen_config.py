from pydantic import ConfigDict

FROZEN_CONFIG = ConfigDict(frozen=True)
# 얼어있는 객체 -> 생성 이후에는 변경할 수 없는 객체 (immutable)
