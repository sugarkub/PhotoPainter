# Waveshare PhotoPainter용 이미지 변환기

이 프로젝트는 Waveshare에서 판매하는 7색 eink 디스플레이를 탑재한 디지털 액자에 사용할 이미지를 생성하는 도구입니다.

## PhotoPainter 사용시 주의사항

아래 사항들을 만족하지 않으면 PhotoPainter의 기본 소프트웨어는 이미지를 제대로 표시하지 못합니다.

- SD카드는 FAT32로 포맷되어야 합니다.
- 이미지는 `pic` 폴더 안에 복사해야 하며, `pic` 폴더는 SD카드의 루트 폴더 아래에 존재해야 합니다.
- 이미지 크기는 가로 800 세로 480 픽셀이어야 합니다.
- 이미지 포맷은 Floyd-Steinberg Dithering 알고리즘이 적용된 BMP만 지원합니다.

## 패키지 요구사항

이미지 변환기를 사용하기 위해서는 `python3`가 설치되어있어야 하며, `python`에서 이미지를 처리하기 위한 `pillow` 패키지가 설치되어 있어야 합니다.

```terminal
$ pip install pillow
```

## 사용법

```terminal
$ python3 convert.py <src-dir> [dst-dir]
```

## 참고자료

- [Waveshare PhotoPainter](https://www.waveshare.com/wiki/PhotoPainter){:target="_blank"}
- [7 colour electronic paper](https://blog.matteoferla.com/2023/03/7-colour-electronic-paper.html){:target="_blank"}