"""Face detection and recognition demo using OpenCV and face_recognition."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import cv2

try:
    import face_recognition
except ImportError:  # pragma: no cover - optional dependency
    face_recognition = None


@dataclass
class FaceMatch:
    label: str
    location: tuple[int, int, int, int]  # top, right, bottom, left
    distance: float | None


def load_image(image_path: Path) -> any:
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Failed to read image: {image_path}")
    return image


def detect_faces(image: any, scale_factor: float = 1.1, min_neighbors: int = 5) -> list[tuple[int, int, int, int]]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
    classifier = cv2.CascadeClassifier(str(cascade_path))
    if classifier.empty():
        raise RuntimeError(f"Failed to load Haar cascade: {cascade_path}")
    faces = classifier.detectMultiScale(gray, scale_factor, min_neighbors)
    return [(x, y, w, h) for (x, y, w, h) in faces]


def encode_directory(known_dir: Path) -> tuple[list[str], list]:
    if face_recognition is None:
        raise RuntimeError("face_recognition library not installed; recognition unavailable.")
    labels: list[str] = []
    encodings: list = []
    for person_dir in known_dir.iterdir():
        if not person_dir.is_dir():
            continue
        for image_path in person_dir.glob("*"):
            if image_path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue
            image = face_recognition.load_image_file(image_path)
            faces = face_recognition.face_encodings(image)
            if not faces:
                continue
            encodings.append(faces[0])
            labels.append(person_dir.name)
    return labels, encodings


def recognize_faces(image: any, known_labels: Sequence[str], known_encodings: Sequence, tolerance: float = 0.6) -> list[FaceMatch]:
    if face_recognition is None:
        raise RuntimeError("face_recognition library not installed; recognition unavailable.")
    rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    matches: list[FaceMatch] = []
    for encoding, location in zip(encodings, face_locations):
        if not known_encodings:
            matches.append(FaceMatch("Unknown", location, None))
            continue
        distances = face_recognition.face_distance(known_encodings, encoding)
        best_idx = distances.argmin()  # type: ignore[attr-defined]
        label = known_labels[best_idx]
        distance = float(distances[best_idx])
        if distance > tolerance:
            label = "Unknown"
        matches.append(FaceMatch(label, location, distance))
    return matches


def annotate(image: any, matches: Iterable[FaceMatch]) -> any:
    for match in matches:
        top, right, bottom, left = match.location
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(
            image,
            f"{match.label} ({match.distance:.2f})" if match.distance is not None else match.label,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
            cv2.LINE_AA,
        )
    return image


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Face detection and recognition demo.")
    parser.add_argument("image", type=Path, help="Path to the target image.")
    parser.add_argument("--known-dir", type=Path, help="Directory holding known identities in subfolders.")
    parser.add_argument("--tolerance", type=float, default=0.6, help="Recognition tolerance (lower is stricter).")
    parser.add_argument("--display", action="store_true", help="Show annotated image in a window.")
    parser.add_argument("--save", type=Path, help="Optional path to save annotated output.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    image = load_image(args.image)

    boxes = detect_faces(image)
    print(f"Detected {len(boxes)} faces via Haar cascade.")

    known_labels: list[str] = []
    known_encodings: list = []
    matches: list[FaceMatch] = []

    if args.known_dir:
        known_labels, known_encodings = encode_directory(args.known_dir)
        print(f"Loaded {len(known_labels)} known faces.")

    if known_encodings:
        matches = recognize_faces(image, known_labels, known_encodings, args.tolerance)
        for match in matches:
            distance = f"{match.distance:.2f}" if match.distance is not None else "N/A"
            print(f"{match.label}: location={match.location} distance={distance}")
    else:
        matches = [FaceMatch("Face", (y, x + w, y + h, x), None) for (x, y, w, h) in boxes]

    annotated = annotate(image.copy(), matches)
    if args.save:
        cv2.imwrite(str(args.save), annotated)
        print(f"Saved annotated image to {args.save}")
    if args.display:
        cv2.imshow("Faces", annotated)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

