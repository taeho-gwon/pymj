# CLAUDE.md

## 프로젝트 개요

pymj - 마작(Mahjong) 관련 Python 라이브러리

## 현재 상태

- 패키지 매니저: uv
- Python 버전: 3.13
- 린터/포매터: ruff, mypy
- 테스트: pytest

## 개발 규칙

- 린터: ruff (line-length 88)
- 타입체크: mypy (strict mode)
- 테스트: pytest + pytest-mock
- pre-commit 훅 사용
